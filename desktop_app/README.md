# Desktop App - Signature Extractor

PyQt/PySide6 desktop client for signature extraction. Connects to the FastAPI backend for image processing.

## Features

- Direct image upload (no login required by default)
- Interactive region selection with rubber band
- Real-time threshold and color controls
- Preview extracted signature
- Save result as PNG with transparency

## Installation

Install dependencies:

```zsh
pip install -r desktop_app/requirements.txt
```

Or install individually:

```zsh
pip install PySide6 requests python-dotenv pillow
```

## Configuration

Create a `.env` file in the project root (optional):

```env
API_BASE_URL=http://127.0.0.1:8001
```

Default: `http://127.0.0.1:8001`

## Running the App

Ensure the backend is running first:

```zsh
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8001
```

Then launch the desktop app:

```zsh
python -m desktop_app.main
```

## Usage

1. Open & Upload Image
2. Select region (Selection mode) or Pan (Pan mode)
3. Adjust Threshold (0–255) and Color
4. Preview to process the selection
5. Export/Copy/Save to Library

Viewport controls
- Zoom In/Out, editable Zoom % (supports Fit), Reset Viewport, Rotate
- Clean Viewport clears all panes and the session; Clear Selection only removes the rubber‑band

## Project Structure

```text
desktop_app/
  main.py              # Entry point
  config.py            # Configuration loader
  api/
    client.py          # HTTP API client
  state/
    session.py         # Session state management
  views/
    main_window.py     # Main application window
    login_dialog.py    # Login dialog (optional, commented out)
  widgets/
    image_view.py      # Image viewer with region selection
```

## Notes

- Login/authentication is optional and currently disabled
- Requires running FastAPI backend
- Color format must include leading # (e.g., #000000 for black)
- Selection coordinates are automatically clamped to image bounds
