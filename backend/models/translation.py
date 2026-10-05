"""
translation.py — Bidirectional Translation
Marathi ↔ English using AI4Bharat IndicTrans2

Models:
  Marathi→English: ai4bharat/indictrans2-indic-en-dist-200M
  English→Marathi: ai4bharat/indictrans2-en-indic-dist-200M
"""

import os
import asyncio
import logging
import httpx

from utils.text_cleaner import clean_for_translation

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
_ip = None


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
            model_id, token=HF_TOKEN or None, trust_remote_code=True
        )
        _models[direction] = AutoModelForSeq2SeqLM.from_pretrained(
            model_id, token=HF_TOKEN or None, trust_remote_code=True
        ).to(DEVICE)
        _models[direction].eval()
        logger.info("Translation model %s loaded.", direction)
    except Exception as e:
        logger.error("Failed to load translation model (%s): %s", direction, e)
        raise


def _translate_local(text: str, direction: str) -> str:
    """Translate using locally loaded IndicTrans2 model."""
    global _ip
    import torch
    from IndicTransToolkit import IndicProcessor
    if _ip is None:
        _ip = IndicProcessor(inference=True)

    _load_local_translation(direction)

    src_lang = LANG_MR if direction == "mr2en" else LANG_EN
    tgt_lang = LANG_EN if direction == "mr2en" else LANG_MR

    tokenizer = _tokenizers[direction]
    model = _models[direction]

    batch = _ip.preprocess_batch([text], src_lang=src_lang, tgt_lang=tgt_lang)
    inputs = tokenizer(batch, return_tensors="pt", padding=True).to(DEVICE)

    with torch.no_grad():
        generated = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_lang) if not hasattr(tokenizer, 'lang_code_to_id') else tokenizer.lang_code_to_id[tgt_lang],
            max_length=256,
        )

    translated = tokenizer.batch_decode(generated, skip_special_tokens=True)
    postprocessed = _ip.postprocess_batch(translated, lang=tgt_lang)
    return postprocessed[0].strip()


def _translate_api(text: str, model_id: str, src_lang: str, tgt_lang: str) -> str:
    """Translate via Google Translate (one request, up to 5000 chars).

    Falls back to MyMemory, which is slower and capped at ~5000 chars/day
    on the anonymous free tier.
    """
    from deep_translator import GoogleTranslator, MyMemoryTranslator

    g_src = 'mr' if src_lang == LANG_MR else 'en'
    g_tgt = 'mr' if tgt_lang == LANG_MR else 'en'
    try:
        return GoogleTranslator(source=g_src, target=g_tgt).translate(text[:4900]) or text
    except Exception as e:
        logger.warning("Google translation failed (%s); falling back to MyMemory", e)

    try:
        mm_src = 'mr-IN' if g_src == 'mr' else 'en-US'
        mm_tgt = 'mr-IN' if g_tgt == 'mr' else 'en-US'
        return MyMemoryTranslator(source=mm_src, target=mm_tgt).translate(text[:450]) or text
    except Exception as e:
        logger.error("Translation API error: %s", e)
        raise RuntimeError(f"Translation API failed: {e}")


async def translate_marathi_to_english(marathi_text: str) -> str:
    """Translate Marathi text → English text."""
    if not marathi_text.strip():
        return ""
    logger.info("Translating MR→EN: %.60s...", marathi_text)
    if INFERENCE_MODE == "local":
        return await asyncio.to_thread(_translate_local, marathi_text, "mr2en")
    else:
        return await asyncio.to_thread(_translate_api, marathi_text, MODEL_MR_TO_EN, LANG_MR, LANG_EN)


async def translate_english_to_marathi(english_text: str) -> str:
    """Translate English text → Marathi text.

    The text is cleaned (markdown stripped, emojis removed, whitespace
    normalised) before being sent to the translation API so that formatting
    noise does not confuse the translation model.
    """
    if not english_text or not english_text.strip():
        return ""

    # ── Clean LLM output before it reaches the translation API ───────────
    cleaned_text = clean_for_translation(english_text)
    logger.info("Cleaned EN text (%.60s...) → sending to translation", cleaned_text)

    if not cleaned_text.strip():
        logger.warning("clean_for_translation() returned empty string; falling back to original.")
        cleaned_text = english_text.strip()

    logger.info("Translating EN→MR: %.60s...", cleaned_text)
    if INFERENCE_MODE == "local":
        return await asyncio.to_thread(_translate_local, cleaned_text, "en2mr")
    else:
        return await asyncio.to_thread(_translate_api, cleaned_text, MODEL_EN_TO_MR, LANG_EN, LANG_MR)
