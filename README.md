# 🎙️ मराठी-इंग्रजी भाषांतरक — Marathi-English Speech Translator

A **Progressive Web App** (PWA) chatbot that converts:
- 🎙️ **Marathi Speech → English Text** (speak in Marathi, read in English)
- 🔊 **English Text → Marathi Speech** (type English, hear in Marathi with word highlighting)

Built with **AI4Bharat** open-source models:

| Task | Model |
|------|-------|
| Marathi ASR | `ai4bharat/indic-conformer-600m-multilingual` |
| Marathi→English | `ai4bharat/indictrans2-indic-en-dist-200M` |
| English→Marathi | `ai4bharat/indictrans2-en-indic-dist-200M` |
| Marathi TTS | `ai4bharat/indic-parler-tts` |

---

## 🚀 Quick Start

### 1. Get a Hugging Face Token

1. Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Create a **Read** token
3. Accept the AI4Bharat model terms:
   - [indic-conformer-600m-multilingual](https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual)
   - [indictrans2-indic-en-dist-200M](https://huggingface.co/ai4bharat/indictrans2-indic-en-dist-200M)
   - [indictrans2-en-indic-dist-200M](https://huggingface.co/ai4bharat/indictrans2-en-indic-dist-200M)
   - [indic-parler-tts](https://huggingface.co/ai4bharat/indic-parler-tts)

### 2. Configure Backend

```bash
cd backend

# Edit .env — add your HF token:
# HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx
notepad .env
```

### 3. Start Backend

```bash
cd backend
.\start.bat
```

Or manually:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Open Frontend

Open `frontend/index.html` in Chrome/Edge, **or** serve it:

```bash
npx serve frontend/
```

Then open [http://localhost:3000](http://localhost:3000)

---

## 📱 Features

- **Hold-to-speak mic** — Hold the mic button and speak Marathi
- **Live Devanagari transcript** — See your Marathi words appear in real-time as you speak (Chrome)
- **Chatbot UI** — Conversations shown as chat bubbles
- **English translation** — Displayed automatically after Marathi speech
- **TTS playback** — English text gets translated to Marathi and spoken aloud
- **Word highlighting** — Each Marathi word highlights as it's spoken
- **Repeat button** — ↺ to replay any message
- **Voice selection** — 6 Marathi voices: Sunita, Sanjay, Nikhil, Radha, Varun, Isha
- **PWA** — Install on phone/desktop for offline app shell
- **Dark mode** — Premium Maharashtra saffron & dark design

---

## 🗂️ Project Structure

```
language/
├── backend/
│   ├── main.py              FastAPI server
│   ├── requirements.txt     Python dependencies
│   ├── .env                 Configuration (add your HF_TOKEN here)
│   ├── start.bat            Windows startup script
│   └── models/
│       ├── asr.py           Marathi speech recognition
│       ├── translation.py   IndicTrans2 bidirectional translation
│       └── tts.py           Indic Parler-TTS speech synthesis
└── frontend/
    ├── index.html           Main app (open in browser)
    ├── style.css            Premium dark UI styles
    ├── app.js               All frontend logic
    ├── manifest.json        PWA manifest
    └── sw.js                Service worker (offline cache)
```

---

## ⚙️ Configuration

Edit `backend/.env`:

```env
HF_TOKEN=hf_your_token_here    # Required
INFERENCE_MODE=api              # "api" or "local"
TTS_VOICE=Sunita                # Marathi voice
DEVICE=cpu                      # "cpu" or "cuda"
```

**`INFERENCE_MODE=api`** (recommended): Uses Hugging Face Inference API — no local models needed, but rate-limited for free accounts.

**`INFERENCE_MODE=local`**: Downloads and runs models locally — requires ~10 GB disk and NVIDIA GPU for good performance.

---

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/speech-to-text` | Audio file → `{marathi_text, english_text}` |
| `POST` | `/api/text-to-speech` | `{english_text}` → `{marathi_text, audio_base64, word_timings}` |
| `GET`  | `/api/health` | Backend health check |

Interactive docs: `http://localhost:8000/docs`

---

## 🌾 For Maharashtra Farmer Project

This app is designed as a base for AI-powered agricultural advisory:

```
Farmer (Marathi speech)
        ↓
  Marathi → English (ASR + Translation)
        ↓
  Your Crop AI Model (FastAPI)
        ↓
  English → Marathi (Translation + TTS)
        ↓
  Farmer hears crop recommendation in Marathi 🌾
```

To extend: add your crop recommendation logic in `backend/main.py` between the translation and TTS steps.
