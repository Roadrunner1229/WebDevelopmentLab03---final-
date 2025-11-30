
# Lab03 — Streamlit Multi-Page App (Starter)

## Run locally
```
pip install -r requirements.txt
streamlit run "Home_Page.py"
```

## Deploy
1. Push this folder to a public GitHub repo.
2. On Streamlit Community Cloud, create a new app from the repo.
3. Set an environment variable `GEMINI_API_KEY` for Phases 3 & 4.
4. App will auto-discover pages in the `pages/` folder.

## Notes
- Phase 2 uses Open-Meteo (no API key). You can swap to any other API if you prefer.
- Phase 3/4 use google-generativeai; keep try/except to prevent crashes.
