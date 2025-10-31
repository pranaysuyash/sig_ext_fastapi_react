"""Storage management for PDF documents and audit logs."""

import os
import json
from dataclasses import dataclass, asdict
from typing import List, Optional
from datetime import datetime
from pathlib import Path


# Use existing app directory structure
APP_DIR = os.path.join(os.path.expanduser("~"), ".signature_extractor")
PDF_DIR = os.path.join(APP_DIR, "pdfs")
AUDIT_DIR = os.path.join(APP_DIR, "audit_logs")


def ensure_pdf_dir() -> str:
    """Ensure PDF output directory exists."""
    os.makedirs(PDF_DIR, exist_ok=True)
    return PDF_DIR


def ensure_audit_dir() -> str:
    """Ensure audit log directory exists."""
    os.makedirs(AUDIT_DIR, exist_ok=True)
    return AUDIT_DIR


def auto_pdf_filename(original_name: str = "document") -> str:
    """Generate timestamped filename for saved PDF."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = Path(original_name).stem
    return f"{base}_signed_{ts}.pdf"


def save_signed_pdf(pdf_bytes: bytes, original_name: str = "document.pdf") -> str:
    """
    Save signed PDF to library.
    
    Args:
        pdf_bytes: PDF file bytes
        original_name: Original PDF filename (for naming)
    
    Returns:
        Full path to saved PDF
    """
    ensure_pdf_dir()
    fname = auto_pdf_filename(original_name)
    path = os.path.join(PDF_DIR, fname)
    with open(path, "wb") as f:
        f.write(pdf_bytes)
    return path


@dataclass
class AuditLogEntry:
    """Single audit log entry."""
    timestamp: str  # ISO format
    operation: str  # "open_pdf", "place_signature", "save_pdf", "delete_signature"
    pdf_path: str
    details: dict  # Operation-specific details
    user_email: Optional[str] = None


class AuditLogger:
    """Audit logger for PDF operations."""
    
    def __init__(self, pdf_path: str, user_email: Optional[str] = None):
        self.pdf_path = pdf_path
        self.user_email = user_email
        ensure_audit_dir()
        
        # Create log file per PDF
        pdf_name = Path(pdf_path).stem
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(AUDIT_DIR, f"{pdf_name}_{ts}.jsonl")
    
    def log(self, operation: str, details: dict) -> None:
        """
        Log an operation.
        
        Args:
            operation: Operation type (e.g., "open_pdf", "place_signature")
            details: Operation-specific details
        """
        entry = AuditLogEntry(
            timestamp=datetime.now().isoformat(),
            operation=operation,
            pdf_path=self.pdf_path,
            details=details,
            user_email=self.user_email
        )
        
        # Append to JSONL file (one JSON object per line)
        with open(self.log_file, "a") as f:
            f.write(json.dumps(asdict(entry)) + "\n")
    
    def log_open(self) -> None:
        """Log PDF opened."""
        self.log("open_pdf", {
            "action": "User opened PDF for viewing/signing"
        })
    
    def log_place_signature(self, page: int, sig_path: str, x: int, y: int, 
                           width: int, height: int) -> None:
        """Log signature placement."""
        self.log("place_signature", {
            "page": page,
            "signature_file": Path(sig_path).name,
            "position": {"x": x, "y": y},
            "size": {"width": width, "height": height}
        })
    
    def log_remove_signature(self, page: int, index: int) -> None:
        """Log signature removal."""
        self.log("remove_signature", {
            "page": page,
            "signature_index": index
        })
    
    def log_save(self, output_path: str, signature_count: int) -> None:
        """Log PDF saved."""
        self.log("save_pdf", {
            "output_path": output_path,
            "signature_count": signature_count,
            "output_size_bytes": os.path.getsize(output_path) if os.path.exists(output_path) else 0
        })
    
    def log_error(self, error_type: str, error_msg: str) -> None:
        """Log an error."""
        self.log("error", {
            "error_type": error_type,
            "error_message": error_msg
        })


def get_audit_logs_for_pdf(pdf_path: str) -> List[AuditLogEntry]:
    """
    Retrieve audit logs for a specific PDF.
    
    Args:
        pdf_path: Path to PDF file
    
    Returns:
        List of audit log entries
    """
    ensure_audit_dir()
    pdf_name = Path(pdf_path).stem
    
    # Find all log files for this PDF
    logs = []
    for fname in os.listdir(AUDIT_DIR):
        if fname.startswith(pdf_name) and fname.endswith(".jsonl"):
            log_path = os.path.join(AUDIT_DIR, fname)
            with open(log_path, "r") as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        logs.append(AuditLogEntry(**data))
                    except Exception:
                        continue
    
    return sorted(logs, key=lambda x: x.timestamp)


def export_audit_logs(pdf_path: str, output_path: str) -> None:
    """
    Export audit logs to JSON file.
    
    Args:
        pdf_path: Path to PDF file
        output_path: Path to save exported logs
    """
    logs = get_audit_logs_for_pdf(pdf_path)
    with open(output_path, "w") as f:
        json.dump([asdict(log) for log in logs], f, indent=2)
