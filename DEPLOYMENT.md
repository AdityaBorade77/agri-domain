# Kisan AI Deployment Guide

## Deploy Frontend to Vercel via GitHub

### Prerequisites
- A GitHub account (github.com)
- A Vercel account (vercel.com — free tier works)

---

## Step 1: Push to GitHub

Open a terminal in the project root and run:

```bash
git add .
git commit -m "feat: Kisan AI frontend redesign with Kisan Earth design system"
git remote add origin https://github.com/YOUR_USERNAME/kisan-ai.git
git push -u origin main
```

---

## Step 2: Deploy on Vercel

1. Go to vercel.com/new
2. Click "Import Git Repository"
3. Connect GitHub and select your kisan-ai repository
4. Vercel will auto-detect the vercel.json config
5. Leave "Root Directory" as-is — the vercel.json handles routing from frontend/
6. Click "Deploy"

Vercel gives you a URL like: https://kisan-ai.vercel.app

---

## Step 3: Set Environment Variables

On Vercel Dashboard → Your Project → Settings → Environment Variables:

- VITE_API_URL = https://your-backend-url.com

The frontend uses the API URL from the Settings modal (stored in localStorage).
For production, users set their backend URL in the voice assistant settings.

---

## Alternative: Vercel CLI

```bash
npm install -g vercel
cd "d:\web dev\language - Copy"
vercel
```

Follow the prompts. Choose your scope, name it "kisan-ai", deploy from root (./), and done.

---

## Project Structure

```
language - Copy/
├── vercel.json        -- Vercel routing config (serves frontend/)
├── DEPLOYMENT.md      -- This file
├── frontend/
│   ├── index.html     -- Main SPA entry point
│   ├── style.css      -- Kisan Earth design system
│   ├── kisan-app.js   -- SPA router + UI logic
│   ├── app.js         -- Backend API client
│   ├── manifest.json  -- PWA manifest
│   └── sw.js          -- Service worker
└── backend/           -- Python backend (NOT deployed to Vercel)
```

NOTE: The Python backend is NOT deployed to Vercel.
Deploy backend separately on Railway, Render, or Google Cloud Run.

---

## Custom Domain (Optional)

1. Vercel Dashboard → Your Project → Domains
2. Add your domain (e.g., kisanai.in)
3. Update DNS records as shown by Vercel
