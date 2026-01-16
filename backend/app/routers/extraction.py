
# extraction.py

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Request,
    Form,
)
from sqlalchemy.orm import Session
from backend.app.database import get_db
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import logging
import uuid
import os
import traceback

from backend.app.paths import UPLOADS_DIR
from backend.app.security import UploadSecurity

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

router = APIRouter(tags=["Extraction"])


# Ensure the uploads directory exists
os.makedirs(str(UPLOADS_DIR), exist_ok=True)


# Upload image endpoint
@router.post("/upload")
async def upload_image_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )

        data = await file.read()
        UploadSecurity.validate_image_bytes(file.filename or "", data)

        # Generate unique filename and save
        file_id = str(uuid.uuid4())
        filename = f"{file_id}.png"
        file_path = os.path.join(str(UPLOADS_DIR), filename)

        with open(file_path, "wb") as buffer:
            buffer.write(data)

        logger.info(f"Successfully uploaded image: {filename}")

        # Return the URL path relative to the static files mount
        return {
            "id": file_id,
            "filename": filename,
            "file_path": f"/uploads/images/{filename}"
        }
    except ValueError as e:
        logger.warning("Upload rejected: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to upload image") from e


# Select region endpoint
@router.post("/select_region/")
async def select_region(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        data = await request.json()
        # Variables extracted for potential future use
        session_id = data.get('session_id')  # noqa: F841
        x1 = data.get('x1')  # noqa: F841
        y1 = data.get('y1')  # noqa: F841
        x2 = data.get('x2')  # noqa: F841
        y2 = data.get('y2')  # noqa: F841
        color = data.get('color')  # noqa: F841
        threshold = data.get('threshold')  # noqa: F841

        # Process the image region (this could call process_image
        # or similar logic). For example, save the selected region
        # data to the session or database

        logger.info("select_region endpoint was called with data:")
        logger.info(data)

        # For demonstration, we'll just return the data back
        return {"message": "Region selected", "data": data}
    except Exception as e:
        logger.error(f"Error in select_region: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to select region"
        )


# Process image endpoint
@router.post("/process_image/")
async def process_image_endpoint(
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
        file_path = os.path.join(str(UPLOADS_DIR), f"{session_id}.png")

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

        # Ensure coordinates are within image bounds
        height, width = image.shape[:2]
        x1 = max(0, min(x1, width))
        x2 = max(0, min(x2, width))
        y1 = max(0, min(y1, height))
        y2 = max(0, min(y2, height))

        logger.info(f"[BACKEND] Clamped coords: ({x1}, {y1}) → ({x2}, {y2})")
        logger.info(f"[BACKEND] Crop size: {x2-x1} x {y2-y1}")

        cropped_image = image[y1:y2, x1:x2]
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
    except ValueError as e:
        logger.warning("process_image rejected: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to process image")
