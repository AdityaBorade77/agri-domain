"""
translation.py — Bidirectional Translation
Marathi ↔ English using AI4Bharat IndicTrans2

Models:
  Marathi→English: ai4bharat/indictrans2-indic-en-dist-200M
  English→Marathi: ai4bharat/indictrans2-en-indic-dist-200M
"""

import os
import logging
import httpx

logger = logging.getLogger(__name__)

INFERENCE_MODE = os.getenv("INFERENCE_MODE", "api")
HF_TOKEN = os.getenv("HF_TOKEN", "")
DEVICE = os.getenv("DEVICE", "cpu")

MODEL_MR_TO_EN = "ai4bharat/indictrans2-indic-en-dist-200M"
MODEL_EN_TO_MR = "ai4bharat/indictrans2-en-indic-dist-200M"

# ─── IndicTrans2 language codes ───────────────────────────────────────────────
# IndicTrans2 uses ISO 639-1 BCP-47 style codes
LANG_MR = "mar_Deva"  # Marathi Devanagari
LANG_EN = "eng_Latn"  # English Latin

# ─── Local model (lazy loaded) ────────────────────────────────────────────────
_models = {}
_tokenizers = {}


def _load_local_translation(direction: str):
    """direction: 'mr2en' or 'en2mr'"""
    if direction in _models:
        return
    try:
        import torch
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        model_id = MODEL_MR_TO_EN if direction == "mr2en" else MODEL_EN_TO_MR
        logger.info("Loading translation model: %s", model_id)
        _tokenizers[direction] = AutoTokenizer.from_pretrained(
            model_id, token=HF_TOKEN or None
        )
        _models[direction] = AutoModelForSeq2SeqLM.from_pretrained(
            model_id, token=HF_TOKEN or None
        ).to(DEVICE)
        _models[direction].eval()
        logger.info("Translation model %s loaded.", direction)
    except Exception as e:
        logger.error("Failed to load translation model (%s): %s", direction, e)
        raise


def _translate_local(text: str, direction: str) -> str:
    """Translate using locally loaded IndicTrans2 model."""
    import torch
    _load_local_translation(direction)

    src_lang = LANG_MR if direction == "mr2en" else LANG_EN
    tgt_lang = LANG_EN if direction == "mr2en" else LANG_MR

    tokenizer = _tokenizers[direction]
    model = _models[direction]

    tokenizer.src_lang = src_lang
    inputs = tokenizer(text, return_tensors="pt", padding=True).to(DEVICE)

    with torch.no_grad():
        generated = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.lang_code_to_id[tgt_lang],
            max_length=256,
        )

    translated = tokenizer.batch_decode(generated, skip_special_tokens=True)
    return translated[0].strip()


def _translate_api(text: str, model_id: str, src_lang: str, tgt_lang: str) -> str:
    """Translate via MyMemoryTranslator since HF models are not supported by the free inference API."""
    from deep_translator import MyMemoryTranslator
    # deep-translator MyMemory requires specific codes
    g_src = 'mr-IN' if src_lang == 'mar_Deva' else 'en-US'
    g_tgt = 'mr-IN' if tgt_lang == 'mar_Deva' else 'en-US'
    try:
        translated = MyMemoryTranslator(source=g_src, target=g_tgt).translate(text)
        return translated if translated else text
    except Exception as e:
        logger.error("Translation API error: %s", e)
        raise RuntimeError(f"Translation API failed: {e}")


async def translate_marathi_to_english(marathi_text: str) -> str:
    """Translate Marathi text → English text."""
    if not marathi_text.strip():
        return ""
    logger.info("Translating MR→EN: %.60s...", marathi_text)
    if INFERENCE_MODE == "local":
        return _translate_local(marathi_text, "mr2en")
    else:
        return _translate_api(marathi_text, MODEL_MR_TO_EN, LANG_MR, LANG_EN)


async def translate_english_to_marathi(english_text: str) -> str:
    """Translate English text → Marathi text."""
    if not english_text.strip():
        return ""
    logger.info("Translating EN→MR: %.60s...", english_text)
    if INFERENCE_MODE == "local":
        return _translate_local(english_text, "en2mr")
    else:
        return _translate_api(english_text, MODEL_EN_TO_MR, LANG_EN, LANG_MR)
