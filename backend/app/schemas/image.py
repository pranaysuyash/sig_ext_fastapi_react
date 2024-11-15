# # # # # backend/app/schemas/image.py
# # # # from pydantic import BaseModel, Field, validator
# # # # from typing import Optional
# # # # import uuid
# # # # from datetime import datetime

# # # # class ImageCreate(BaseModel):
# # # #     # Define fields if necessary
# # # #     pass

# # # # class ImageResponse(BaseModel):
# # # #     id: uuid.UUID
# # # #     user_id: uuid.UUID
# # # #     original_image_path: str
# # # #     extracted_signature_path: Optional[str]
# # # #     uploaded_at: datetime

# # # #     class Config:
# # # #         from_attributes = True  # For Pydantic V2

# # # # class ExtractionData(BaseModel):
# # # #     x: int = Field(..., ge=0, description="X-coordinate for cropping")
# # # #     y: int = Field(..., ge=0, description="Y-coordinate for cropping")
# # # #     width: int = Field(..., gt=0, description="Width of the cropping area")
# # # #     height: int = Field(..., gt=0, description="Height of the cropping area")
# # # #     color: Optional[str] = Field(
# # # #         None,
# # # #         pattern="^#(?:[0-9a-fA-F]{3}){1,2}$",
# # # #         description="Hex color code for the signature"
# # # #     )
# # # #     threshold: int = Field(
# # # #         ...,
# # # #         ge=0,
# # # #         le=255,
# # # #         description="Threshold value for binary thresholding"
# # # #     )

# # # #     @validator('color')
# # # #     def validate_color(cls, v):
# # # #         if v is not None:
# # # #             if not v.startswith("#"):
# # # #                 raise ValueError("Color must start with '#'")
# # # #         return v


# # # # backend/app/schemas/image.py
# # # from pydantic import BaseModel, Field, validator
# # # from typing import Optional
# # # import uuid
# # # from datetime import datetime

# # # class ImageCreate(BaseModel):
# # #     # Define fields if necessary
# # #     pass

# # # class ImageResponse(BaseModel):
# # #     id: uuid.UUID
# # #     user_id: uuid.UUID
# # #     original_image_path: str
# # #     extracted_signature_path: Optional[str] = None
# # #     uploaded_at: datetime
# # #     message: str = "Image uploaded successfully"

# # #     class Config:
# # #         from_attributes = True  # For Pydantic V2

# # # class ExtractionData(BaseModel):
# # #     x: int = Field(..., ge=0, description="X-coordinate for cropping")
# # #     y: int = Field(..., ge=0, description="Y-coordinate for cropping")
# # #     width: int = Field(..., gt=0, description="Width of the cropping area")
# # #     height: int = Field(..., gt=0, description="Height of the cropping area")
# # #     color: Optional[str] = Field(
# # #         None,
# # #         pattern="^#(?:[0-9a-fA-F]{3}){1,2}$",
# # #         description="Hex color code for the signature"
# # #     )
# # #     threshold: int = Field(
# # #         ...,
# # #         ge=0,
# # #         le=255,
# # #         description="Threshold value for binary thresholding"
# # #     )

# # #     @validator('color')
# # #     def validate_color(cls, v):
# # #         if v is not None:
# # #             if not v.startswith("#"):
# # #                 raise ValueError("Color must start with '#'")
# # #         return v


# # from pydantic import BaseModel, UUID4, Field, validator
# # from typing import Optional
# # from datetime import datetime
# # import re

# # class ExtractionData(BaseModel):
# #     x: int = Field(..., ge=0, description="X coordinate of the extraction area")
# #     y: int = Field(..., ge=0, description="Y coordinate of the extraction area")
# #     width: int = Field(..., gt=0, description="Width of the extraction area")
# #     height: int = Field(..., gt=0, description="Height of the extraction area")
# #     threshold: int = Field(
# #         default=128,
# #         ge=0,
# #         le=255,
# #         description="Threshold value for binarization"
# #     )
# #     color: Optional[str] = Field(
# #         None,
# #         description="Hex color code for the signature (e.g., '#000000')"
# #     )

# #     @validator('color')
# #     def validate_color(cls, v):
# #         if v is not None:
# #             if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', v):
# #                 raise ValueError('Invalid hex color code')
# #         return v

# # class ImageBase(BaseModel):
# #     original_image_path: str
# #     extracted_signature_path: Optional[str] = None

# # class ImageCreate(ImageBase):
# #     pass

# # class Image(ImageBase):
# #     id: UUID4
# #     user_id: UUID4
# #     uploaded_at: datetime

# #     class Config:
# #         orm_mode = True

# # class ImageResponse(BaseModel):
# #     image: Image

# from pydantic import BaseModel, UUID4, Field, field_validator
# from typing import Optional
# from datetime import datetime
# import re

# class ExtractionData(BaseModel):
#     x: int = Field(..., ge=0, description="X coordinate of the extraction area")
#     y: int = Field(..., ge=0, description="Y coordinate of the extraction area")
#     width: int = Field(..., gt=0, description="Width of the extraction area")
#     height: int = Field(..., gt=0, description="Height of the extraction area")
#     threshold: int = Field(
#         default=128,
#         ge=0,
#         le=255,
#         description="Threshold value for binarization"
#     )
#     color: Optional[str] = Field(
#         None,
#         description="Hex color code for the signature (e.g., '#000000')"
#     )

#     @field_validator('color')
#     def validate_color(cls, v):
#         if v is not None:
#             if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', v):
#                 raise ValueError('Invalid hex color code')
#         return v

# class ImageBase(BaseModel):
#     original_image_path: str
#     extracted_signature_path: Optional[str] = None

# class ImageCreate(ImageBase):
#     pass

# class Image(ImageBase):
#     id: UUID4
#     user_id: UUID4
#     uploaded_at: datetime

#     class Config:
#         from_attributes = True  # This replaces orm_mode=True

# class ImageResponse(BaseModel):
#     image: Image


from pydantic import BaseModel, UUID4, Field, field_validator
from typing import Optional
from datetime import datetime
import re

class ExtractionData(BaseModel):
    x: int = Field(..., ge=0, description="X coordinate of the extraction area")
    y: int = Field(..., ge=0, description="Y coordinate of the extraction area")
    width: int = Field(..., gt=0, description="Width of the extraction area")
    height: int = Field(..., gt=0, description="Height of the extraction area")
    threshold: int = Field(
        default=128,
        ge=0,
        le=255,
        description="Threshold value for binarization"
    )
    color: Optional[str] = Field(
        None,
        description="Hex color code for the signature (e.g., '#000000')"
    )

    @field_validator('color')
    def validate_color(cls, v):
        if v is not None:
            if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', v):
                raise ValueError('Invalid hex color code')
        return v

class ImageBase(BaseModel):
    filename: str
    file_path: str
    content_type: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: UUID4
    user_id: UUID4
    original_image_id: Optional[UUID4] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ImageResponse(BaseModel):
    id: UUID4
    filename: str
    file_path: str
    content_type: str
    original_image_id: Optional[UUID4] = None
    created_at: datetime