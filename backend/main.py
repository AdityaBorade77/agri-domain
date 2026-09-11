"""
main.py — FastAPI Backend
Marathi-English Speech Translator PWA

Routes:
  POST /api/speech-to-text   Audio → Marathi text + English translation
  POST /api/text-to-speech   English text → Marathi audio + word timings
  GET  /api/health           Health check
"""

import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Import model modules
from models.asr import transcribe_marathi
from models.translation import translate_marathi_to_english, translate_english_to_marathi
from models.tts import synthesize_marathi_speech


# ─── App Setup ────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle."""
    logger.info("🚀 Marathi-English Speech Translator API starting...")
    logger.info("Inference mode: %s", os.getenv("INFERENCE_MODE", "api"))
    logger.info("TTS Voice: %s", os.getenv("TTS_VOICE", "Sunita"))
    yield
    logger.info("API shutting down.")


app = FastAPI(
    title="Marathi-English Speech Translator",
    description="PWA backend for Marathi ASR + IndicTrans2 + Indic Parler-TTS",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow frontend to call the API
frontend_origin = os.getenv("FRONTEND_ORIGIN", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin] if frontend_origin != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Pydantic Models ──────────────────────────────────────────────────────────

class TextToSpeechRequest(BaseModel):
    english_text: str


class SpeechToTextResponse(BaseModel):
    marathi_text: str
    english_text: str
    success: bool = True


class TextToSpeechResponse(BaseModel):
    marathi_text: str
    audio_base64: str
    word_timings: list
    duration: float
    voice: str
    success: bool = True


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "inference_mode": os.getenv("INFERENCE_MODE", "api"),
        "tts_voice": os.getenv("TTS_VOICE", "Sunita"),
        "device": os.getenv("DEVICE", "cpu"),
        "hf_token_set": bool(os.getenv("HF_TOKEN")),
    }


@app.post("/api/speech-to-text", response_model=SpeechToTextResponse)
async def speech_to_text(audio: UploadFile = File(...)):
    """
    Convert Marathi speech audio to English text.

    Pipeline:
      Audio (WebM/WAV/OGG) → IndicConformer → Marathi Text → IndicTrans2 → English Text
    """
    if not audio.filename:
        raise HTTPException(status_code=400, detail="No audio file provided.")

    logger.info("Received audio: %s (%s)", audio.filename, audio.content_type)

    try:
        audio_bytes = await audio.read()

        if len(audio_bytes) < 100:
            raise HTTPException(status_code=400, detail="Audio file is too small or empty.")

        # Step 1: Transcribe Marathi speech → Marathi text
        marathi_text = await transcribe_marathi(audio_bytes)
        logger.info("Transcribed: %s", marathi_text[:100])

        if not marathi_text.strip():
            return SpeechToTextResponse(
                marathi_text="",
                english_text="(No speech detected)",
                success=True,
            )

        # Step 2: Translate Marathi → English
        english_text = await translate_marathi_to_english(marathi_text)
        logger.info("Translated: %s", english_text[:100])

        return SpeechToTextResponse(
            marathi_text=marathi_text,
            english_text=english_text,
        )

    except HTTPException:
        raise
    except RuntimeError as e:
        logger.error("Model error in speech-to-text: %s", e)
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error in speech-to-text")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/api/text-to-speech", response_model=TextToSpeechResponse)
async def text_to_speech(request: TextToSpeechRequest):
    """
    Convert English text to Marathi speech audio.

    Pipeline:
      English Text → IndicTrans2 → Marathi Text → Indic Parler-TTS → Audio + Word Timings
    """
    english_text = request.english_text.strip()

    if not english_text:
        raise HTTPException(status_code=400, detail="No text provided.")

    if len(english_text) > 2000:
        raise HTTPException(status_code=400, detail="Text too long (max 2000 chars).")

    logger.info("TTS request: %s", english_text[:100])

    try:
        # Step 1: Translate English → Marathi
        marathi_text = await translate_english_to_marathi(english_text)
        logger.info("Translated to Marathi: %s", marathi_text[:100])

        if not marathi_text.strip():
            raise HTTPException(status_code=500, detail="Translation returned empty text.")

        # Step 2: Synthesize Marathi speech
        tts_result = await synthesize_marathi_speech(marathi_text)

        return TextToSpeechResponse(
            marathi_text=marathi_text,
            audio_base64=tts_result["audio_base64"],
            word_timings=tts_result["word_timings"],
            duration=tts_result["duration"],
            voice=tts_result["voice"],
        )

    except HTTPException:
        raise
    except RuntimeError as e:
        logger.error("Model error in text-to-speech: %s", e)
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error in text-to-speech")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
