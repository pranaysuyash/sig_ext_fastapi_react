# from sqlalchemy import Column, String, ForeignKey, DateTime
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# import uuid
# from app.database import Base

# class Image(Base):
#     __tablename__ = "images"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
#     user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
#     filename = Column(String, nullable=False)
#     file_path = Column(String, nullable=False)
#     content_type = Column(String, nullable=True)
#     uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

#     # Relationships
#     user = relationship("User", backref="images")

#     def __repr__(self):
#         return f"<Image(id={self.id}, filename={self.filename})>"

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    original_image_id = Column(UUID(as_uuid=True), ForeignKey("images.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    user = relationship("User", backref="images")
    original_image = relationship("Image", remote_side=[id], backref="derived_images")

    def __repr__(self):
        return f"<Image(id={self.id}, filename={self.filename})>"