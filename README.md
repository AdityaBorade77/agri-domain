# 🎙️ Multilingual Integration — Marathi Voice Assistant for Farmers

A **Progressive Web App** (PWA) voice chatbot for Indian languages, built for
Maharashtra farmers. A farmer speaks in Marathi, an AI answers, and the answer
is read back aloud in Marathi with word-by-word highlighting.

```
Farmer speaks Marathi ──► Speech-to-Text ──► LLM (answers in Marathi) ──► Text-to-Speech ──► Farmer hears answer
```

It also works as a plain translator:

- 🎙️ **Marathi speech → English text**
- 🔊 **English text → Marathi speech** (with word highlighting)

---

## ✨ Features

- **Hold-to-speak mic** with live Devanagari transcript (Chrome / Edge)
- **AI farming assistant** — powered by NVIDIA Nemotron LLMs, replies directly in Marathi
- **Chat history** — conversations are saved locally (SQLite) and can be reopened
- **Marathi TTS** with word highlighting and a ↺ repeat button
- **6 Marathi voices** — Sunita, Sanjay, Nikhil, Radha, Varun, Isha
- **Installable PWA** — works on phone or desktop
- Supports Marathi, Hindi, English, Gujarati, Kannada, Telugu, Tamil, Bengali and Punjabi as reply languages

---

## 🧰 Requirements

| What | Version / Notes |
|------|-----------------|
| **Python** | **3.12** recommended (3.9 – 3.13 work for API mode) |
| **Browser** | Chrome or Edge (needed for the microphone / live transcript) |
| **Hugging Face token** | Free — [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| **NVIDIA API key** | Free — [build.nvidia.com](https://build.nvidia.com) |
| Node.js *(optional)* | Only if you want to serve the frontend with `npx serve` |

---

## 🚀 Setup

### 1. Clone the repository

```bash
git clone https://github.com/AdityaBorade77/Multilingual-Integration.git
cd Multilingual-Integration
```

### 2. Get your API keys

**Hugging Face token** (used for speech recognition, translation and TTS models):

1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) and create a **Read** token.
2. Open each model page below while logged in and click **Agree / Access repository**:
   - [ai4bharat/indic-conformer-600m-multilingual](https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual)
   - [ai4bharat/indictrans2-indic-en-dist-200M](https://huggingface.co/ai4bharat/indictrans2-indic-en-dist-200M)
   - [ai4bharat/indictrans2-en-indic-dist-200M](https://huggingface.co/ai4bharat/indictrans2-en-indic-dist-200M)
   - [ai4bharat/indic-parler-tts](https://huggingface.co/ai4bharat/indic-parler-tts)

**NVIDIA API key** (used for the AI chat answers):

1. Sign in at [build.nvidia.com](https://build.nvidia.com).
2. Open any model page and click **Get API Key**. The key starts with `nvapi-`.

### 3. Create the `.env` file

Copy the example file and put your keys in it:

```bash
# Windows (Command Prompt / PowerShell)
copy backend\.env.example backend\.env

# macOS / Linux
cp backend/.env.example backend/.env
```

Open `backend/.env` and fill in at least these two lines:

```env
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxx
```

> ⚠️ **Never commit `backend/.env`.** It is already listed in `.gitignore`.

### 4. Start the backend

**Windows (easiest):**

```bat
cd backend
start.bat
```

`start.bat` creates a Python 3.12 virtual environment, installs dependencies,
and starts the server. The first run takes a few minutes.

**Manual (Windows / macOS / Linux):**

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend is running when you see `Uvicorn running on http://0.0.0.0:8000`.
Check it at [http://localhost:8000/api/health](http://localhost:8000/api/health)
or browse the interactive API docs at [http://localhost:8000/docs](http://localhost:8000/docs).

> Always start the server from inside the `backend/` folder — the `.env` file
> and the `chat_history.db` database are read from the current directory.

### 5. Open the frontend

Open a **second** terminal in the project folder and run:

```bash
npx serve frontend
```

Then open [http://localhost:3000](http://localhost:3000) in Chrome or Edge.

No Node.js? Use Python instead:

```bash
python -m http.server 3000 --directory frontend
```

You can also double-click `frontend/index.html`, but the microphone and PWA
install work best when served over `http://localhost`.

### 6. Use it

1. Allow microphone access when the browser asks.
2. **Hold** the mic button, speak in Marathi, then release.
3. The assistant replies in text and reads the answer aloud.

If the frontend can't reach the backend, open ⚙️ **Settings** in the app and
check that the API URL is `http://localhost:8000`.

---

## ⚙️ Configuration (`backend/.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `HF_TOKEN` | — | **Required.** Hugging Face read token |
| `NVIDIA_API_KEY` | — | **Required** for AI chat. Key from build.nvidia.com |
| `INFERENCE_MODE` | `api` | `api` = cloud inference (recommended). `local` = run models on your machine |
| `TTS_VOICE` | `Sunita` | `Sunita`, `Sanjay`, `Nikhil`, `Radha`, `Varun`, `Isha` |
| `DEVICE` | `cpu` | `cpu` or `cuda` (only used in `local` mode) |
| `FRONTEND_ORIGIN` | `*` | Allowed CORS origin. Set to your frontend URL in production |
| `LLM_MODEL` | `nvidia/nemotron-3-ultra-550b-a55b` | Primary LLM |
| `LLM_FALLBACK_MODEL` | `nvidia/nemotron-3-super-120b-a12b` | Backup LLM, queried if the primary is slow |
| `LLM_HEDGE_AFTER` | `8` | Seconds to wait before also querying the fallback (first answer wins) |
| `LLM_TIMEOUT` | `40` | Max seconds per LLM call |
| `LLM_MAX_TOKENS` | `600` | Max length of an LLM reply |

> NVIDIA's own Nemotron models usually answer in 3–8 s. Third-party models on
> NVIDIA's free tier (DeepSeek, Gemma, GLM, Kimi) are often queued for minutes.

### Local model mode (optional, advanced)

`INFERENCE_MODE=local` downloads the AI4Bharat models and runs them on your
machine. It needs ~10 GB of disk space and ideally an NVIDIA GPU.

```bash
pip install -r requirements-local.txt
```

Then set `INFERENCE_MODE=local` (and `DEVICE=cuda` if you have a GPU) in `backend/.env`.

---

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/health` | Backend health check and current config |
| `POST` | `/api/speech-to-text` | Audio file → `{marathi_text, english_text}` |
| `POST` | `/api/text-to-speech` | `{english_text}` → `{marathi_text, audio_base64, word_timings}` |
| `POST` | `/api/chat` | Question text → LLM answer in the chosen language |
| `POST` | `/api/chats` | Create a new chat |
| `GET`  | `/api/chats` | List saved chats |
| `GET`  | `/api/chats/{chat_id}/messages` | Messages in a chat |
| `POST` | `/api/chats/{chat_id}/messages` | Save a message to a chat |

Full request/response schemas: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧠 Models Used

| Task | Model |
|------|-------|
| Marathi speech recognition | `ai4bharat/indic-conformer-600m-multilingual` |
| Marathi → English | `ai4bharat/indictrans2-indic-en-dist-200M` |
| English → Marathi | `ai4bharat/indictrans2-en-indic-dist-200M` |
| Marathi TTS | `ai4bharat/indic-parler-tts` |
| Farming assistant (LLM) | NVIDIA Nemotron (via build.nvidia.com) |

---

## 🗂️ Project Structure

```
Multilingual-Integration/
├── backend/
│   ├── main.py                  FastAPI server and all API routes
│   ├── requirements.txt         Python dependencies (API mode)
│   ├── requirements-local.txt   Extra dependencies for local model mode
│   ├── .env.example             Template for your .env (copy → .env)
│   ├── start.bat                One-click Windows setup + start
│   ├── models/
│   │   ├── asr.py               Speech recognition
│   │   ├── translation.py       IndicTrans2 translation
│   │   ├── tts.py               Text-to-speech
│   │   └── db.py                SQLite chat history
│   └── utils/
│       └── text_cleaner.py      Cleans LLM text before translation / TTS
└── frontend/
    ├── index.html               Main app page
    ├── style.css                UI styles
    ├── app.js                   Frontend logic
    ├── manifest.json            PWA manifest
    └── sw.js                    Service worker (offline app shell)
```

Files created at runtime (not in git): `backend/.env`, `backend/venv/`,
`backend/chat_history.db`.

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| `py -3.12` not found when running `start.bat` | Install Python 3.12 from [python.org](https://www.python.org/downloads/) and tick **Add to PATH** |
| `start.bat` stops saying `.env not found` | It copied `.env.example` → `.env` for you. Add your keys to `backend/.env` and run it again |
| `401` / `403` errors from Hugging Face | Check `HF_TOKEN`, and make sure you accepted the terms on **all four** model pages |
| Chat answers fail or time out | Check `NVIDIA_API_KEY`. Keep the default Nemotron models — others are often queued |
| Frontend says backend is offline | Make sure the backend terminal is still running and the app's API URL is `http://localhost:8000` |
| Microphone doesn't work | Use Chrome/Edge, open the app via `http://localhost`, and allow mic access |
| `503` / rate-limit errors in `api` mode | The free Hugging Face Inference API is rate-limited — wait a minute and retry |

---

## 🔐 Security

- API keys live **only** in `backend/.env`, which is gitignored. Never paste them into code, issues or commits.
- If a key is ever leaked, revoke it immediately at
  [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) or
  [build.nvidia.com](https://build.nvidia.com) and create a new one.
