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
API_BASE_URL=http://127.0.0.1:8000
```

Default: `http://127.0.0.1:8000`

## Running the App

Ensure the backend is running first:

```zsh
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Then launch the desktop app:

```zsh
python -m desktop_app.main
```

## Usage

1. Click "Open & Upload Image" to select and upload an image
2. Drag on the source image to select the signature region
3. Adjust threshold slider (0-255) and pick a color
4. Click "Preview" to process the selection
5. Click "Save Result" to save the extracted signature as PNG

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
