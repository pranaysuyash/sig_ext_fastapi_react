"""Audit log model for PDF signing operations."""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from backend.app.database import Base


class PDFAuditLog(Base):
    """Audit log entry for PDF operations."""
    
    __tablename__ = "pdf_audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # PDF information
    pdf_path = Column(String(512), nullable=False, index=True)
    pdf_name = Column(String(255), nullable=False)
    
    # Operation details
    operation = Column(String(50), nullable=False, index=True)  # 'open_pdf', 'place_signature', 'save_pdf', 'error'
    
    # User information
    user_email = Column(String(255), nullable=True)
    
    # Operation-specific details (JSON-serialized)
    details = Column(Text, nullable=True)
    
    # For signature placement
    page_number = Column(Integer, nullable=True)
    signature_path = Column(String(512), nullable=True)
    x = Column(Integer, nullable=True)
    y = Column(Integer, nullable=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    
    # For save operations
    output_path = Column(String(512), nullable=True)
    signature_count = Column(Integer, nullable=True)
    
    # For errors
    error_type = Column(String(100), nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Success flag
    success = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<PDFAuditLog(id={self.id}, operation='{self.operation}', pdf='{self.pdf_name}', timestamp='{self.timestamp}')>"
