import io
import json
import logging
import os
from pathlib import Path
from typing import Optional

import pytest
import requests
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8001")


def _ensure_test_image(image_path: Path) -> Path:
    """Create a simple image so uploads have deterministic content."""
    if not image_path.exists():
        img = Image.new("RGB", (100, 100), color="red")
        img.save(image_path)
        logger.info("Created test image: %s", image_path)
    return image_path

def _load_token(token_path: Path) -> Optional[str]:
    try:
        with token_path.open("r", encoding="utf-8") as token_file:
            token_data = json.load(token_file)
            return token_data.get("access_token")
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        pytest.fail(f"Malformed token file {token_path}: {exc}")


def test_upload():
    """Exercise the upload endpoint end-to-end when prerequisites are available."""
    token_path = Path("test_token.txt")
    token = _load_token(token_path)
    if not token:
        pytest.skip("No token found. Run backend/test_auth.py to generate test_token.txt.")

    image_path = _ensure_test_image(Path("test_image.jpg"))
    headers = {"Authorization": f"Bearer {token}"}

    logger.info("Sending upload request to %s/extraction/upload", BASE_URL)
    try:
        with image_path.open("rb") as image_handle:
            response = requests.post(
                f"{BASE_URL}/extraction/upload",
                headers=headers,
                files={"file": ("test_image.jpg", image_handle, "image/jpeg")},
                timeout=10,
            )
    except requests.exceptions.RequestException as exc:
        pytest.skip(f"Upload endpoint unavailable: {exc}")

    logger.info("Upload response code: %s", response.status_code)
    logger.debug("Upload response headers: %s", response.headers)
    logger.debug("Upload response body: %s", response.text)

    assert response.status_code == 200, f"Upload failed: {response.status_code} {response.text}"


if __name__ == "__main__":
    test_upload()
