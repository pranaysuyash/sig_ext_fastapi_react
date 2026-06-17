"""PDF viewing, signing, and audit logging module."""

from desktop_app.pdf.renderer import PDFRenderer
from desktop_app.pdf.viewer import PDFViewer, PDFPageView
from desktop_app.pdf.signer import PDFSigner, sign_pdf
from desktop_app.pdf.field_detection import SignatureFieldDetector, SignatureFieldCandidate
from desktop_app.pdf.form_fields import PdfFormFieldEditor, FormFieldCandidate
from desktop_app.pdf.annotations import PdfAnnotationEditor, PdfAnnotationSpec, PdfAnnotationResult
from desktop_app.pdf.storage import (
    AuditLogger,
    save_signed_pdf,
    get_audit_logs_for_pdf,
    export_audit_logs,
    ensure_pdf_dir,
    ensure_audit_dir
)
from desktop_app.pdf.template_store import (
    SignaturePlacementTemplate,
    create_template,
    delete_template,
    get_template,
    list_templates,
    save_template,
)

__all__ = [
    'PDFRenderer',
    'PDFViewer',
    'PDFPageView',
    'PDFSigner',
    'sign_pdf',
    'SignatureFieldDetector',
    'SignatureFieldCandidate',
    'PdfFormFieldEditor',
    'FormFieldCandidate',
    'PdfAnnotationEditor',
    'PdfAnnotationSpec',
    'PdfAnnotationResult',
    'AuditLogger',
    'save_signed_pdf',
    'get_audit_logs_for_pdf',
    'export_audit_logs',
    'ensure_pdf_dir',
    'ensure_audit_dir',
    'SignaturePlacementTemplate',
    'create_template',
    'delete_template',
    'get_template',
    'list_templates',
    'save_template',
]
