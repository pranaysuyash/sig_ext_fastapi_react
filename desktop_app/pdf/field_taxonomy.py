"""Shared field taxonomy helpers for PDF parsing and form workflows."""

from __future__ import annotations

from typing import Optional


def normalize_field_kind(raw_value: object) -> str:
    """Return a canonical field kind label."""
    text = str(raw_value or "").strip().lower()
    if not text:
        return "unknown"

    compact = text.replace(" ", "_").replace("-", "_")
    mapping = {
        "/sig": "signature",
        "sig": "signature",
        "signature": "signature",
        "text": "text",
        "textfield": "text",
        "textbox": "text",
        "combo": "choice",
        "combobox": "choice",
        "choice": "choice",
        "listbox": "choice",
        "checkbox": "checkbox",
        "check_box": "checkbox",
        "btn": "checkbox",
        "radio": "radio",
        "radiobutton": "radio",
        "date": "date",
        "initial": "initials",
        "initials": "initials",
        "field_box": "field_box",
        "signature_box": "signature_box",
        "signature_line": "signature_line",
        "ocr_keyword_hint": "ocr_keyword_hint",
        "unknown": "unknown",
    }
    return mapping.get(compact, mapping.get(text, compact))


def field_family(kind: object) -> str:
    """Map a field kind to a broader family label."""
    canonical = normalize_field_kind(kind)
    if canonical in {"signature", "signature_box", "signature_line"}:
        return "signature"
    if canonical in {"text", "choice", "checkbox", "radio", "date", "initials"}:
        return "form"
    if canonical == "ocr_keyword_hint":
        return "heuristic_hint"
    if canonical == "field_box":
        return "heuristic_box"
    return "unknown"

