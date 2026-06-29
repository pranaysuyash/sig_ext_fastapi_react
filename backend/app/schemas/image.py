from datetime import datetime
from typing import Optional

import re
from pydantic import BaseModel, ConfigDict, Field, UUID4, field_validator


class ExtractionData(BaseModel):
    x: int = Field(..., ge=0, description="X coordinate of the extraction area")
    y: int = Field(..., ge=0, description="Y coordinate of the extraction area")
    width: int = Field(..., gt=0, description="Width of the extraction area")
    height: int = Field(..., gt=0, description="Height of the extraction area")
    threshold: int = Field(
        default=128,
        ge=0,
        le=255,
        description="Threshold value for binarization",
    )
    color: Optional[str] = Field(
        None,
        description="Hex color code for the signature (e.g., '#000000')",
    )

    @field_validator("color")
    def validate_color(cls, v):
        if v is not None and not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", v):
            raise ValueError("Invalid hex color code")
        return v


class ImageBase(BaseModel):
    filename: str
    file_path: str
    content_type: str


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    user_id: UUID4
    original_image_id: Optional[UUID4] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class ImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    filename: str
    file_path: str
    content_type: str
    original_image_id: Optional[UUID4] = None
    created_at: datetime
