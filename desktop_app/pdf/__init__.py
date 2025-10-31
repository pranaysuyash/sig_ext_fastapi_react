"""PDF viewing, signing, and audit logging module."""

from desktop_app.pdf.renderer import PDFRenderer
from desktop_app.pdf.viewer import PDFViewer, PDFPageView
from desktop_app.pdf.signer import PDFSigner, sign_pdf
from desktop_app.pdf.storage import (
    AuditLogger,
    save_signed_pdf,
    get_audit_logs_for_pdf,
    export_audit_logs,
    ensure_pdf_dir,
    ensure_audit_dir
)

__all__ = [
    'PDFRenderer',
    'PDFViewer',
    'PDFPageView',
    'PDFSigner',
    'sign_pdf',
    'AuditLogger',
    'save_signed_pdf',
    'get_audit_logs_for_pdf',
    'export_audit_logs',
    'ensure_pdf_dir',
    'ensure_audit_dir'
]
