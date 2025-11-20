## Quick repository snapshot (big picture)

- Desktop-first application with a PySide6 (Qt) GUI and a FastAPI backend used for optional cloud features.
- Desktop frontend: `desktop_app/` (entry: `desktop_app/main.py`). Backend: `backend/app/` (entry: `backend/app/main.py`).
- Backend provides authentication and image extraction APIs under `/auth` and `/extraction` and serves uploaded images under `/uploads/images`.

## High-level architecture & why it matters

- Hybrid offline-first design: the desktop app starts an embedded or subprocess backend (see `desktop_app/backend_manager.py`) to enable cloud features while remaining functional offline using local extraction logic (`desktop_app/processing/extractor.py`).
- Local processing is the preferred fast path — `SignatureExtractor` has robust input validation and resource limits to prevent malicious files and DoS (magic numbers, size limits, PIL verify, path sanitization).
- Backend uses SQLAlchemy with optional Postgres; SQLite is used as a default fallback when `DATABASE_URL` is not set.

## Practical developer tasks and commands

- Run desktop app (dev):
  - `python -m desktop_app.main` (the app will auto-start the backend on an available port)
- Run backend (dev):
  - `uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8001`
- Initialize or reset the DB (dev):
  - `python backend/setup_db.py` (creates/drops tables using SQLAlchemy models)
- Generate secure JWT_SECRET (if needed):
  - `python backend/generate_secret.py` (prints a 32-byte hex key — add to your `.env`)
- Small integration tests (scripts in `backend/`):
  - `python backend/test_auth.py` — generates `test_token.txt` for further tests (requires DB and backend running)
  - `python backend/test_upload.py` — exercises `/extraction/upload` using the test token

## Configuration & environment notes

- Key settings and `.env`: `backend/app/config.py` expects `JWT_SECRET` (required). Use `.env` at repo root or export env vars. Example: `DATABASE_URL=sqlite:///backend/data/app.db` and `JWT_SECRET=<secure value>`.
- Desktop config loader: `desktop_app/config.py` reads `.env` and validates `API_BASE_URL` and `UPDATES_URL`. Default API base URL: `http://127.0.0.1:8001`.

## Project-specific code patterns and conventions

- API endpoints in `backend/app/routers/` use FastAPI routers included in `backend/app/main.py`.
- Uploads mount and path: backend creates a user-writable `uploads/images` directory and serves it under `/uploads/images`. See `UPLOADS_DIR` usage in `backend/app/routers/extraction.py`.
- Desktop backend management: `desktop_app/backend_manager.py` dynamically finds uvicorn or the backend script and starts it, falling back to an in-process server when packaged.
- Client & session lifecycle: `desktop_app/api/client.py` stores `session_id` and `last_request` in `desktop_app/state/session.py` which is the single-session state object shared across the app.
- Local processing implementation: `desktop_app/processing/extractor.py` is the offline extraction engine. Prefer it for offline-first behavior. It implements strong security checks (magic numbers, size/dimension limits, PIL validation) and robust session handling.

## Integration & security notes

- Local vs backend processing: Desktop `MainWindow` prefers `SignatureExtractor` for immediate, offline processing. The backend `process_image` mirrors its behavior — keep both implementations in sync for feature parity.
- Security: Validate `JWT_SECRET` and DB credentials; if using packaged app, `BackendManager` will persist a JWT secret in user data dir and default to SQLite to keep things robust.
- File uploads: Backend `/extraction/upload` expects `multipart/form-data` with a `file` field — desktop `ApiClient.upload_image()` does this correctly.

## Build, packaging, and tests

- Packaging: Use `build-tools/build.py` (PyInstaller wrapper) or native spec files under `build-tools/` to create platform-specific builds. The script includes helper options (`--one-file`, `--debug`, `--console`, `--create-scripts`).
- PDF features: The desktop app optionally uses `pypdfium2` and `pikepdf`. If you need PDF features, ensure these dependencies are installed; otherwise the `PdfTab` features will be disabled with a helpful message.
- Tests: Backend has runnable scripts under `backend/` (not pytest suites). Use these scripts for quick integration checks when backend and DB are running.

## Where to start for common changes

- Fix backend APIs: check `backend/app/routers/__init__.py`, `backend/app/routers/extraction.py`, `backend/app/routers/auth.py`, and `backend/app/main.py`.
- Fix client or UI behavior: `desktop_app/api/client.py`, `desktop_app/views/*`, and `desktop_app/main.py`.
- Update security or processing: `desktop_app/processing/extractor.py` and `backend/app/routers/extraction.py` (mirror logic).
- Packaging & build tweaks: `build-tools/build.py` and spec files in `build-tools/`.

If you'd like, I can add CI steps, Docker dev containers, or a Makefile to codify common runs (backend start, setup DB, run desktop app) — tell me which you prefer.
