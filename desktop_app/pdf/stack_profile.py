from __future__ import annotations

"""Canonical PDF library profile and capability routing policy.

This module is the single source of truth for which PDF package is used for
which task. The intent is explicit, additive, and long-term:

- Keep each dependency to one primary role.
- Document fallback behavior explicitly.
- Avoid duplicate paths and conflicting implementations.
"""

from dataclasses import dataclass
import json
import importlib
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class PDFPackageRole:
    """Describes one canonical library role in the pipeline."""

    library: str
    module: str
    purpose: str
    fallback_for: str
    notes: str


_LIBRARY_ROLES: List[PDFPackageRole] = [
    PDFPackageRole(
        library="pypdfium2",
        module="pypdfium2",
        purpose="High-fidelity PDF rendering in desktop viewer",
        fallback_for="rendering",
        notes="Preferred for performance and Apache-2.0/BSD licensing footprint.",
    ),
    PDFPackageRole(
        library="pypdf",
        module="pypdf",
        purpose="Pure-Python annotations, comments, and light structural PDF edits",
        fallback_for="annotations",
        notes="Commercial-safe default adapter for review annotations and PDF mutation.",
    ),
    PDFPackageRole(
        library="fitz",
        module="fitz",
        purpose="Image stamp insertion / signature overlays when available",
        fallback_for="signing",
        notes=(
            "Preferred signing implementation for robust image placement and form edits. "
            "Opt-in only by setting SIGNKIT_ALLOW_PYMUPDF_SIGNING=1 to keep OSS-first defaults."
        ),
    ),
    PDFPackageRole(
        library="pikepdf",
        module="pikepdf",
        purpose="Structural PDF edits and reliable fallback for missing PyMuPDF",
        fallback_for="signing",
        notes="Mandatory fallback for environments that cannot import fitz.",
    ),
    PDFPackageRole(
        library="tesseract+opencv stack (optional)",
        module="cv2",
        purpose="Scan normalization/OCR text hints for field detection (phase 2)",
        fallback_for="scan-preprocessing",
        notes=(
            "Optional dependency for scanned-document assist. "
            "Requires both cv2 and optional pytesseract when SIGNKIT_PDF_SCAN_PREPROCESS is enabled."
        ),
    ),
]


def _is_importable(module: str) -> bool:
    if not module:
        return False
    try:
        importlib.import_module(module)
        return True
    except Exception:
        return False


def _is_fitz_allowed() -> bool:
    """Allow opting out of PyMuPDF to keep open-source-only default policy."""
    return os.getenv("SIGNKIT_ALLOW_PYMUPDF_SIGNING", "false").strip().lower() in {"1", "true", "yes", "on"}


def _telemetry_file_path() -> Optional[Path]:
    custom = os.getenv("SIGNKIT_PDF_BACKEND_TELEMETRY_PATH")
    if custom:
        return Path(custom)
    return Path.home() / ".signature_extractor" / "telemetry" / "pdf_backends.jsonl"


def _telemetry_enabled() -> bool:
    return os.getenv("SIGNKIT_DISABLE_PDF_BACKEND_TELEMETRY", "false").strip().lower() not in {"1", "true", "yes", "on"}


def get_pdf_stack_profile() -> Dict[str, object]:
    """Return canonical stack capabilities and runtime availability."""
    package_status = {}
    scan_preprocess_enabled = is_scan_preprocess_enabled()

    for role in _LIBRARY_ROLES:
        if role.library == "fitz" and not _is_fitz_allowed():
            available = False
        elif role.library == "tesseract+opencv stack (optional)":
            if not scan_preprocess_enabled:
                available = False
            else:
                available = _is_importable(role.module)
        else:
            available = _is_importable(role.module)
        package_status[role.library] = {
            "module": role.module,
            "available": available,
            "purpose": role.purpose,
            "fallback_for": role.fallback_for,
            "notes": role.notes,
        }
    signing_stack = []
    if package_status.get("fitz", {}).get("available"):
        signing_stack.append("fitz")
    if package_status.get("pikepdf", {}).get("available"):
        signing_stack.append("pikepdf")

    annotation_stack = []
    if package_status.get("pypdf", {}).get("available"):
        annotation_stack.append("pypdf")

    return {
        "roles": [r.__dict__ for r in _LIBRARY_ROLES],
        "packages": package_status,
        "primary": {
            "rendering": "pypdfium2" if package_status.get("pypdfium2", {}).get("available") else "unavailable",
            "signing": signing_stack[0] if signing_stack else "unavailable",
            "annotations": annotation_stack[0] if annotation_stack else "unavailable",
            "scan_preprocess": "opencv-ocr" if package_status.get("tesseract+opencv stack (optional)", {}).get("available") else "basic-only",
        },
        "fallback_order": {
            "signing": signing_stack,
            "annotations": annotation_stack,
        },
    }


def choose_signer_backend() -> str:
    """Return the active signature backend name."""
    profile = get_pdf_stack_profile()
    return str(profile["primary"].get("signing", "unavailable"))


def record_signing_backend_telemetry(
    backend: str,
    *,
    source: str = "PDFSigner",
    reason: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    """Persist one-line backend telemetry for long-term reliability analysis."""
    if not _telemetry_enabled() or not backend or backend == "unavailable":
        return

    path = _telemetry_file_path()
    if path is None:
        return

    try:
        payload = {
            "ts": datetime.now(tz=timezone.utc).isoformat(),
            "backend": backend,
            "source": source,
            "reason": reason or "selected",
            "extra": extra or {},
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as out:
            out.write(json.dumps(payload) + "\n")
    except Exception:
        # Telemetry must never block runtime behavior
        return


def signing_backend_report() -> str:
    """One-line human-readable summary for UI/diagnostics."""
    profile = get_pdf_stack_profile()
    fallback_order = profile.get("fallback_order", {}).get("signing", [])
    if not fallback_order:
        return "Signing backend unavailable"
    return " -> ".join(str(item) for item in fallback_order)


def stack_install_hint() -> str:
    """User-facing dependency hint based on missing required packages."""
    profile = get_pdf_stack_profile()
    scan_preprocess_enabled = is_scan_preprocess_enabled()
    packages = profile.get("packages", {})
    if not isinstance(packages, dict):
        return "pip install pypdfium2 pypdf PyMuPDF pikepdf"

    required: List[str] = []
    if not bool(packages.get("pypdfium2", {}).get("available")):
        required.append("pypdfium2")
    if not bool(packages.get("pypdf", {}).get("available")):
        required.append("pypdf")
    if _is_fitz_allowed() and not bool(packages.get("fitz", {}).get("available")):
        required.append("PyMuPDF")
    if not bool(packages.get("pikepdf", {}).get("available")):
        required.append("pikepdf")
    if scan_preprocess_enabled and not _is_importable("cv2"):
        required.append("opencv-python")
        required.append("pytesseract")
    elif scan_preprocess_enabled and not _is_importable("pytesseract"):
        required.append("pytesseract")
    if not required:
        return "All required PDF packages are already installed"

    # De-duplicate while preserving order
    ordered_unique: List[str] = []
    for name in required:
        if name not in ordered_unique:
            ordered_unique.append(name)

    return f"pip install {' '.join(ordered_unique)}"


def is_scan_preprocess_enabled() -> bool:
    """Feature flag for scan/OCR-enhanced field detection.

    We keep this off by default to keep the baseline path minimal.
    """
    return os.getenv("SIGNKIT_PDF_SCAN_PREPROCESS", "false").strip().lower() in {"1", "true", "yes", "on", "scan"}
