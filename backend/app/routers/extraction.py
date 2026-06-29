
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from pathlib import Path
import logging
import uuid
import os
from pydantic import BaseModel, Field
import cv2

from backend.app.paths import UPLOADS_DIR
from backend.app.security import UploadSecurity
from backend.app.services.extraction import (
    build_selection_metadata,
    persist_selection_metadata,
    render_signature_png,
    resolve_upload_path,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Extraction"])


os.makedirs(str(UPLOADS_DIR), exist_ok=True)

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


# Upload image endpoint
@router.post("/upload")
def upload_image_endpoint(
    file: UploadFile = File(...),
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

        file_id = str(uuid.uuid4())
        saved_filename = f"{file_id}{extension}"
        file_path = os.path.join(str(UPLOADS_DIR), saved_filename)

        with open(file_path, "wb") as buffer:
            buffer.write(data)

        logger.info("Successfully uploaded image: %s (source: %s)", saved_filename, filename)

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
):
    try:
        session_id = payload.session_id
        file_path = resolve_upload_path(session_id, Path(str(UPLOADS_DIR)))

        image = cv2.imread(str(file_path))
        if image is None:
            raise ValueError("Failed to read image file")

        height, width = image.shape[:2]
        metadata = build_selection_metadata(
            session_id,
            width=width,
            height=height,
            x1=payload.x1,
            y1=payload.y1,
            x2=payload.x2,
            y2=payload.y2,
            threshold=payload.threshold,
            color=payload.color,
        )
        persist_selection_metadata(REGION_METADATA_DIR, session_id, metadata)

        return {
            "message": "Region selected",
            "session_id": session_id,
            "selection": metadata["selection"],
            "image": metadata["image_bounds"],
            "file_path": f"/uploads/images/{file_path.name}",
        }
    except HTTPException:
        raise
    except FileNotFoundError as e:
        logger.warning("select_region missing file: %s", e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ValueError as e:
        logger.warning("select_region rejected: %s", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        logger.exception("Error in select_region: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to select region"
        ) from e


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
):
    try:
        file_path = resolve_upload_path(session_id, Path(str(UPLOADS_DIR)))

        final_image_io = render_signature_png(
            file_path,
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
            color=color,
            threshold=threshold,
        )
        return StreamingResponse(final_image_io, media_type="image/png")
    except HTTPException:
        raise
    except FileNotFoundError as e:
        logger.warning("process_image missing file: %s", e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ValueError as e:
        logger.warning("process_image rejected: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.exception("Error processing image: %s", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process image") from e
