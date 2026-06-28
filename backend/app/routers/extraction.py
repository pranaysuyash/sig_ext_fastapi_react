
# extraction.py

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from backend.app.database import get_db
from fastapi.responses import StreamingResponse
from io import BytesIO
from pathlib import Path
from PIL import Image
import numpy as np
import json
import cv2
import logging
import uuid
import os
import traceback
from pydantic import BaseModel, Field
from typing import Tuple

from backend.app.paths import UPLOADS_DIR
from backend.app.security import UploadSecurity

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

router = APIRouter(tags=["Extraction"])


# Ensure the uploads directory exists
os.makedirs(str(UPLOADS_DIR), exist_ok=True)


# Ensure the per-session region metadata directory exists
REGION_METADATA_DIR = Path(str(UPLOADS_DIR)) / "regions"
REGION_METADATA_DIR.mkdir(parents=True, exist_ok=True)


class RegionSelectionRequest(BaseModel):
    session_id: str = Field(..., min_length=1, description="Session ID returned by upload")
    x1: int = Field(..., ge=0)
    y1: int = Field(..., ge=0)
    x2: int = Field(..., ge=0)
    y2: int = Field(..., ge=0)
    color: str = Field(..., min_length=7, max_length=7)
    threshold: int = Field(..., ge=0, le=255)


def _resolve_upload_path(session_id: str) -> str:
    """Resolve uploaded file by session id with legacy-compatible behavior."""
    session_id = UploadSecurity.validate_session_id(session_id)

    direct_png = Path(str(UPLOADS_DIR)) / f"{session_id}.png"
    if direct_png.exists():
        return str(direct_png)

    for extension in sorted(UploadSecurity.ALLOWED_EXTENSIONS):
        candidate = Path(str(UPLOADS_DIR)) / f"{session_id}{extension}"
        if candidate.exists():
            return str(candidate)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Image file not found."
    )


def _normalize_crop_bounds(
    width: int,
    height: int,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
) -> Tuple[int, int, int, int]:
    start_x, end_x = sorted((x1, x2))
    start_y, end_y = sorted((y1, y2))
    start_x = max(0, min(start_x, width))
    end_x = max(0, min(end_x, width))
    start_y = max(0, min(start_y, height))
    end_y = max(0, min(end_y, height))

    if start_x == end_x or start_y == end_y:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid crop dimensions: area is zero"
        )

    return start_x, start_y, end_x, end_y


def _selection_metadata_path(session_id: str) -> Path:
    return REGION_METADATA_DIR / f"{session_id}.json"


def _persist_selection(session_id: str, selection_payload: dict) -> None:
    metadata_path = _selection_metadata_path(session_id)
    try:
        metadata_path.write_text(json.dumps(selection_payload, indent=2), encoding="utf-8")
    except Exception as exc:
        logger.warning("Failed to persist selection metadata for %s: %s", session_id, exc)


# Upload image endpoint
@router.post("/upload")
def upload_image_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        filename = (file.filename or "").strip()
        extension = Path(filename).suffix.lower()
        data = file.file.read()
        UploadSecurity.validate_image_bytes(filename, data)

        # Generate unique filename and save
        file_id = str(uuid.uuid4())
        saved_filename = f"{file_id}{extension}"
        file_path = os.path.join(str(UPLOADS_DIR), saved_filename)

        with open(file_path, "wb") as buffer:
            buffer.write(data)

        logger.info("Successfully uploaded image: %s (source: %s)", saved_filename, filename)

        # Return the URL path relative to the static files mount
        return {
            "id": file_id,
            "filename": saved_filename,
            "file_path": f"/uploads/images/{saved_filename}",
        }
    except ValueError as e:
        logger.warning("Upload rejected: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to upload image") from e


# Select region endpoint
@router.post("/select_region/")
def select_region(
    payload: RegionSelectionRequest,
    db: Session = Depends(get_db)
):
    try:
        session_id = UploadSecurity.validate_session_id(payload.session_id)
        threshold = UploadSecurity.validate_threshold(payload.threshold)
        color = UploadSecurity.validate_hex_color(payload.color)
        file_path = _resolve_upload_path(session_id)

        # Read image dimensions and validate bounds without forcing a crop write.
        image = cv2.imread(file_path)
        if image is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to read image file"
            )

        height, width = image.shape[:2]
        x1, y1, x2, y2 = _normalize_crop_bounds(
            width=width,
            height=height,
            x1=payload.x1,
            y1=payload.y1,
            x2=payload.x2,
            y2=payload.y2
        )

        metadata = {
            "session_id": session_id,
            "selected_at": datetime.now(timezone.utc).isoformat(),
            "selection": {
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "threshold": threshold,
                "color": color,
            },
            "image_bounds": {"width": width, "height": height},
        }
        _persist_selection(session_id, metadata)

        return {
            "message": "Region selected",
            "session_id": session_id,
            "selection": metadata["selection"],
            "image": metadata["image_bounds"],
            "file_path": f"/uploads/images/{Path(file_path).name}",
        }
    except Exception as e:
        logger.error(f"Error in select_region: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to select region"
        )


# Process image endpoint
@router.post("/process_image/")
def process_image_endpoint(
    session_id: str = Form(...),
    x1: int = Form(...),
    y1: int = Form(...),
    x2: int = Form(...),
    y2: int = Form(...),
    color: str = Form(...),
    threshold: int = Form(...),
    db: Session = Depends(get_db)
):
    try:
        session_id = UploadSecurity.validate_session_id(session_id)
        threshold = UploadSecurity.validate_threshold(threshold)
        color = UploadSecurity.validate_hex_color(color)

        # Correctly reference the saved image file based on session_id
        file_path = _resolve_upload_path(session_id)

        logger.info("[BACKEND] process_image_endpoint called")
        logger.info(f"[BACKEND] Session ID: {session_id}")
        logger.info(f"[BACKEND] File path: {file_path}")
        logger.info(f"[BACKEND] File exists: {os.path.exists(file_path)}")
        logger.info(f"[BACKEND] Coords: ({x1}, {y1}) → ({x2}, {y2})")
        logger.info(f"[BACKEND] Color: {color}, Threshold: {threshold}")

        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail="Image file not found."
            )

        # Process the image
        image = cv2.imread(file_path)
        if image is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to read image file"
            )
        logger.info(f"[BACKEND] Image shape: {image.shape}")

        height, width = image.shape[:2]
        x_start, y_start, x_end, y_end = _normalize_crop_bounds(
            width=width,
            height=height,
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2
        )

        logger.info(f"[BACKEND] Clamped coords: ({x_start}, {y_start}) → ({x_end}, {y_end})")
        logger.info(f"[BACKEND] Crop size: {x_end-x_start} x {y_end-y_start}")

        if x_start == x_end or y_start == y_end:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid crop dimensions: area is zero"
            )

        cropped_image = image[y_start:y_end, x_start:x_end]
        gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)

        # Convert color hex string (#RRGGBB) to BGR tuple for OpenCV
        hex_color = color.lstrip("#")
        r_val = int(hex_color[0:2], 16)
        g_val = int(hex_color[2:4], 16)
        b_val = int(hex_color[4:6], 16)
        color_bgr = (b_val, g_val, r_val)

        color_image = np.zeros_like(cropped_image, dtype=np.uint8)
        color_image[:, :] = color_bgr
        result_image = cv2.bitwise_and(color_image, color_image, mask=mask)

        b_channel, g_channel, r_channel = cv2.split(result_image)
        alpha = mask
        final_image = cv2.merge([b_channel, g_channel, r_channel, alpha])

        final_image_pil = Image.fromarray(final_image)
        final_image_io = BytesIO()
        final_image_pil.save(final_image_io, format="PNG")
        final_image_io.seek(0)

        logger.info(
            f"[BACKEND] Returning PNG, "
            f"{final_image_io.getbuffer().nbytes} bytes"
        )

        return StreamingResponse(final_image_io, media_type="image/png")
    except HTTPException:
        # Re-raise explicit HTTP exceptions (e.g., 400 Bad Request, 404 Not Found)
        raise
    except ValueError as e:
        logger.warning("process_image rejected: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to process image")
