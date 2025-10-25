## Repository snapshot (big picture)

- This project is a two-piece app: a Vite + React frontend (root `src/`, `package.json`) and a FastAPI backend in `backend/app/`.
- Frontend serves the UI and uploads images; backend exposes authentication and extraction APIs under `/auth` and `/extraction`.
- Backend persists data via SQLAlchemy (models in `backend/app/models`) and stores uploaded files under `backend/uploads/` (mounted as `/uploads/images`).

## Key commands & developer workflows

- Frontend (from repository root)

  - Install: `npm install`
  - Run dev server (HMR): `npm run dev` (this runs `vite` per `package.json`).
  - Build for production: `npm run build`

- Backend (run from repo root)
  - Typical dev server (example):
    - `uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000`
    - The app exposes a health endpoint at `/health` useful for smoke tests.
  - Database setup / reset: `python backend/setup_db.py` (drops and recreates tables using SQLAlchemy metadata).
  - Quick verification: `python backend/verify_setup.py` (inspects tables and sample rows).
  - Auth test helper (requires backend running): `python backend/test_auth.py` (connects to DB and hits `/auth/login`).

Notes: there are no npm-style scripts for the backend; use direct Python/uvicorn commands. Tests in `backend/` are small runnable scripts (not pytest suites).

## Important environment & configuration

- `backend/app/config.py` implements settings via `pydantic_settings`. Critical values:
  - `JWT_SECRET` (required) — must be set in environment or `.env` (the code will raise if missing).
  - Database fields: `DATABASE_HOSTNAME`, `DATABASE_PORT`, `DATABASE_USERNAME`, `DATABASE_PASSWORD`, `DATABASE_NAME` — a `DATABASE_URL` property is constructed from them.

Example minimal `.env` for local development (place at repo root):

```text
JWT_SECRET=replace-with-secure-string
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_USERNAME=pranay
DATABASE_PASSWORD=pranay
DATABASE_NAME=signature_extractor
```

## Project-specific conventions & patterns

- Router layout: backend endpoints are split into routers under `backend/app/routers/` — currently `auth.py` and `extraction.py`. They are included in `backend/app/main.py` with prefixes `/auth` and `/extraction`.
- Persistence: SQLAlchemy models live under `backend/app/models/`. CRUD helpers are in `backend/app/crud/` and used by routers.
- Static uploads: `backend/app/main.py` mounts `backend/uploads/images` at `/uploads/images`. When working with file paths reference that folder.
- Frontend <> Backend communication:
  - The frontend uses `src/utils/axiosInstance.js` which defaults to `http://127.0.0.1:8000` and attaches a Bearer token from `localStorage` where available.
  - `axiosInstance` purposely avoids overriding `Content-Type` for FormData uploads — important when debugging file upload failures.

## Integration points & external deps

- PostgreSQL is assumed (SQLAlchemy/psycopg2 usage). Ensure a running Postgres instance matching the `.env` values.
- The frontend relies on Vite (see `vite.config.js`) and modern React libraries (`react`, `react-router-dom`, `react-redux` etc.).

### Desktop frontend option (PyQt/PySide6)

- An alternative desktop GUI can replace the React UI while reusing the same FastAPI backend.
- See detailed spec: `docs/desktop-frontend/pyqt-spec.md` (flows, API contracts, packaging, migration plan).
- Quick dev notes:
  - Suggested layout under `desktop_app/` (entry: `desktop_app/main.py`).
  - Install: `pip install PySide6 requests python-dotenv pillow`
  - Run: `python desktop_app/main.py`
  - API usage mirrors web: /auth/login (form), /extraction/upload (multipart field: file), /extraction/process_image/ (form/query params: session_id, x1, y1, x2, y2, color, threshold).
  - Color must include a leading hash character # to match backend parsing.

## Files to inspect first when changing behavior

- Backend API surface and bootstrapping:

  - `backend/app/main.py` — CORS config, static mount, router includes, `/health` endpoint.
  - `backend/app/config.py` — env-driven settings; validates `JWT_SECRET`.
  - `backend/app/database.py` — SQLAlchemy engine and session (used across app).

- Business logic & persistence:

  - `backend/app/routers/*.py` (auth/extraction) — request/response shapes and route wiring.
  - `backend/app/crud/*` and `backend/app/models/*` — where DB operations and schemas live.

- Frontend:
  - `src/utils/axiosInstance.js` — baseURL, auth header and upload behavior.
  - `src/components/Extraction/` — UI components and dataflow for image upload/extraction.

## Common pitfalls and debugging tips (project-specific)

- Missing `JWT_SECRET` results in startup/config validation problems. Check `backend/app/config.py` logs.
- If file uploads fail with 413/415 or appear empty in backend, ensure the browser request uses `FormData` and `Content-Type` is not overridden — `axiosInstance` contains logic around this.
- If static uploads are not served, confirm `backend/uploads/images` exists and `main.py` mount path (`/uploads/images`) matches frontend requests.
- Tests in `backend/` directly connect to DB (psycopg2). They will fail unless the DB credentials and network are correct and the backend is running for endpoint tests.

## What an agent should do first

1. Check for a `.env` and `backend/app/config.py` values. If `JWT_SECRET` isn't present, prompt the developer or generate a secure secret using `python backend/generate_secret.py`.
2. Start Postgres locally or point `DATABASE_*` envs to a reachable DB.
3. Run `python backend/setup_db.py` to ensure schema is present.
4. Launch the backend via `uvicorn` and the frontend via `npm run dev` and hit `/health`.

## Merging notes

- There was no pre-existing `.github/copilot-instructions.md`. If you have internal agent docs (AGENT.md or similar), add them here and merge important steps — but prefer the concise checklist above.

---

If anything here is unclear or you want more prescriptive run configurations (Docker, systemd, or a Makefile), tell me which environment you run (macOS local, Docker, CI) and I'll add tailored steps.
