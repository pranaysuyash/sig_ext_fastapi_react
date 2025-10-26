# # # # # from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
# # # # # from sqlalchemy.orm import Session
# # # # # from app.database import get_db
# # # # # from app.schemas.image import ImageResponse, ExtractionData
# # # # # from app.crud.image import upload_image, extract_signature
# # # # # from app.utils import get_current_user
# # # # # from app.models.user import User
# # # # # import logging
# # # # # import uuid
# # # # # import os
# # # # # from pathlib import Path
# # # # # import traceback

# # # # # logger = logging.getLogger(__name__)
# # # # # logging.basicConfig(level=logging.DEBUG)

# # # # # router = APIRouter(
# # # # #     tags=["Extraction"]
# # # # # )

# # # # # @router.post("/upload", response_model=ImageResponse)
# # # # # async def upload_image_endpoint(
# # # # #     file: UploadFile = File(...),
# # # # #     db: Session = Depends(get_db),
# # # # #     current_user: User = Depends(get_current_user)
# # # # # ):
# # # # #     try:
# # # # #         logger.info(f"Starting image upload for user {current_user.id}")
# # # # #         logger.info(f"File details - Name: {file.filename}, Content-Type: {file.content_type}")
        
# # # # #         if not file:
# # # # #             logger.error("No file provided")
# # # # #             raise HTTPException(
# # # # #                 status_code=status.HTTP_400_BAD_REQUEST,
# # # # #                 detail="No file provided"
# # # # #             )
            
# # # # #         # Process upload
# # # # #         try:
# # # # #             image = await upload_image(db, file, current_user)
# # # # #             if not image:
# # # # #                 logger.error("Upload function returned None")
# # # # #                 raise HTTPException(
# # # # #                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # # # #                     detail="Failed to process image"
# # # # #                 )
                
# # # # #             logger.info(f"Successfully uploaded image: {image.id}")
# # # # #             return ImageResponse(
# # # # #                 id=image.id,
# # # # #                 filename=image.filename,
# # # # #                 file_path=image.file_path,
# # # # #                 content_type=image.content_type,
# # # # #                 original_image_id=image.original_image_id,
# # # # #                 created_at=image.created_at
# # # # #             )
            
# # # # #         except Exception as upload_error:
# # # # #             logger.error(f"Error in upload_image function: {str(upload_error)}")
# # # # #             logger.error(traceback.format_exc())
# # # # #             raise HTTPException(
# # # # #                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # # # #                 detail=f"Failed to process image: {str(upload_error)}"
# # # # #             )
        
# # # # #     except HTTPException as he:
# # # # #         logger.error(f"HTTP Exception: {str(he)}")
# # # # #         raise
# # # # #     except Exception as e:
# # # # #         logger.error(f"Unexpected error during image upload: {str(e)}")
# # # # #         logger.error(traceback.format_exc())
# # # # #         raise HTTPException(
# # # # #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # # # #             detail=f"Failed to upload image: {str(e)}"
# # # # #         )
# # # # #     finally:
# # # # #         await file.close()

# # # # # @router.post("/{image_id}/extract", response_model=ImageResponse)
# # # # # async def extract_signature_endpoint(
# # # # #     image_id: uuid.UUID,
# # # # #     extraction_data: ExtractionData,
# # # # #     db: Session = Depends(get_db),
# # # # #     current_user: User = Depends(get_current_user)
# # # # # ):
# # # # #     try:
# # # # #         logger.info(f"Starting signature extraction for image {image_id}")
        
# # # # #         signature = extract_signature(db, image_id, extraction_data, current_user)
# # # # #         if not signature:
# # # # #             raise HTTPException(
# # # # #                 status_code=status.HTTP_400_BAD_REQUEST,
# # # # #                 detail="Failed to extract signature"
# # # # #             )
            
# # # # #         logger.info(f"Successfully extracted signature: {signature.id}")
# # # # #         return ImageResponse(
# # # # #             id=signature.id,
# # # # #             filename=signature.filename,
# # # # #             file_path=signature.file_path,
# # # # #             content_type=signature.content_type,
# # # # #             original_image_id=signature.original_image_id,
# # # # #             created_at=signature.created_at
# # # # #         )
        
# # # # #     except HTTPException:
# # # # #         raise
# # # # #     except Exception as e:
# # # # #         logger.error(f"Error during signature extraction: {str(e)}")
# # # # #         logger.error(traceback.format_exc())
# # # # #         raise HTTPException(
# # # # #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # # # #             detail=f"Failed to extract signature: {str(e)}"
# # # # #         )


# # # # from fastapi import APIRouter, Depends, HTTPException, status
# # # # from sqlalchemy.orm import Session
# # # # from app.database import get_db
# # # # from io import BytesIO
# # # # from PIL import Image
# # # # import numpy as np
# # # # import cv2
# # # # from fastapi.responses import StreamingResponse
# # # # import uuid
# # # # import logging
# # # # import traceback

# # # # logger = logging.getLogger(__name__)
# # # # logging.basicConfig(level=logging.DEBUG)

# # # # router = APIRouter(tags=["Extraction"])

# # # # @router.post("/extraction/process_image/")
# # # # async def process_image_endpoint(
# # # #     session_id: str,
# # # #     x1: int,
# # # #     y1: int,
# # # #     x2: int,
# # # #     y2: int,
# # # #     color: str,
# # # #     threshold: int,
# # # #     db: Session = Depends(get_db)
# # # # ):
# # # #     try:
# # # #         # Assuming the file path format for uploaded images
# # # #         file_path = f"images/{session_id}.png"
# # # #         image = cv2.imread(file_path)
        
# # # #         # Check if the image loaded successfully
# # # #         if image is None:
# # # #             logger.error(f"Image file not found for session_id {session_id}")
# # # #             raise HTTPException(status_code=404, detail="Image file not found.")
        
# # # #         # Crop the image to the selected region
# # # #         cropped_image = image[y1:y2, x1:x2]
        
# # # #         # Convert to grayscale and apply threshold
# # # #         gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
# # # #         _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
        
# # # #         # Convert hex color to BGR tuple
# # # #         color_rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
# # # #         color_image = np.zeros_like(cropped_image, dtype=np.uint8)
# # # #         color_image[:, :] = color_rgb
# # # #         result_image = cv2.bitwise_and(color_image, color_image, mask=mask)
        
# # # #         # Add alpha channel to the result image
# # # #         b, g, r = cv2.split(result_image)
# # # #         alpha = mask
# # # #         final_image = cv2.merge([b, g, r, alpha])
        
# # # #         # Save as PNG to a BytesIO object
# # # #         final_image_pil = Image.fromarray(final_image)
# # # #         final_image_io = BytesIO()
# # # #         final_image_pil.save(final_image_io, format="PNG")
# # # #         final_image_io.seek(0)
        
# # # #         return StreamingResponse(final_image_io, media_type="image/png")
# # # #     except Exception as e:
# # # #         logger.error(f"Error processing image: {str(e)}")
# # # #         logger.error(traceback.format_exc())
# # # #         raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")


# # # # from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
# # # # from sqlalchemy.orm import Session
# # # # from app.database import get_db
# # # # from app.schemas.image import ImageResponse, ExtractionData
# # # # from app.crud.image import upload_image, extract_signature
# # # # from app.utils import get_current_user
# # # # from app.models.user import User
# # # # from fastapi.responses import StreamingResponse
# # # # from io import BytesIO
# # # # from PIL import Image
# # # # import numpy as np
# # # # import cv2
# # # # import logging
# # # # import uuid
# # # # import os
# # # # import traceback
# # # # from pathlib import Path

# # # # logger = logging.getLogger(__name__)
# # # # logging.basicConfig(level=logging.DEBUG)

# # # # router = APIRouter(tags=["Extraction"])

# # # # @router.post("/upload", response_model=ImageResponse)
# # # # async def upload_image_endpoint(
# # # #     file: UploadFile = File(...),
# # # #     db: Session = Depends(get_db),
# # # #     current_user: User = Depends(get_current_user)
# # # # ):
# # # #     try:
# # # #         logger.info(f"Starting image upload for user {current_user.id}")
# # # #         logger.info(f"File details - Name: {file.filename}, Content-Type: {file.content_type}")
        
# # # #         if not file:
# # # #             logger.error("No file provided")
# # # #             raise HTTPException(
# # # #                 status_code=status.HTTP_400_BAD_REQUEST,
# # # #                 detail="No file provided"
# # # #             )
            
# # # #         # Process upload
# # # #         try:
# # # #             image = await upload_image(db, file, current_user)
# # # #             if not image:
# # # #                 logger.error("Upload function returned None")
# # # #                 raise HTTPException(
# # # #                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # # #                     detail="Failed to process image"
# # # #                 )
                
# # # #             logger.info(f"Successfully uploaded image: {image.id}")
# # # #             return ImageResponse(
# # # #                 id=image.id,
# # # #                 filename=image.filename,
# # # #                 file_path=image.file_path,
# # # #                 content_type=image.content_type,
# # # #                 original_image_id=image.original_image_id,
# # # #                 created_at=image.created_at
# # # #             )
            
# # # #         except Exception as upload_error:
# # # #             logger.error(f"Error in upload_image function: {str(upload_error)}")
# # # #             logger.error(traceback.format_exc())
# # # #             raise HTTPException(
# # # #                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # # #                 detail=f"Failed to process image: {str(upload_error)}"
# # # #             )
        
# # # #     except HTTPException as he:
# # # #         logger.error(f"HTTP Exception: {str(he)}")
# # # #         raise
# # # #     except Exception as e:
# # # #         logger.error(f"Unexpected error during image upload: {str(e)}")
# # # #         logger.error(traceback.format_exc())
# # # #         raise HTTPException(
# # # #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # # #             detail=f"Failed to upload image: {str(e)}"
# # # #         )
# # # #     finally:
# # # #         await file.close()

# # # # @router.post("/{image_id}/extract", response_model=ImageResponse)
# # # # async def extract_signature_endpoint(
# # # #     image_id: uuid.UUID,
# # # #     extraction_data: ExtractionData,
# # # #     db: Session = Depends(get_db),
# # # #     current_user: User = Depends(get_current_user)
# # # # ):
# # # #     try:
# # # #         logger.info(f"Starting signature extraction for image {image_id}")
        
# # # #         signature = extract_signature(db, image_id, extraction_data, current_user)
# # # #         if not signature:
# # # #             raise HTTPException(
# # # #                 status_code=status.HTTP_400_BAD_REQUEST,
# # # #                 detail="Failed to extract signature"
# # # #             )
            
# # # #         logger.info(f"Successfully extracted signature: {signature.id}")
# # # #         return ImageResponse(
# # # #             id=signature.id,
# # # #             filename=signature.filename,
# # # #             file_path=signature.file_path,
# # # #             content_type=signature.content_type,
# # # #             original_image_id=signature.original_image_id,
# # # #             created_at=signature.created_at
# # # #         )
        
# # # #     except HTTPException:
# # # #         raise
# # # #     except Exception as e:
# # # #         logger.error(f"Error during signature extraction: {str(e)}")
# # # #         logger.error(traceback.format_exc())
# # # #         raise HTTPException(
# # # #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # # #             detail=f"Failed to extract signature: {str(e)}"
# # # #         )

# # # # @router.post("/extraction/process_image/")
# # # # async def process_image_endpoint(
# # # #     session_id: str,
# # # #     x1: int,
# # # #     y1: int,
# # # #     x2: int,
# # # #     y2: int,
# # # #     color: str,
# # # #     threshold: int,
# # # #     db: Session = Depends(get_db)
# # # # ):
# # # #     try:
# # # #         # Assuming the file path format for uploaded images
# # # #         file_path = f"images/{session_id}.png"
# # # #         image = cv2.imread(file_path)
        
# # # #         # Check if the image loaded successfully
# # # #         if image is None:
# # # #             logger.error(f"Image file not found for session_id {session_id}")
# # # #             raise HTTPException(status_code=404, detail="Image file not found.")
        
# # # #         # Crop the image to the selected region
# # # #         cropped_image = image[y1:y2, x1:x2]
        
# # # #         # Convert to grayscale and apply threshold
# # # #         gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
# # # #         _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
        
# # # #         # Convert hex color to BGR tuple
# # # #         color_rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
# # # #         color_image = np.zeros_like(cropped_image, dtype=np.uint8)
# # # #         color_image[:, :] = color_rgb
# # # #         result_image = cv2.bitwise_and(color_image, color_image, mask=mask)
        
# # # #         # Add alpha channel to the result image
# # # #         b, g, r = cv2.split(result_image)
# # # #         alpha = mask
# # # #         final_image = cv2.merge([b, g, r, alpha])
        
# # # #         # Save as PNG to a BytesIO object
# # # #         final_image_pil = Image.fromarray(final_image)
# # # #         final_image_io = BytesIO()
# # # #         final_image_pil.save(final_image_io, format="PNG")
# # # #         final_image_io.seek(0)
        
# # # #         return StreamingResponse(final_image_io, media_type="image/png")
# # # #     except Exception as e:
# # # #         logger.error(f"Error processing image: {str(e)}")
# # # #         logger.error(traceback.format_exc())
# # # #         raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")


# # # from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
# # # from sqlalchemy.orm import Session
# # # from app.database import get_db
# # # from app.schemas.image import ImageResponse, ExtractionData
# # # from app.crud.image import upload_image, extract_signature
# # # from app.utils import get_current_user
# # # from app.models.user import User
# # # from fastapi.responses import StreamingResponse
# # # from io import BytesIO
# # # from PIL import Image
# # # import numpy as np
# # # import cv2
# # # import logging
# # # import uuid
# # # import os
# # # import traceback
# # # from pathlib import Path

# # # logger = logging.getLogger(__name__)
# # # logging.basicConfig(level=logging.DEBUG)

# # # router = APIRouter(tags=["Extraction"])

# # # # Upload image endpoint
# # # @router.post("/upload", response_model=ImageResponse)
# # # async def upload_image_endpoint(
# # #     file: UploadFile = File(...),
# # #     db: Session = Depends(get_db),
# # #     current_user: User = Depends(get_current_user)
# # # ):
# # #     try:
# # #         logger.info(f"Starting image upload for user {current_user.id}")
# # #         if not file:
# # #             raise HTTPException(
# # #                 status_code=status.HTTP_400_BAD_REQUEST,
# # #                 detail="No file provided"
# # #             )
            
# # #         # Process upload
# # #         image = await upload_image(db, file, current_user)
# # #         if not image:
# # #             raise HTTPException(
# # #                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # #                 detail="Failed to process image"
# # #             )
            
# # #         logger.info(f"Successfully uploaded image: {image.id}")
# # #         return ImageResponse(
# # #             id=image.id,
# # #             filename=image.filename,
# # #             file_path=image.file_path,
# # #             content_type=image.content_type,
# # #             original_image_id=image.original_image_id,
# # #             created_at=image.created_at
# # #         )
# # #     finally:
# # #         await file.close()

# # # # Process image endpoint
# # # @router.post("/process_image")
# # # async def process_image_endpoint(
# # #     session_id: str,
# # #     x1: int,
# # #     y1: int,
# # #     x2: int,
# # #     y2: int,
# # #     color: str,
# # #     threshold: int,
# # #     db: Session = Depends(get_db)
# # # ):
# # #     try:
# # #         # Use the correct path to the uploaded image file
# # #         file_path = f"uploads/images/{session_id}.png"
# # #         image = cv2.imread(file_path)
        
# # #         if image is None:
# # #             raise HTTPException(status_code=404, detail="Image file not found.")
        
# # #         # Crop and process the image
# # #         cropped_image = image[y1:y2, x1:x2]
# # #         gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
# # #         _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
        
# # #         color_rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
# # #         color_image = np.zeros_like(cropped_image, dtype=np.uint8)
# # #         color_image[:, :] = color_rgb
# # #         result_image = cv2.bitwise_and(color_image, color_image, mask=mask)
        
# # #         b, g, r = cv2.split(result_image)
# # #         alpha = mask
# # #         final_image = cv2.merge([b, g, r, alpha])
        
# # #         final_image_pil = Image.fromarray(final_image)
# # #         final_image_io = BytesIO()
# # #         final_image_pil.save(final_image_io, format="PNG")
# # #         final_image_io.seek(0)
        
# # #         return StreamingResponse(final_image_io, media_type="image/png")
# # #     except Exception as e:
# # #         logger.error(f"Error processing image: {str(e)}")
# # #         raise HTTPException(status_code=500, detail="Failed to process image")


# # from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
# # from sqlalchemy.orm import Session
# # from app.database import get_db
# # from app.schemas.image import ImageResponse
# # from app.crud.image import upload_image
# # from app.utils import get_current_user
# # from app.models.user import User
# # from fastapi.responses import StreamingResponse
# # from io import BytesIO
# # from PIL import Image
# # import numpy as np
# # import cv2
# # import logging
# # import uuid
# # import traceback

# # logger = logging.getLogger(__name__)
# # logging.basicConfig(level=logging.DEBUG)

# # router = APIRouter(tags=["Extraction"])

# # # Upload image endpoint
# # @router.post("/upload", response_model=ImageResponse)
# # async def upload_image_endpoint(
# #     file: UploadFile = File(...),
# #     db: Session = Depends(get_db),
# #     current_user: User = Depends(get_current_user)
# # ):
# #     try:
# #         logger.info(f"Starting image upload for user {current_user.id}")
        
# #         if not file:
# #             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided")

# #         # Process upload
# #         image = await upload_image(db, file, current_user)
# #         if not image:
# #             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process image")
        
# #         logger.info(f"Successfully uploaded image: {image.id}")
# #         return ImageResponse(
# #             id=image.id,
# #             filename=image.filename,
# #             file_path=image.file_path,
# #             content_type=image.content_type,
# #             original_image_id=image.original_image_id,
# #             created_at=image.created_at
# #         )
# #     finally:
# #         await file.close()

# # # Select region endpoint
# # @router.post("/select_region")
# # async def select_region_endpoint(
# #     session_id: str,
# #     x1: int,
# #     y1: int,
# #     x2: int,
# #     y2: int,
# #     db: Session = Depends(get_db)
# # ):
# #     logger.info(f"Region selected for session {session_id}: ({x1}, {y1}) to ({x2}, {y2})")
# #     return {"status": "Region selected", "session_id": session_id, "coordinates": (x1, y1, x2, y2)}

# # # Process image endpoint
# # @router.post("/process_image")
# # async def process_image_endpoint(
# #     session_id: str,
# #     x1: int,
# #     y1: int,
# #     x2: int,
# #     y2: int,
# #     color: str,
# #     threshold: int,
# #     db: Session = Depends(get_db)
# # ):
# #     try:
# #         file_path = f"uploads/images/{session_id}.png"
# #         image = cv2.imread(file_path)
        
# #         if image is None:
# #             raise HTTPException(status_code=404, detail="Image file not found.")
        
# #         # Crop and process the image
# #         cropped_image = image[y1:y2, x1:x2]
# #         gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
# #         _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
        
# #         color_rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
# #         color_image = np.zeros_like(cropped_image, dtype=np.uint8)
# #         color_image[:, :] = color_rgb
# #         result_image = cv2.bitwise_and(color_image, color_image, mask=mask)
        
# #         b, g, r = cv2.split(result_image)
# #         alpha = mask
# #         final_image = cv2.merge([b, g, r, alpha])
        
# #         final_image_pil = Image.fromarray(final_image)
# #         final_image_io = BytesIO()
# #         final_image_pil.save(final_image_io, format="PNG")
# #         final_image_io.seek(0)
        
# #         return StreamingResponse(final_image_io, media_type="image/png")
# #     except Exception as e:
# #         logger.error(f"Error processing image: {str(e)}")
# #         raise HTTPException(status_code=500, detail="Failed to process image")


# from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
# from sqlalchemy.orm import Session
# from app.database import get_db
# from fastapi.responses import StreamingResponse
# from io import BytesIO
# from PIL import Image
# import numpy as np
# import cv2
# import logging
# import uuid
# import os
# import traceback

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)

# router = APIRouter(tags=["Extraction"])

# # Define the directory for image uploads
# UPLOADS_DIR = "uploads/images"  # Relative to where FastAPI serves static files

# # Upload image endpoint
# @router.post("/upload")
# async def upload_image_endpoint(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):
#     try:
#         if not file:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="No file provided"
#             )

#         # Generate unique filename and save
#         file_id = str(uuid.uuid4())
#         filename = f"{file_id}.png"
#         file_path = os.path.join(UPLOADS_DIR, filename)

#         with open(file_path, "wb") as buffer:
#             buffer.write(await file.read())

#         logger.info(f"Successfully uploaded image: {filename}")

#         # Return the URL path relative to the static files mount
#         return {
#             "id": file_id,
#             "filename": filename,
#             "file_path": f"/uploads/images/{filename}"
#         }
#     except Exception as e:
#         logger.error(f"Error uploading image: {str(e)}")
#         raise HTTPException(status_code=500, detail="Failed to upload image")

# # Process image endpoint
# @router.post("/process_image")
# async def process_image_endpoint(
#     session_id: str,
#     x1: int,
#     y1: int,
#     x2: int,
#     y2: int,
#     color: str,
#     threshold: int,
#     db: Session = Depends(get_db)
# ):
#     try:
#         # Correctly reference the saved image file based on session_id
#         file_path = os.path.join(UPLOADS_DIR, f"{session_id}.png")
#         if not os.path.exists(file_path):
#             raise HTTPException(status_code=404, detail="Image file not found.")

#         # Process the image
#         image = cv2.imread(file_path)
#         cropped_image = image[y1:y2, x1:x2]
#         gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
#         _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)

#         color_rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
#         color_image = np.zeros_like(cropped_image, dtype=np.uint8)
#         color_image[:, :] = color_rgb
#         result_image = cv2.bitwise_and(color_image, color_image, mask=mask)

#         b, g, r = cv2.split(result_image)
#         alpha = mask
#         final_image = cv2.merge([b, g, r, alpha])

#         final_image_pil = Image.fromarray(final_image)
#         final_image_io = BytesIO()
#         final_image_pil.save(final_image_io, format="PNG")
#         final_image_io.seek(0)

#         return StreamingResponse(final_image_io, media_type="image/png")
#     except Exception as e:
#         logger.error(f"Error processing image: {str(e)}")
#         raise HTTPException(status_code=500, detail="Failed to process image")


# extraction.py

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request, Form
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

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

router = APIRouter(tags=["Extraction"])

# Define the directory for image uploads
UPLOADS_DIR = "uploads/images"  # Relative to where FastAPI serves static files

# Ensure the uploads directory exists
os.makedirs(UPLOADS_DIR, exist_ok=True)

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

        # Generate unique filename and save
        file_id = str(uuid.uuid4())
        filename = f"{file_id}.png"
        file_path = os.path.join(UPLOADS_DIR, filename)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        logger.info(f"Successfully uploaded image: {filename}")

        # Return the URL path relative to the static files mount
        return {
            "id": file_id,
            "filename": filename,
            "file_path": f"/uploads/images/{filename}"
        }
    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to upload image")

# Select region endpoint
@router.post("/select_region/")
async def select_region(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        data = await request.json()
        session_id = data.get('session_id')
        x1 = data.get('x1')
        y1 = data.get('y1')
        x2 = data.get('x2')
        y2 = data.get('y2')
        color = data.get('color')
        threshold = data.get('threshold')

        # Process the image region (this could call process_image or similar logic)
        # For example, save the selected region data to the session or database

        logger.info("select_region endpoint was called with data:")
        logger.info(data)

        # For demonstration, we'll just return the data back
        return {"message": "Region selected", "data": data}
    except Exception as e:
        logger.error(f"Error in select_region: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to select region")

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
        # Correctly reference the saved image file based on session_id
        file_path = os.path.join(UPLOADS_DIR, f"{session_id}.png")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Image file not found.")

        # Process the image
        image = cv2.imread(file_path)

        # Ensure coordinates are within image bounds
        height, width = image.shape[:2]
        x1 = max(0, min(x1, width))
        x2 = max(0, min(x2, width))
        y1 = max(0, min(y1, height))
        y2 = max(0, min(y2, height))

        cropped_image = image[y1:y2, x1:x2]
        gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)

        # Convert color hex string to RGB tuple
        color_rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))

        color_image = np.zeros_like(cropped_image, dtype=np.uint8)
        color_image[:, :] = color_rgb
        result_image = cv2.bitwise_and(color_image, color_image, mask=mask)

        b, g, r = cv2.split(result_image)
        alpha = mask
        final_image = cv2.merge([b, g, r, alpha])

        final_image_pil = Image.fromarray(final_image)
        final_image_io = BytesIO()
        final_image_pil.save(final_image_io, format="PNG")
        final_image_io.seek(0)

        return StreamingResponse(final_image_io, media_type="image/png")
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to process image")
