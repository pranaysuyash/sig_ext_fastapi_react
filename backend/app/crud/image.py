# backend/app/crud/image.py

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from app.models.image import Image
from app.schemas.image import ExtractionData
from app.database import safe_commit
import uuid
import os
import cv2
import numpy as np
import logging
from pathlib import Path
import traceback
from typing import Optional
from app.models.user import User
import aiofiles

logger = logging.getLogger(__name__)

async def upload_image(db: Session, file: UploadFile, current_user: User) -> Optional[Image]:
    """Upload and save an image file."""
    file_path = None
    
    try:
        # Log incoming file details
        logger.info(f"Starting file upload process for user {current_user.id}")
        logger.info(f"File details - Name: {file.filename}, Content-Type: {file.content_type}")

        # Validate file type
        if not file.content_type.startswith('image/'):
            logger.error(f"Invalid file type: {file.content_type}")
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Unsupported file type: {file.content_type}"
            )

        # Create upload directory
        upload_dir = Path("uploads/images") / str(current_user.id)
        try:
            os.makedirs(str(upload_dir), exist_ok=True)
            logger.info(f"Created/verified upload directory: {upload_dir}")
        except Exception as e:
            logger.error(f"Failed to create upload directory: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create upload directory"
            )

        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1].lower()
        if not file_ext:
            file_ext = '.jpg'  # Default extension
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = upload_dir / unique_filename
        logger.info(f"Generated file path: {file_path}")

        # Save the file
        try:
            contents = await file.read()
            async with aiofiles.open(str(file_path), 'wb') as f:
                await f.write(contents)
            logger.info("File saved successfully")
        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save file"
            )

        # Create database record
        try:
            db_image = Image(
                id=uuid.uuid4(),
                user_id=current_user.id,
                filename=unique_filename,
                file_path=str(file_path),
                content_type=file.content_type
            )
            db.add(db_image)
            if not safe_commit(db):
                raise Exception("Failed to commit to database")
            
            logger.info(f"Database record created for image: {db_image.id}")
            return db_image

        except Exception as e:
            logger.error(f"Failed to create database record: {e}")
            logger.error(traceback.format_exc())
            if os.path.exists(file_path):
                os.unlink(file_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create database record: {str(e)}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during file upload: {e}")
        logger.error(traceback.format_exc())
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file upload: {str(e)}"
        )

def extract_signature(
    db: Session, 
    image_id: uuid.UUID, 
    extraction_data: ExtractionData, 
    current_user: User
) -> Optional[Image]:
    """Extract signature from an uploaded image."""
    try:
        # Get the original image
        original_image = db.query(Image).filter(
            Image.id == image_id,
            Image.user_id == current_user.id
        ).first()
        
        if not original_image:
            logger.error(f"Image {image_id} not found for user {current_user.id}")
            return None
            
        # Load the image using OpenCV
        try:
            img = cv2.imread(str(original_image.file_path))
            if img is None:
                logger.error(f"Failed to load image from {original_image.file_path}")
                return None
        except Exception as e:
            logger.error(f"Error loading image: {e}")
            return None
            
        # Extract the signature region
        try:
            x1, y1 = extraction_data.x1, extraction_data.y1
            x2, y2 = extraction_data.x2, extraction_data.y2
            
            # Ensure coordinates are within bounds
            height, width = img.shape[:2]
            x1, x2 = max(0, min(x1, width-1)), max(0, min(x2, width-1))
            y1, y2 = max(0, min(y1, height-1)), max(0, min(y2, height-1))
            
            # Get the region
            signature = img[y1:y2, x1:x2]
            
            # Create output directory
            output_dir = Path("uploads/signatures") / str(current_user.id)
            os.makedirs(str(output_dir), exist_ok=True)
            
            # Save the extracted signature
            output_filename = f"sig_{uuid.uuid4()}.png"
            output_path = output_dir / output_filename
            cv2.imwrite(str(output_path), signature)
            
            # Create database record for extracted signature
            signature_image = Image(
                id=uuid.uuid4(),
                user_id=current_user.id,
                filename=output_filename,
                file_path=str(output_path),
                content_type="image/png",
                original_image_id=original_image.id
            )
            
            db.add(signature_image)
            if not safe_commit(db):
                logger.error("Failed to save signature record to database")
                if os.path.exists(output_path):
                    os.unlink(output_path)
                return None
                
            return signature_image
            
        except Exception as e:
            logger.error(f"Error extracting signature: {e}")
            logger.error(traceback.format_exc())
            return None
            
    except Exception as e:
        logger.error(f"Error in extract_signature: {e}")
        logger.error(traceback.format_exc())
        return None

def extract_signature_async(
    db: Session, 
    image_id: uuid.UUID, 
    extraction_data: ExtractionData, 
    current_user: User
) -> Image:
    """Extract signature from an uploaded image."""
    try:
        logger.info(f"Starting signature extraction for image {image_id}")
        
        # Fetch the image record
        image = db.query(Image).filter(
            Image.id == image_id,
            Image.user_id == current_user.id
        ).first()
        
        if not image:
            logger.error(f"Image {image_id} not found for user {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )

        # Verify original file exists
        original_path = Path(image.original_image_path)
        if not original_path.exists():
            logger.error(f"Original image file not found: {original_path}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Original image file not found"
            )

        # Read the image
        try:
            img = cv2.imread(str(original_path))
            if img is None:
                raise ValueError("Failed to read image file")
            logger.info("Successfully read original image")
        except Exception as e:
            logger.error(f"Error reading image: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to read image file"
            )

        # Validate extraction parameters
        height, width, _ = img.shape
        if not (0 <= extraction_data.x < width and 
                0 <= extraction_data.y < height and
                0 < extraction_data.width <= width - extraction_data.x and
                0 < extraction_data.height <= height - extraction_data.y):
            logger.error("Invalid extraction coordinates")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid extraction coordinates"
            )

        try:
            # Extract ROI
            roi = img[
                extraction_data.y:extraction_data.y + extraction_data.height,
                extraction_data.x:extraction_data.x + extraction_data.width
            ]

            # Convert to grayscale
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            
            # Apply thresholding
            _, thresh = cv2.threshold(
                gray,
                extraction_data.threshold,
                255,
                cv2.THRESH_BINARY
            )

            # Apply color if specified
            if extraction_data.color:
                color = extraction_data.color.lstrip('#')
                if len(color) == 3:
                    color = ''.join(c * 2 for c in color)
                bgr_color = tuple(int(color[i:i+2], 16) for i in (4, 2, 0))
                colored_signature = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
                colored_signature[thresh == 255] = bgr_color
            else:
                colored_signature = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

            logger.info("Successfully processed signature")

        except Exception as e:
            logger.error(f"Error processing signature: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process signature"
            )

        try:
            # Setup signature directory
            signature_dir = Path("uploads/signatures") / str(current_user.id)
            signature_dir.mkdir(parents=True, exist_ok=True)
            
            # Save extracted signature
            signature_id = uuid.uuid4()
            signature_path = signature_dir / f"{signature_id}.png"
            cv2.imwrite(str(signature_path), colored_signature)
            logger.info(f"Saved extracted signature to: {signature_path}")

            # Update database record
            image.extracted_signature_path = str(signature_path)
            db.commit()
            db.refresh(image)
            logger.info("Updated database record with signature path")
            
            return image

        except Exception as e:
            logger.error(f"Error saving signature: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save signature"
            )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Unexpected error in extract_signature: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to extract signature"
        )