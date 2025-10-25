# Signature Extractor App

FastAPI backend with a pluggable frontend. The current web UI is React (Vite), and there is an optional desktop UI using PyQt/PySide6 that reuses the same backend APIs.

## Backend quickstart

1. Create a `.env` at repo root with at least:

```env
JWT_SECRET=replace-with-secure-string
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_USERNAME=pranay
DATABASE_PASSWORD=pranay
DATABASE_NAME=signature_extractor
```

1. Initialize DB and run server:

```zsh
python backend/setup_db.py
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Health check: <http://127.0.0.1:8000/health>

## Web frontend (React)

```zsh
npm install
npm run dev
```

## Desktop frontend (PyQt/PySide6)

See detailed spec and plan in `docs/desktop-frontend/pyqt-spec.md`.

Quick run (once code exists under `desktop_app/`):

```zsh
python -m pip install --upgrade pip
pip install PySide6 requests python-dotenv pillow
python desktop_app/main.py
```
