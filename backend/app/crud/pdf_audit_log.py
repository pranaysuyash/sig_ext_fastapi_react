"""CRUD operations for PDF audit logs."""

from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from backend.app.models.pdf_audit_log import PDFAuditLog


def create_audit_log(
    db: Session,
    pdf_path: str,
    pdf_name: str,
    operation: str,
    user_email: Optional[str] = None,
    details: Optional[str] = None,
    page_number: Optional[int] = None,
    signature_path: Optional[str] = None,
    x: Optional[int] = None,
    y: Optional[int] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    output_path: Optional[str] = None,
    signature_count: Optional[int] = None,
    error_type: Optional[str] = None,
    error_message: Optional[str] = None,
    success: bool = True
) -> PDFAuditLog:
    """Create a new audit log entry."""
    log = PDFAuditLog(
        pdf_path=pdf_path,
        pdf_name=pdf_name,
        operation=operation,
        user_email=user_email,
        details=details,
        page_number=page_number,
        signature_path=signature_path,
        x=x,
        y=y,
        width=width,
        height=height,
        output_path=output_path,
        signature_count=signature_count,
        error_type=error_type,
        error_message=error_message,
        success=success
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_logs_by_pdf(db: Session, pdf_path: str, limit: int = 100) -> List[PDFAuditLog]:
    """Get all audit logs for a specific PDF."""
    return db.query(PDFAuditLog)\
        .filter(PDFAuditLog.pdf_path == pdf_path)\
        .order_by(PDFAuditLog.timestamp.desc())\
        .limit(limit)\
        .all()


def get_recent_logs(db: Session, limit: int = 50) -> List[PDFAuditLog]:
    """Get most recent audit logs across all PDFs."""
    return db.query(PDFAuditLog)\
        .order_by(PDFAuditLog.timestamp.desc())\
        .limit(limit)\
        .all()


def get_logs_by_operation(db: Session, operation: str, limit: int = 100) -> List[PDFAuditLog]:
    """Get audit logs filtered by operation type."""
    return db.query(PDFAuditLog)\
        .filter(PDFAuditLog.operation == operation)\
        .order_by(PDFAuditLog.timestamp.desc())\
        .limit(limit)\
        .all()


def get_error_logs(db: Session, limit: int = 100) -> List[PDFAuditLog]:
    """Get all error logs."""
    return db.query(PDFAuditLog)\
        .filter(PDFAuditLog.success == False)\
        .order_by(PDFAuditLog.timestamp.desc())\
        .limit(limit)\
        .all()


def delete_logs_older_than(db: Session, days: int) -> int:
    """Delete audit logs older than specified days. Returns count of deleted logs."""
    from datetime import timedelta
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    count = db.query(PDFAuditLog)\
        .filter(PDFAuditLog.timestamp < cutoff_date)\
        .delete()
    
    db.commit()
    return count
