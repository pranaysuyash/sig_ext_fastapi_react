# Desktop Frontend (PyQt/PySide6) Specification

This document proposes a desktop GUI replacement for the current React frontend using PySide6 (Qt for Python). The backend FastAPI service and PostgreSQL database remain unchanged.

## Overview

- Keep FastAPI backend as-is (auth + extraction) and build a cross-platform desktop client.
- Two run modes:
  1. Client-server (recommended): Desktop app talks to running FastAPI over HTTP.
  2. Bundled: Optional second phase where the desktop app can start FastAPI in a background process for an all-in-one experience.

## User flows

### 1) Login

- Inputs: email, password.
- Call POST /auth/login with OAuth2PasswordRequestForm fields: username, password.
- Store JWT in memory (optionally OS keyring); attach as Bearer to subsequent calls.
- Store JWT in memory (optionally OS keyring); attach as Bearer to subsequent calls.

### 2) Upload image

- Open file dialog, select PNG/JPG.
- Call POST /extraction/upload as multipart/form-data with field `file`.
- Response JSON: { id: string (UUID), filename: string, file_path: "/uploads/images/{id}.png" }.
- Save `id` as session_id for future processing.
- Save `id` as session_id for future processing.

### 3) Select region and preview

- Display image preview; user draws rectangle (x1,y1,x2,y2) using QRubberBand over QGraphicsView.
- Controls: Threshold slider (0–255), Color picker (hex, e.g. #000000 for black).
- Call POST /extraction/process_image/ with fields: session_id, x1, y1, x2, y2, color, threshold.
- Receives PNG stream (image/png). Render in preview panel.
- Receives PNG stream (image/png). Render in preview panel.

### 4) Save result

- Save previewed result as PNG with alpha via QFileDialog.
- Optional: Copy to clipboard.

## API contracts (backend already implemented)

- POST /auth/login

  - Content-Type: application/x-www-form-urlencoded
  - Body: username, password
  - Response: { access_token, token_type }

- POST /extraction/upload

  - Content-Type: multipart/form-data (field `file`)
  - Response: { id, filename, file_path }

- POST /extraction/process_image/
  - Params/Form fields: session_id: str (UUID), x1: int, y1: int, x2: int, y2: int, color: str ("#RRGGBB"), threshold: int (0–255)
  - Response: image/png stream

Notes

- Color string must start with `#`; backend slices indexes 1,3,5 to parse hex.
- Coordinates should be clamped to the actual image size (backend performs guard checks as well).

## Project layout (proposed)

```text
desktop_app/
  main.py                   # Entry point (QtApplication)
  config.py                 # API base URL, env loading
  api/
    client.py               # Tiny HTTP wrapper (requests) with JWT handling
  views/
    login_dialog.py         # QDialog for login
    main_window.py          # QMainWindow; left: controls, right: image views
  widgets/
    image_view.py           # QGraphicsView + QRubberBand for cropping
    color_picker.py         # QColorDialog wrapper + hex sync
  state/
    session.py              # Holds access_token, session_id, last request params
  resources/                # icons, qss
  requirements.txt          # PySide6, requests, python-dotenv, pillow
```

## Key components

- api/client.py

  - Methods: login(username, password) -> token; upload_image(path) -> {id, filename, file_path};
    process_image(params) -> bytes (PNG)
  - Adds Authorization: Bearer {token} header when token present

- widgets/image_view.py

  - Loads QImage from file_path URL (optionally via GET, or from local selection)
  - Supports zoom/pan and rectangle selection; emits selectionChanged(x1,y1,x2,y2)

- views/main_window.py
  - Controls: file picker, threshold slider, color picker, preview button, save button
  - Binds to client methods; displays returned PNG in a QLabel/QGraphicsView

## Configuration

- API base URL from environment: VITE_API_URL equivalent
  - `.env` (root): API_BASE_URL=`http://127.0.0.1:8000`
  - Fallback: `http://127.0.0.1:8000`

## Error handling

- Map common HTTP status to user messages:
  - 401: clear token and show Login dialog
  - 403: show "Permission denied"
  - 404: show "File not found" for session/image
  - 413/415: show file too large/unsupported type
  - 422: show validation errors
  - 500: show generic server error with details

## Logging & diagnostics

- Console logging by default; optional rotating file handler in `desktop_app/logs/app.log`.
- Add a Help > Diagnostics menu to open logs and test `/health`.

## Build & run (macOS zsh examples)

```zsh
# Create venv and install deps
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install PySide6 requests python-dotenv pillow

# Run desktop app (assuming desktop_app/main.py exists)
python desktop_app/main.py
```

Packaging (optional)

```zsh
pip install pyinstaller
pyinstaller --noconfirm --windowed --name "Signature Extractor" desktop_app/main.py
```

## Migration plan

Phase 1 (parallel):

- Implement `desktop_app` skeleton and minimal login + upload + preview flow.
- Keep React frontend working for continuity.
- Dogfood desktop app; gather feedback.

Phase 2 (consolidation):

- Reach UI parity (crop, threshold, color, save) with web UI.
- Optional: add in-app backend launcher for single-binary distribution.
- Deprecate or archive React UI if desired.

## Acceptance criteria

- Can login, upload, crop-select, preview, and save PNG result using existing FastAPI.
- Handles large files gracefully with progress and errors surfaced to user.
- Minimal footprint and simple packaging for macOS (works on Apple Silicon).
