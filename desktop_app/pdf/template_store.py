"""Template persistence for reusable PDF signature placements."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid


APP_DIR = os.path.join(os.path.expanduser("~"), ".signature_extractor")
TEMPLATES_FILE = os.path.join(APP_DIR, "pdf_templates.json")
_TEMPLATE_VERSION = 1


@dataclass
class SignaturePlacementTemplate:
    """Reusable signature placement for one or many pages."""

    template_id: str
    name: str
    signature_path: str
    page_index: int
    x_ratio: float
    y_ratio: float
    width_ratio: float
    height_ratio: float
    use_field_anchor: bool = False
    field_type: Optional[str] = None
    field_label: Optional[str] = None
    field_confidence: Optional[float] = None
    anchor_x_ratio: Optional[float] = None
    anchor_y_ratio: Optional[float] = None
    source_pdf_name: Optional[str] = None
    source_pdf_path: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


def ensure_templates_dir() -> str:
    """Ensure template directory exists."""
    Path(APP_DIR).mkdir(parents=True, exist_ok=True)
    return APP_DIR


def _load_payload() -> Dict[str, Any]:
    """Load raw JSON payload safely."""
    ensure_templates_dir()
    if not os.path.exists(TEMPLATES_FILE):
        return {"version": _TEMPLATE_VERSION, "templates": []}

    try:
        with open(TEMPLATES_FILE, "r", encoding="utf-8") as f:
            payload = json.load(f)
    except Exception:
        return {"version": _TEMPLATE_VERSION, "templates": []}

    if not isinstance(payload, dict):
        return {"version": _TEMPLATE_VERSION, "templates": []}

    payload.setdefault("version", _TEMPLATE_VERSION)
    payload.setdefault("templates", [])
    return payload


def _write_payload(payload: Dict[str, Any]) -> None:
    """Write payload and fail softly in best-effort mode."""
    ensure_templates_dir()
    try:
        with open(TEMPLATES_FILE, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, sort_keys=True)
    except Exception:
        return


def _clamp_ratio(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _coerce_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in {"1", "true", "yes", "y", "on"}
    return default


def _coerce_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _coerce_optional_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _coerce_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_template(payload: Dict[str, Any]) -> SignaturePlacementTemplate:
    """Build a strict template from possibly older payloads."""
    return SignaturePlacementTemplate(
        template_id=str(payload.get("template_id") or uuid.uuid4().hex),
        name=str(payload.get("name") or "Unnamed Template"),
        signature_path=str(payload.get("signature_path") or ""),
        page_index=_coerce_int(payload.get("page_index"), 0),
        x_ratio=_clamp_ratio(_coerce_float(payload.get("x_ratio"), 0.0)),
        y_ratio=_clamp_ratio(_coerce_float(payload.get("y_ratio"), 0.0)),
        width_ratio=_clamp_ratio(_coerce_float(payload.get("width_ratio"), 0.0)),
        height_ratio=_clamp_ratio(_coerce_float(payload.get("height_ratio"), 0.0)),
        use_field_anchor=_coerce_bool(payload.get("use_field_anchor"), False),
        field_type=_normalize_optional_text(payload.get("field_type")),
        field_label=_normalize_optional_text(payload.get("field_label")),
        field_confidence=_coerce_optional_float(payload.get("field_confidence")),
        anchor_x_ratio=_coerce_optional_float(payload.get("anchor_x_ratio")),
        anchor_y_ratio=_coerce_optional_float(payload.get("anchor_y_ratio")),
        source_pdf_name=_normalize_optional_text(payload.get("source_pdf_name")),
        source_pdf_path=_normalize_optional_text(payload.get("source_pdf_path")),
        created_at=str(payload.get("created_at") or datetime.utcnow().isoformat()),
        updated_at=str(payload.get("updated_at") or datetime.utcnow().isoformat()),
    )


def _normalize_optional_text(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _safe_templates_payload() -> Dict[str, Any]:
    payload = _load_payload()
    templates = payload.get("templates")
    if not isinstance(templates, list):
        payload["templates"] = []
    return payload


def list_templates() -> List[SignaturePlacementTemplate]:
    """Return saved templates in newest-first order."""
    payload = _safe_templates_payload()
    templates = []
    for item in payload.get("templates", []):
        if not isinstance(item, dict):
            continue
        templates.append(_as_template(item))
    templates.sort(key=lambda item: item.updated_at, reverse=True)
    return templates


def get_template(template_id: str) -> Optional[SignaturePlacementTemplate]:
    """Return a template by id."""
    for template in list_templates():
        if template.template_id == template_id:
            return template
    return None


def save_template(template: SignaturePlacementTemplate) -> SignaturePlacementTemplate:
    """Save or update a template."""
    payload = _safe_templates_payload()
    now = datetime.utcnow().isoformat()
    to_save = asdict(template)
    to_save["updated_at"] = now
    if not to_save.get("created_at"):
        to_save["created_at"] = now
    if not to_save.get("template_id"):
        to_save["template_id"] = uuid.uuid4().hex

    exists = False
    entries = payload["templates"]
    for index, item in enumerate(entries):
        if isinstance(item, dict) and item.get("template_id") == to_save["template_id"]:
            entries[index] = to_save
            exists = True
            break
    if not exists:
        entries.append(to_save)

    _write_payload(payload)
    return _as_template(to_save)


def create_template(
    *,
    signature_path: str,
    page_index: int,
    x_ratio: float,
    y_ratio: float,
    width_ratio: float,
    height_ratio: float,
    name: str,
    use_field_anchor: bool = False,
    field_type: Optional[str] = None,
    field_label: Optional[str] = None,
    field_confidence: Optional[float] = None,
    anchor_x_ratio: Optional[float] = None,
    anchor_y_ratio: Optional[float] = None,
    source_pdf_path: Optional[str] = None,
    source_pdf_name: Optional[str] = None,
) -> SignaturePlacementTemplate:
    """Create and persist a placement template."""
    template = SignaturePlacementTemplate(
        template_id=uuid.uuid4().hex,
        name=name.strip() or "Signature Template",
        signature_path=signature_path,
        page_index=_coerce_int(page_index, 0),
        x_ratio=_clamp_ratio(x_ratio),
        y_ratio=_clamp_ratio(y_ratio),
        width_ratio=_clamp_ratio(width_ratio),
        height_ratio=_clamp_ratio(height_ratio),
        use_field_anchor=_coerce_bool(use_field_anchor, False),
        field_type=_normalize_optional_text(field_type),
        field_label=_normalize_optional_text(field_label),
        field_confidence=_coerce_optional_float(field_confidence),
        anchor_x_ratio=_coerce_optional_float(anchor_x_ratio),
        anchor_y_ratio=_coerce_optional_float(anchor_y_ratio),
    )
    template.source_pdf_path = _normalize_optional_text(source_pdf_path)
    template.source_pdf_name = _normalize_optional_text(source_pdf_name)
    template.created_at = datetime.utcnow().isoformat()
    template.updated_at = template.created_at
    return save_template(template)


def delete_template(template_id: str) -> bool:
    """Delete a template by id."""
    payload = _safe_templates_payload()
    before = len(payload["templates"])
    payload["templates"] = [
        item for item in payload["templates"]
        if not (isinstance(item, dict) and item.get("template_id") == template_id)
    ]
    deleted = len(payload["templates"]) < before
    if deleted:
        _write_payload(payload)
    return deleted

