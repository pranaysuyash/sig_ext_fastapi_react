"""Database-backed audit logging for PDF operations."""

import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass
import json


# Local SQLite database path
DB_DIR = Path.home() / ".signature_extractor"
DB_PATH = DB_DIR / "audit_logs.db"


@dataclass
class AuditLogEntry:
    """Audit log entry."""
    id: int
    timestamp: str
    pdf_path: str
    pdf_name: str
    operation: str
    user_email: Optional[str]
    details: Optional[str]
    page_number: Optional[int]
    signature_path: Optional[str]
    x: Optional[int]
    y: Optional[int]
    width: Optional[int]
    height: Optional[int]
    output_path: Optional[str]
    signature_count: Optional[int]
    error_type: Optional[str]
    error_message: Optional[str]
    success: bool


class DatabaseAuditLogger:
    """SQLite-based audit logger for PDF operations."""
    
    def __init__(self, pdf_path: str, user_email: Optional[str] = None):
        self.pdf_path = pdf_path
        self.pdf_name = Path(pdf_path).name
        self.user_email = user_email
        self._ensure_database()
    
    def _ensure_database(self):
        """Create database and table if they don't exist."""
        DB_DIR.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pdf_audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                pdf_path TEXT NOT NULL,
                pdf_name TEXT NOT NULL,
                operation TEXT NOT NULL,
                user_email TEXT,
                details TEXT,
                page_number INTEGER,
                signature_path TEXT,
                x INTEGER,
                y INTEGER,
                width INTEGER,
                height INTEGER,
                output_path TEXT,
                signature_count INTEGER,
                error_type TEXT,
                error_message TEXT,
                success BOOLEAN DEFAULT 1
            )
        ''')
        
        # Create indexes for common queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_pdf_path ON pdf_audit_logs(pdf_path)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_operation ON pdf_audit_logs(operation)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON pdf_audit_logs(timestamp)')
        
        conn.commit()
        conn.close()
    
    def _log(self, operation: str, **kwargs):
        """Internal method to log an operation."""
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO pdf_audit_logs (
                pdf_path, pdf_name, operation, user_email, details,
                page_number, signature_path, x, y, width, height,
                output_path, signature_count, error_type, error_message, success
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.pdf_path,
            self.pdf_name,
            operation,
            self.user_email,
            kwargs.get('details'),
            kwargs.get('page_number'),
            kwargs.get('signature_path'),
            kwargs.get('x'),
            kwargs.get('y'),
            kwargs.get('width'),
            kwargs.get('height'),
            kwargs.get('output_path'),
            kwargs.get('signature_count'),
            kwargs.get('error_type'),
            kwargs.get('error_message'),
            kwargs.get('success', True)
        ))
        
        conn.commit()
        conn.close()
    
    def log_open(self):
        """Log PDF opening."""
        self._log('open_pdf', details=f"Opened PDF: {self.pdf_name}")
    
    def log_place_signature(self, page_num: int, sig_path: str, x: int, y: int, width: int, height: int):
        """Log signature placement."""
        details = f"Placed signature on page {page_num + 1} at ({x}, {y})"
        self._log(
            'place_signature',
            details=details,
            page_number=page_num,
            signature_path=sig_path,
            x=x,
            y=y,
            width=width,
            height=height
        )
    
    def log_save(self, output_path: str, sig_count: int):
        """Log PDF save operation."""
        details = f"Saved signed PDF with {sig_count} signature(s)"
        self._log(
            'save_pdf',
            details=details,
            output_path=output_path,
            signature_count=sig_count
        )
    
    def log_error(self, error_type: str, error_message: str):
        """Log an error."""
        self._log(
            'error',
            error_type=error_type,
            error_message=error_message,
            success=False
        )


def get_audit_logs_for_pdf(pdf_path: str) -> List[AuditLogEntry]:
    """Get all audit logs for a specific PDF."""
    if not DB_PATH.exists():
        return []
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM pdf_audit_logs
        WHERE pdf_path = ?
        ORDER BY timestamp DESC
    ''', (pdf_path,))
    
    logs = []
    for row in cursor.fetchall():
        logs.append(AuditLogEntry(
            id=row[0],
            timestamp=row[1],
            pdf_path=row[2],
            pdf_name=row[3],
            operation=row[4],
            user_email=row[5],
            details=row[6],
            page_number=row[7],
            signature_path=row[8],
            x=row[9],
            y=row[10],
            width=row[11],
            height=row[12],
            output_path=row[13],
            signature_count=row[14],
            error_type=row[15],
            error_message=row[16],
            success=bool(row[17])
        ))
    
    conn.close()
    return logs


def get_recent_audit_logs(limit: int = 50) -> List[AuditLogEntry]:
    """Get most recent audit logs across all PDFs."""
    if not DB_PATH.exists():
        return []
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM pdf_audit_logs
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))
    
    logs = []
    for row in cursor.fetchall():
        logs.append(AuditLogEntry(
            id=row[0],
            timestamp=row[1],
            pdf_path=row[2],
            pdf_name=row[3],
            operation=row[4],
            user_email=row[5],
            details=row[6],
            page_number=row[7],
            signature_path=row[8],
            x=row[9],
            y=row[10],
            width=row[11],
            height=row[12],
            output_path=row[13],
            signature_count=row[14],
            error_type=row[15],
            error_message=row[16],
            success=bool(row[17])
        ))
    
    conn.close()
    return logs
