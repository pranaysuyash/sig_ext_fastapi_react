"""Database-backed audit logging for PDF operations."""
import sqlite3
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


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
    run_id: Optional[str]


@dataclass
class AuditRunEntry:
    """Run manifest entry."""
    run_id: str
    pdf_path: str
    pdf_name: str
    operation: str
    user_email: Optional[str]
    started_at: str
    finished_at: Optional[str]
    success: Optional[bool]
    details: Optional[str]
    signature_count: Optional[int]
    page_count: Optional[int]


def _row_to_audit_log(row: tuple) -> AuditLogEntry:
    return AuditLogEntry(
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
        success=bool(row[17]),
        run_id=row[18],
    )


def _row_to_audit_run(row: tuple) -> AuditRunEntry:
    return AuditRunEntry(
        run_id=row[0],
        pdf_path=row[1],
        pdf_name=row[2],
        operation=row[3],
        user_email=row[4],
        started_at=row[5],
        finished_at=row[6],
        success=None if row[7] is None else bool(row[7]),
        details=row[8],
        signature_count=row[9],
        page_count=row[10],
    )


class DatabaseAuditLogger:
    """SQLite-based audit logger for PDF operations."""

    def __init__(self, pdf_path: str, user_email: Optional[str] = None):
        self.pdf_path = pdf_path
        self.pdf_name = Path(pdf_path).name
        self.user_email = user_email
        self.active_run_id: Optional[str] = None
        self._ensure_database()

    def _ensure_database(self) -> None:
        """Create database and table if they don't exist."""
        DB_DIR.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        self._ensure_audit_schema_backwards_compat(cursor)

        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS pdf_audit_runs (
                run_id TEXT PRIMARY KEY,
                pdf_path TEXT NOT NULL,
                pdf_name TEXT NOT NULL,
                operation TEXT NOT NULL,
                user_email TEXT,
                started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                finished_at DATETIME,
                success BOOLEAN,
                details TEXT,
                signature_count INTEGER,
                page_count INTEGER
            )
            '''
        )

        cursor.execute(
            '''
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
                success BOOLEAN DEFAULT 1,
                run_id TEXT,
                FOREIGN KEY (run_id) REFERENCES pdf_audit_runs (run_id)
            )
            '''
        )

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_pdf_path ON pdf_audit_logs(pdf_path)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_operation ON pdf_audit_logs(operation)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON pdf_audit_logs(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_run_id ON pdf_audit_logs(run_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_runs_pdf_path ON pdf_audit_runs(pdf_path)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_runs_started_at ON pdf_audit_runs(started_at)')

        conn.commit()
        conn.close()

    def _ensure_audit_schema_backwards_compat(self, cursor: sqlite3.Cursor) -> None:
        """Backfill legacy installations missing run_id or runs table."""
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='pdf_audit_logs'"
        )
        logs_table_exists = cursor.fetchone() is not None

        if logs_table_exists:
            cursor.execute("PRAGMA table_info(pdf_audit_logs)")
            existing_columns = {row[1] for row in cursor.fetchall()}
            if "run_id" not in existing_columns:
                cursor.execute("ALTER TABLE pdf_audit_logs ADD COLUMN run_id TEXT")

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='pdf_audit_runs'"
        )
        runs_table_exists = cursor.fetchone() is not None
        if not runs_table_exists:
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS pdf_audit_runs (
                    run_id TEXT PRIMARY KEY,
                    pdf_path TEXT NOT NULL,
                    pdf_name TEXT NOT NULL,
                    operation TEXT NOT NULL,
                    user_email TEXT,
                    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    finished_at DATETIME,
                    success BOOLEAN,
                    details TEXT,
                    signature_count INTEGER,
                    page_count INTEGER
                )
                '''
            )

    def _log(
        self,
        operation: str,
        *,
        run_id: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Internal method to log an operation."""
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        cursor.execute(
            '''
            INSERT INTO pdf_audit_logs (
                pdf_path, pdf_name, operation, user_email, details,
                page_number, signature_path, x, y, width, height,
                output_path, signature_count, error_type, error_message, success, run_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
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
                kwargs.get('success', True),
                run_id or self.active_run_id,
            )
        )

        conn.commit()
        conn.close()

    def start_run(
        self,
        operation: str,
        *,
        details: Optional[str] = None,
        page_count: Optional[int] = None,
    ) -> str:
        """Start a new audit run and mark it active."""
        run_id = uuid.uuid4().hex
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO pdf_audit_runs (
                run_id, pdf_path, pdf_name, operation, user_email, details, page_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                run_id,
                self.pdf_path,
                self.pdf_name,
                operation,
                self.user_email,
                details,
                page_count,
            )
        )
        conn.commit()
        conn.close()
        self._log(
            'run_started',
            run_id=run_id,
            details=details or f"Run {operation} started",
            success=True,
        )
        # Keep active run_id for subsequent event logging.
        self.active_run_id = run_id
        return run_id

    def finish_run(
        self,
        run_id: Optional[str],
        *,
        success: bool = True,
        details: Optional[str] = None,
        signature_count: Optional[int] = None,
    ) -> None:
        """Finish an audit run and optionally update counters."""
        if not run_id:
            return

        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(
            '''
            UPDATE pdf_audit_runs
            SET finished_at = CURRENT_TIMESTAMP,
                success = ?,
                details = COALESCE(?, details),
                signature_count = COALESCE(?, signature_count)
            WHERE run_id = ?
            ''',
            (1 if success else 0, details, signature_count, run_id)
        )
        conn.commit()
        conn.close()
        if self.active_run_id == run_id:
            self.active_run_id = None

    def set_active_run(self, run_id: Optional[str]) -> None:
        """Set active run id for event logging."""
        self.active_run_id = run_id

    def log_open(self) -> None:
        """Log PDF opening."""
        self._log('open_pdf', details=f"Opened PDF: {self.pdf_name}")

    def log_place_signature(
        self,
        page_num: int,
        sig_path: str,
        x: int,
        y: int,
        width: int,
        height: int,
        *,
        run_id: Optional[str] = None,
        details: Optional[str] = None,
    ) -> None:
        """Log signature placement."""
        message = f"Placed signature on page {page_num + 1} at ({x}, {y})"
        if details:
            message = f"{message} | {details}"
        self._log(
            'place_signature',
            run_id=run_id or self.active_run_id,
            details=message,
            page_number=page_num,
            signature_path=sig_path,
            x=x,
            y=y,
            width=width,
            height=height,
        )

    def log_save(self, output_path: str, sig_count: int, *, run_id: Optional[str] = None) -> None:
        """Log PDF save operation."""
        details = f"Saved signed PDF with {sig_count} signature(s)"
        self._log(
            'save_pdf',
            run_id=run_id or self.active_run_id,
            details=details,
            output_path=output_path,
            signature_count=sig_count,
        )

    def log_error(self, error_type: str, error_message: str, *, run_id: Optional[str] = None) -> None:
        """Log an error."""
        self._log(
            'error',
            run_id=run_id or self.active_run_id,
            error_type=error_type,
            error_message=error_message,
            success=False,
        )


def get_audit_logs_for_pdf(pdf_path: str) -> List[AuditLogEntry]:
    """Get all audit logs for a specific PDF."""
    if not DB_PATH.exists():
        return []

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT * FROM pdf_audit_logs
        WHERE pdf_path = ?
        ORDER BY timestamp DESC
        ''',
        (pdf_path,),
    )
    logs = [_row_to_audit_log(row) for row in cursor.fetchall()]
    conn.close()
    return logs


def get_recent_audit_logs(limit: int = 50) -> List[AuditLogEntry]:
    """Get most recent audit logs across all PDFs."""
    if not DB_PATH.exists():
        return []

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT * FROM pdf_audit_logs
        ORDER BY timestamp DESC
        LIMIT ?
        ''',
        (limit,),
    )
    logs = [_row_to_audit_log(row) for row in cursor.fetchall()]
    conn.close()
    return logs


def get_audit_runs_for_pdf(pdf_path: str) -> List[AuditRunEntry]:
    """Get all run manifests for a specific PDF."""
    if not DB_PATH.exists():
        return []

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT run_id, pdf_path, pdf_name, operation, user_email, started_at,
               finished_at, success, details, signature_count, page_count
        FROM pdf_audit_runs
        WHERE pdf_path = ?
        ORDER BY started_at DESC
        ''',
        (pdf_path,),
    )
    runs = [_row_to_audit_run(row) for row in cursor.fetchall()]
    conn.close()
    return runs
