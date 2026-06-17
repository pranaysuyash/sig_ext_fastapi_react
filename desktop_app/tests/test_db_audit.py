"""Tests for database-backed PDF audit run manifests."""
import pytest
import sqlite3

from desktop_app.pdf import db_audit


@pytest.fixture
def logger_db(tmp_path, monkeypatch):
    """Create a DatabaseAuditLogger that points to a temporary DB path."""
    db_file = tmp_path / "audit_logs.db"
    monkeypatch.setattr(db_audit, "DB_DIR", tmp_path)
    monkeypatch.setattr(db_audit, "DB_PATH", db_file)
    return db_audit.DatabaseAuditLogger(str(tmp_path / "sample.pdf"), "qa@example.com")


def test_audit_run_manifest_lifecycle(logger_db: db_audit.DatabaseAuditLogger):
    """Start and finish a run while logging child signature placements."""
    run_id = logger_db.start_run(
        "bulk_signature_placement",
        details="unit test run",
        page_count=2,
    )
    assert run_id == logger_db.active_run_id
    logger_db.log_place_signature(0, "/tmp/signature.png", 10, 20, 100, 50, run_id=run_id)
    logger_db.log_place_signature(1, "/tmp/signature.png", 12, 22, 100, 50, run_id=run_id)
    logger_db.finish_run(run_id, success=True, signature_count=2, details="unit test run complete")

    runs = db_audit.get_audit_runs_for_pdf(logger_db.pdf_path)
    assert any(run.run_id == run_id and run.signature_count == 2 for run in runs)

    logs = db_audit.get_audit_logs_for_pdf(logger_db.pdf_path)
    bulk_logs = [entry for entry in logs if entry.operation == "place_signature"]
    assert bulk_logs
    assert all(entry.run_id == run_id for entry in bulk_logs)
    assert bulk_logs[0].page_number in {0, 1}


def test_audit_log_includes_run_id_when_set_active(logger_db: db_audit.DatabaseAuditLogger):
    """Verify active-run logging assigns the run id automatically."""
    run_id = logger_db.start_run("single", page_count=1)
    logger_db.log_place_signature(0, "/tmp/signature.png", 1, 2, 3, 4)
    logger_db.finish_run(run_id, success=True)

    logs = db_audit.get_audit_logs_for_pdf(logger_db.pdf_path)
    assert any(entry.operation == "place_signature" and entry.run_id == run_id for entry in logs)


def test_get_audit_runs_for_pdf_returns_rows(logger_db: db_audit.DatabaseAuditLogger):
    """Ensure run retrieval returns run manifests for a PDF."""
    logger_db.start_run("single")
    runs = db_audit.get_audit_runs_for_pdf(logger_db.pdf_path)
    assert len(runs) >= 1


def test_migrates_legacy_audit_schema(tmp_path, monkeypatch):
    """Legacy tables should auto-upgrade to include run_id and run manifest table."""
    db_file = tmp_path / "audit_logs.db"
    monkeypatch.setattr(db_audit, "DB_DIR", tmp_path)
    monkeypatch.setattr(db_audit, "DB_PATH", db_file)

    with sqlite3.connect(str(db_file)) as conn:
        cur = conn.cursor()
        cur.execute(
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
                success BOOLEAN DEFAULT 1
            )
            '''
        )
        conn.commit()

    logger = db_audit.DatabaseAuditLogger(str(tmp_path / "legacy.pdf"), "qa@example.com")
    logger.log_open()

    with sqlite3.connect(str(db_file)) as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(pdf_audit_logs)")
        columns = {row[1] for row in cur.fetchall()}

    assert "run_id" in columns
    assert db_audit.get_audit_runs_for_pdf(logger.pdf_path) == []
