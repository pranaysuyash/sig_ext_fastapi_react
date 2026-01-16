"""Backend security validation utilities.

The desktop app already implements strong validation. The backend keeps
similar checks so the upload/extraction endpoints are safe to expose later.
"""

from __future__ import annotations

import re
import uuid
from io import BytesIO
from pathlib import Path

from PIL import Image


class UploadSecurity:
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}
    MAX_IMAGE_WIDTH = 10_000
    MAX_IMAGE_HEIGHT = 10_000
    MAX_PIXELS = 50_000_000  # 50 megapixels

    @staticmethod
    def validate_image_bytes(filename: str, data: bytes) -> None:
        if not filename:
            raise ValueError("Missing filename")

        suffix = Path(filename).suffix.lower()
        if suffix not in UploadSecurity.ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported file extension: {suffix}")

        if not data:
            raise ValueError("File is empty")

        if len(data) > UploadSecurity.MAX_FILE_SIZE:
            raise ValueError("File too large")

        # Magic number validation: PNG exact signature; JPEG universal prefix.
        header = data[:16]
        if header.startswith(b"\x89PNG\r\n\x1a\n"):
            pass
        elif header.startswith(b"\xff\xd8\xff"):
            pass
        else:
            raise ValueError("Invalid image file format (magic number check failed)")

        try:
            with Image.open(BytesIO(data)) as img:
                img.verify()

            with Image.open(BytesIO(data)) as img:
                width, height = img.size
                if width > UploadSecurity.MAX_IMAGE_WIDTH or height > UploadSecurity.MAX_IMAGE_HEIGHT:
                    raise ValueError("Image too large")
                if width * height > UploadSecurity.MAX_PIXELS:
                    raise ValueError("Image has too many pixels")
        except ValueError:
            raise
        except Exception as exc:
            raise ValueError(f"Invalid image file: {exc}") from exc

    @staticmethod
    def validate_session_id(session_id: str) -> str:
        """Return canonical UUID string or raise ValueError."""
        try:
            return str(uuid.UUID(session_id))
        except Exception as exc:
            raise ValueError("Invalid session_id") from exc

    @staticmethod
    def validate_hex_color(color: str) -> str:
        if not isinstance(color, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
            raise ValueError("Invalid color format; expected #RRGGBB")
        return color

    @staticmethod
    def validate_threshold(threshold: int) -> int:
        if not isinstance(threshold, int) or not (0 <= threshold <= 255):
            raise ValueError("Invalid threshold; expected 0-255")
        return threshold

