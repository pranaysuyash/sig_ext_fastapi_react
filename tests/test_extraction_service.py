from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path

import cv2
import numpy as np
import pytest
from PIL import Image

from backend.app.services.extraction import (
    build_selection_metadata,
    normalize_crop_bounds,
    persist_selection_metadata,
    render_signature_png,
    resolve_upload_path,
)


def _write_test_image(path: Path, *, width: int = 24, height: int = 18) -> None:
    image = np.full((height, width, 3), 80, dtype=np.uint8)
    image[4:12, 5:15] = 255
    cv2.imwrite(str(path), image)


def test_normalize_crop_bounds_clamps_and_rejects_zero_area():
    assert normalize_crop_bounds(100, 80, -5, 10, 20, 90) == (0, 10, 20, 80)

    with pytest.raises(ValueError, match="area is zero"):
        normalize_crop_bounds(10, 10, 4, 4, 4, 8)


def test_resolve_upload_path_prefers_direct_png(tmp_path):
    session_id = "12345678-1234-5678-1234-567812345678"
    image_path = tmp_path / f"{session_id}.png"
    _write_test_image(image_path)

    assert resolve_upload_path(session_id, tmp_path) == image_path


def test_resolve_upload_path_rejects_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        resolve_upload_path("12345678-1234-5678-1234-567812345678", tmp_path)


def test_persist_selection_metadata_round_trips(tmp_path):
    payload = build_selection_metadata(
        "12345678-1234-5678-1234-567812345678",
        width=20,
        height=10,
        x1=1,
        y1=2,
        x2=8,
        y2=9,
        threshold=128,
        color="#000000",
    )

    metadata_path = persist_selection_metadata(tmp_path, "session-abc", payload)
    assert metadata_path.exists()
    assert json.loads(metadata_path.read_text(encoding="utf-8")) == payload


def test_render_signature_png_produces_png_bytes(tmp_path):
    image_path = tmp_path / "source.png"
    _write_test_image(image_path)

    output = render_signature_png(
        image_path,
        x1=4,
        y1=3,
        x2=16,
        y2=13,
        color="#112233",
        threshold=100,
    )

    assert isinstance(output, BytesIO)
    assert output.getvalue().startswith(b"\x89PNG\r\n\x1a\n")

    output.seek(0)
    rendered = Image.open(output)
    assert rendered.size == (12, 10)
    assert rendered.mode == "RGBA"
