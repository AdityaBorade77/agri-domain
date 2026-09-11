"""
tts.py — Text-to-Speech: Marathi Text → Marathi Audio
Uses: ai4bharat/indic-parler-tts

Returns: base64-encoded WAV audio + word timing list for frontend highlighting
"""

import os
import io
import logging
import base64
import httpx
import numpy as np

logger = logging.getLogger(__name__)

INFERENCE_MODE = os.getenv("INFERENCE_MODE", "api")
HF_TOKEN = os.getenv("HF_TOKEN", "")
DEVICE = os.getenv("DEVICE", "cpu")
TTS_VOICE = os.getenv("TTS_VOICE", "Sunita")

TTS_MODEL_ID = "ai4bharat/indic-parler-tts"
# router.huggingface.co resolves where api-inference subdomain may be blocked
HF_INFERENCE_URL = f"https://router.huggingface.co/hf-inference/models/{TTS_MODEL_ID}"

# Voice description templates for Indic Parler-TTS
# The model uses a text description to select voice characteristics
VOICE_DESCRIPTIONS = {
    "Sunita": (
        "Sunita's voice is clear and warm with a moderate pace. "
        "The recording is of very high quality, with no background noise."
    ),
    "Sanjay": (
        "Sanjay speaks in a clear, deep male voice at a moderate speed. "
        "The recording is of very high quality, with no background noise."
    ),
    "Nikhil": (
        "Nikhil's voice is clear and confident at a moderate pace. "
        "The recording is of very high quality, with no background noise."
    ),
    "Radha": (
        "Radha speaks with a gentle, warm female voice at a moderate speed. "
        "The recording is of very high quality, with no background noise."
    ),
    "Varun": (
        "Varun's voice is authoritative and clear at a moderate pace. "
        "The recording is of very high quality, with no background noise."
    ),
    "Isha": (
        "Isha speaks with a soft, pleasant female voice at a moderate speed. "
        "The recording is of very high quality, with no background noise."
    ),
}

# ─── Local model (lazy loaded) ────────────────────────────────────────────────
_tts_model = None
_tts_tokenizer = None


def _load_local_tts():
    global _tts_model, _tts_tokenizer
    if _tts_model is not None:
        return
    try:
        import torch
        from transformers import AutoTokenizer
        # Indic Parler TTS uses parler_tts library
        try:
            from parler_tts import ParlerTTSForConditionalGeneration
            logger.info("Loading local TTS model: %s", TTS_MODEL_ID)
            _tts_tokenizer = AutoTokenizer.from_pretrained(TTS_MODEL_ID, token=HF_TOKEN or None)
            _tts_model = ParlerTTSForConditionalGeneration.from_pretrained(
                TTS_MODEL_ID, token=HF_TOKEN or None
            ).to(DEVICE)
            logger.info("TTS model loaded.")
        except ImportError:
            raise RuntimeError(
                "parler_tts not installed. Run: pip install git+https://github.com/huggingface/parler-tts"
            )
    except Exception as e:
        logger.error("Failed to load TTS model: %s", e)
        raise


def _synthesize_local(marathi_text: str) -> bytes:
    """Synthesize speech locally using Parler-TTS."""
    import torch
    import soundfile as sf
    _load_local_tts()

    voice_desc = VOICE_DESCRIPTIONS.get(TTS_VOICE, VOICE_DESCRIPTIONS["Sunita"])
    # Prefix with Marathi language tag
    prompt = f"<mr> {marathi_text}"

    tokenizer = _tts_tokenizer
    model = _tts_model

    input_ids = tokenizer(voice_desc, return_tensors="pt").input_ids.to(DEVICE)
    prompt_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(DEVICE)

    with torch.no_grad():
        generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_ids)

    audio_arr = generation.cpu().numpy().squeeze()
    sample_rate = model.config.sampling_rate

    buf = io.BytesIO()
    sf.write(buf, audio_arr, sample_rate, format="WAV")
    return buf.getvalue()


def _synthesize_api(marathi_text: str) -> bytes:
    """Synthesize speech via gTTS instead of HF Inference API."""
    from gtts import gTTS
    try:
        tts = gTTS(text=marathi_text, lang='mr')
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()
    except Exception as e:
        logger.error("TTS API error: %s", e)
        raise RuntimeError(f"TTS API failed: {e}")


def _estimate_word_timings(marathi_text: str, total_duration_s: float) -> list:
    """
    Estimate word timings based on character count distribution.
    Real forced-alignment would require NeMo/CTC-Segmentation.
    This approximation is good enough for visual highlighting.

    Returns: list of {word, start, end} in seconds
    """
    words = marathi_text.split()
    if not words:
        return []

    # Weight each word by character length (Devanagari chars are variable width)
    char_counts = [max(1, len(w)) for w in words]
    total_chars = sum(char_counts)

    # Add 0.1s leading silence
    current_time = 0.1
    timings = []
    for word, chars in zip(words, char_counts):
        word_duration = (chars / total_chars) * (total_duration_s - 0.2)
        timings.append({
            "word": word,
            "start": round(current_time, 3),
            "end": round(current_time + word_duration, 3),
        })
        current_time += word_duration

    return timings


def _get_audio_duration(audio_bytes: bytes) -> float:
    """Return a rough estimate based on byte length (gTTS outputs MP3)."""
    # mp3 bytes length rough estimation
    return len(audio_bytes) / 4000.0


async def synthesize_marathi_speech(marathi_text: str) -> dict:
    """
    Main entry: convert Marathi text to speech.
    Returns: {audio_base64, sample_rate, word_timings, duration}
    """
    if not marathi_text.strip():
        raise ValueError("Empty text provided.")

    logger.info("Synthesizing TTS for: %.60s...", marathi_text)

    if INFERENCE_MODE == "local":
        audio_bytes = _synthesize_local(marathi_text)
    else:
        audio_bytes = _synthesize_api(marathi_text)

    duration = _get_audio_duration(audio_bytes)
    word_timings = _estimate_word_timings(marathi_text, duration)
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    return {
        "audio_base64": audio_b64,
        "word_timings": word_timings,
        "duration": duration,
        "voice": TTS_VOICE,
    }
