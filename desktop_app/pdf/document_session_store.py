"""Persistence for per-document PDF placement sessions.

This keeps signature placements durable across app restarts so export can work
later, not just in the live viewer session.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


APP_DIR = Path.home() / ".signature_extractor"
SESSIONS_FILE = APP_DIR / "pdf_document_sessions.json"
_VERSION = 1


@dataclass(frozen=True)
class DocumentPlacementSession:
    """Durable PDF placement manifest for one source document."""

    pdf_path: str
    pdf_name: str
    file_size: Optional[int]
    modified_ns: Optional[int]
    placements: List[Dict[str, Any]]
    updated_at: str


def _ensure_dir() -> None:
    APP_DIR.mkdir(parents=True, exist_ok=True)


def _load_payload() -> Dict[str, Any]:
    _ensure_dir()
    if not SESSIONS_FILE.exists():
        return {"version": _VERSION, "documents": []}
    try:
        with SESSIONS_FILE.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except Exception:
        return {"version": _VERSION, "documents": []}

    if not isinstance(payload, dict):
        return {"version": _VERSION, "documents": []}
    payload.setdefault("version", _VERSION)
    payload.setdefault("documents", [])
    return payload


def _write_payload(payload: Dict[str, Any]) -> None:
    _ensure_dir()
    tmp_path = SESSIONS_FILE.with_suffix(".json.tmp")
    with tmp_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
    os.replace(tmp_path, SESSIONS_FILE)


def _stat_pdf(pdf_path: str) -> tuple[Optional[int], Optional[int]]:
    try:
        stat = Path(pdf_path).stat()
        return stat.st_size, stat.st_mtime_ns
    except Exception:
        return None, None


def save_document_session(pdf_path: str, placements: List[Dict[str, Any]]) -> DocumentPlacementSession:
    """Persist the current placement manifest for a PDF."""
    payload = _load_payload()
    pdf_name = Path(pdf_path).name
    file_size, modified_ns = _stat_pdf(pdf_path)
    updated_at = datetime.now(timezone.utc).isoformat()

    session = DocumentPlacementSession(
        pdf_path=pdf_path,
        pdf_name=pdf_name,
        file_size=file_size,
        modified_ns=modified_ns,
        placements=list(placements),
        updated_at=updated_at,
    )
    serialized = asdict(session)

    documents = payload.get("documents", [])
    if not isinstance(documents, list):
        documents = []

    replaced = False
    for index, item in enumerate(documents):
        if isinstance(item, dict) and item.get("pdf_path") == pdf_path:
            documents[index] = serialized
            replaced = True
            break

    if not replaced:
        documents.append(serialized)

    payload["documents"] = documents
    _write_payload(payload)
    return session


def load_document_session(pdf_path: str) -> List[Dict[str, Any]]:
    """Load persisted placements for a PDF when its file identity still matches."""
    payload = _load_payload()
    documents = payload.get("documents", [])
    if not isinstance(documents, list):
        return []

    file_size, modified_ns = _stat_pdf(pdf_path)
    for item in documents:
        if not isinstance(item, dict):
            continue
        if item.get("pdf_path") != pdf_path:
            continue

        stored_size = item.get("file_size")
        stored_mtime = item.get("modified_ns")
        if stored_size is not None and file_size is not None and stored_size != file_size:
            return []
        if stored_mtime is not None and modified_ns is not None and stored_mtime != modified_ns:
            return []

        placements = item.get("placements", [])
        if isinstance(placements, list):
            return [entry for entry in placements if isinstance(entry, dict)]
        return []

    return []


def clear_document_session(pdf_path: str) -> bool:
    """Remove persisted placements for a PDF."""
    payload = _load_payload()
    documents = payload.get("documents", [])
    if not isinstance(documents, list):
        return False

    before = len(documents)
    payload["documents"] = [item for item in documents if not (isinstance(item, dict) and item.get("pdf_path") == pdf_path)]
    if len(payload["documents"]) == before:
        return False

    _write_payload(payload)
    return True
