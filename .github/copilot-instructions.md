## Repository snapshot (big picture)

- This project is a **desktop-first signature extraction tool** with a PySide6/Qt frontend and FastAPI backend.
- **Desktop app** is in `desktop_app/` (entry: `desktop_app/main.py`); backend is in `backend/app/`.
- Backend exposes authentication and extraction APIs under `/auth` and `/extraction`.
- Backend persists data via SQLAlchemy (models in `backend/app/models`) and stores uploaded files under `backend/uploads/`.
- **Note**: The React/Vite web frontend has been **completely removed** — this is now a desktop-only application.

## Key commands & developer workflows

- **Desktop App** (from repository root)
  - Install dependencies: `pip install PySide6 requests python-dotenv pillow opencv-python numpy`
  - Run: `python -m desktop_app.main`
  - The app connects to the backend at `http://127.0.0.1:8001` by default

- **Backend** (run from repo root)
  - Typical dev server:
    - `uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8001`
    - The app exposes a health endpoint at `/health` useful for smoke tests.
  - Database setup / reset: `python backend/setup_db.py` (drops and recreates tables using SQLAlchemy metadata).
  - Quick verification: `python backend/verify_setup.py` (inspects tables and sample rows).
  - Auth test helper (requires backend running): `python backend/test_auth.py` (connects to DB and hits `/auth/login`).

Notes: Tests in `backend/` are small runnable scripts (not pytest suites).

## Important environment & configuration

- `backend/app/config.py` implements settings via `pydantic_settings`. Critical values:
  - `JWT_SECRET` (required) — must be set in environment or `.env` (the code will raise if missing).
  - Database fields: `DATABASE_HOSTNAME`, `DATABASE_PORT`, `DATABASE_USERNAME`, `DATABASE_PASSWORD`, `DATABASE_NAME` — a `DATABASE_URL` property is constructed from them.

Example minimal `.env` for local development (place at repo root):

```text
JWT_SECRET=replace-with-secure-string

# SQLite (default, recommended for desktop app):
DATABASE_URL=sqlite:///backend/data/app.db

# OR PostgreSQL (optional):
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_USERNAME=pranay
DATABASE_PASSWORD=pranay
DATABASE_NAME=signature_extractor
```

## Project-specific conventions & patterns

- **Router layout**: backend endpoints are split into routers under `backend/app/routers/` — currently `auth.py` and `extraction.py`. They are included in `backend/app/main.py` with prefixes `/auth` and `/extraction`.
- **Persistence**: SQLAlchemy models live under `backend/app/models/`. CRUD helpers are in `backend/app/crud/` and used by routers.
- **Static uploads**: `backend/app/main.py` mounts `backend/uploads/images` at `/uploads/images`. When working with file paths reference that folder.
- **Desktop <> Backend communication**:
  - The desktop app uses `desktop_app/api/client.py` (ApiClient) which connects to `http://127.0.0.1:8001` by default.
  - API usage: `/auth/login` (form), `/extraction/upload` (multipart field: file), `/extraction/process_image/` (form/query params: session_id, x1, y1, x2, y2, color, threshold).
  - Color must include a leading hash character # to match backend parsing.

## Integration points & external deps

- **Database**: SQLite by default (no setup needed); PostgreSQL optional (SQLAlchemy/psycopg2 usage).
- **Desktop app**: PySide6/Qt6 for GUI; PIL/Pillow for image handling; requests for HTTP client.
- **Backend**: FastAPI, SQLAlchemy, OpenCV, NumPy for image processing.

## Files to inspect first when changing behavior

- **Backend API surface and bootstrapping:**
  - `backend/app/main.py` — CORS config, static mount, router includes, `/health` endpoint.
  - `backend/app/config.py` — env-driven settings; validates `JWT_SECRET`.
  - `backend/app/database.py` — SQLAlchemy engine and session (used across app).

- **Business logic & persistence:**
  - `backend/app/routers/*.py` (auth/extraction) — request/response shapes and route wiring.
  - `backend/app/crud/*` and `backend/app/models/*` — where DB operations and schemas live.

- **Desktop UI:**
  - `desktop_app/main.py` — Application entry point and initialization.
  - `desktop_app/views/main_window.py` — Main UI window, controls, and event handlers.
  - `desktop_app/widgets/image_view.py` — Image display widget with zoom/pan/selection.
  - `desktop_app/api/client.py` — Backend API client (upload, process, etc.).
  - `desktop_app/state/session.py` — Session state management.

## Common pitfalls and debugging tips (project-specific)

- Missing `JWT_SECRET` results in startup/config validation problems. Check `backend/app/config.py` logs.
- If file uploads fail with 413/415 or appear empty in backend, ensure the request uses proper `multipart/form-data` with the `file` field.
- If static uploads are not served, confirm `backend/uploads/images` exists and `main.py` mount path (`/uploads/images`) is correct.
- Tests in `backend/` directly connect to DB. They will fail unless the DB credentials and network are correct and the backend is running for endpoint tests.
- Desktop app expects backend at `http://127.0.0.1:8001` by default — ensure backend is running on port 8001 (not 8000).

## What an agent should do first

1. Check for a `.env` and `backend/app/config.py` values. If `JWT_SECRET` isn't present, generate a secure secret using `python backend/generate_secret.py`.
2. Decide on database: SQLite (default, zero-config) or PostgreSQL (set `DATABASE_*` envs).
3. Run `python backend/setup_db.py` to ensure schema is present.
4. Launch the backend via `uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8001` and verify `/health` endpoint.
5. Launch the desktop app via `python -m desktop_app.main`.

## Merging notes

- The React/Vite web frontend was removed in October 2025. All references to `src/`, `package.json`, `vite.config.js`, `index.html` etc. are stale.
- This is now a desktop-first application using PySide6/Qt6.
- If you see instructions mentioning npm, React, or Vite, they are outdated.

---

If anything here is unclear or you want more prescriptive run configurations (Docker, systemd, or a Makefile), tell me which environment you run (macOS local, Docker, CI) and I'll add tailored steps.
