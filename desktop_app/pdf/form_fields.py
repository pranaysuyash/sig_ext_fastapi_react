"""Helpers for inspecting and editing native PDF form fields."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional, TYPE_CHECKING

from desktop_app.pdf.field_taxonomy import normalize_field_kind
from desktop_app.pdf.stack_profile import _is_fitz_allowed

if TYPE_CHECKING:
    import fitz


@dataclass(frozen=True)
class FormFieldCandidate:
    """A native PDF form field widget."""

    page_index: int
    field_name: str
    field_type: str
    value: str
    x: float
    y: float
    width: float
    height: float
    field_flags: int
    on_state: str = ""
    tooltip: str = ""
    choices: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "page_index": self.page_index,
            "field_name": self.field_name,
            "field_type": self.field_type,
            "value": self.value,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "field_flags": self.field_flags,
            "on_state": self.on_state,
            "tooltip": self.tooltip,
            "choices": list(self.choices),
        }


class PdfFormFieldEditor:
    """Inspect and edit native PDF form widgets with PyMuPDF."""

    def detect_pdf(self, pdf_path: str, page_index: Optional[int] = None) -> List[FormFieldCandidate]:
        fitz = self._require_fitz()
        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        candidates: list[FormFieldCandidate] = []
        doc = fitz.open(pdf_path)
        try:
            page_indexes = [page_index] if page_index is not None else list(range(doc.page_count))
            for idx in page_indexes:
                if idx < 0 or idx >= doc.page_count:
                    continue
                page = doc[idx]
                for widget in page.widgets() or []:
                    candidates.append(self._widget_to_candidate(idx, widget))
        finally:
            doc.close()
        return candidates

    def fill_field(
        self,
        pdf_path: str,
        output_path: str,
        field_name: str,
        value: str = "",
        signature_image_path: str = "",
    ) -> bool:
        fitz = self._require_fitz()
        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        doc = fitz.open(pdf_path)
        changed = False
        try:
            for page in doc:
                for widget in page.widgets() or []:
                    if widget.field_name != field_name:
                        continue
                    changed = self._apply_widget_value(page, widget, value, signature_image_path) or changed
            if changed:
                doc.save(output_path, deflate=True)
            return changed
        finally:
            doc.close()

    def _widget_to_candidate(self, page_index: int, widget: Any) -> FormFieldCandidate:
        rect = widget.rect
        on_state = ""
        try:
            on_state = str(widget.on_state() or "")
        except Exception:
            on_state = ""
        choices = tuple(str(choice) for choice in (widget.choice_values or []) if choice is not None)
        return FormFieldCandidate(
            page_index=page_index,
            field_name=widget.field_name or "",
            field_type=normalize_field_kind(widget.field_type_string or "Unknown"),
            value=str(widget.field_value or ""),
            x=float(rect.x0),
            y=float(rect.y0),
            width=float(rect.width),
            height=float(rect.height),
            field_flags=int(getattr(widget, "field_flags", 0) or 0),
            on_state=on_state,
            tooltip=str(getattr(widget, "field_label", "") or ""),
            choices=choices,
        )

    def _apply_widget_value(
        self,
        page: Any,
        widget: Any,
        value: str,
        signature_image_path: str,
    ) -> bool:
        field_type = (widget.field_type_string or "").strip().lower()
        if field_type in {"text", "combobox", "listbox"}:
            widget.field_value = value
            widget.update()
            return True

        if "check" in field_type:
            widget.field_value = widget.on_state() if self._truthy(value) else "Off"
            widget.update()
            return True

        if "radio" in field_type:
            selected = self._select_radio_state(widget, value)
            widget.field_value = selected if selected else "Off"
            widget.update()
            return True

        if "sig" in field_type or "signature" in field_type:
            if signature_image_path:
                page.insert_image(widget.rect, filename=signature_image_path, keep_proportion=True, overlay=True)
                widget.field_value = "Signed"
                widget.update()
                return True

        return False

    def _truthy(self, value: str) -> bool:
        normalized = value.strip().lower()
        return normalized in {"1", "true", "yes", "y", "on", "checked", "signed"}

    def _select_radio_state(self, widget: Any, value: str) -> str:
        """Choose the radio state to activate for a widget."""
        normalized = value.strip()
        if not normalized:
            return "Off"

        current_state = ""
        try:
            current_state = str(widget.on_state() or "")
        except Exception:
            current_state = ""

        if normalized.casefold() == current_state.casefold():
            return current_state
        if normalized.casefold() == str(widget.field_value or "").casefold():
            return current_state
        return "Off"

    def _require_fitz(self) -> Any:
        if not _is_fitz_allowed():
            raise RuntimeError(
                "PyMuPDF form editing is disabled by policy. Set SIGNKIT_ALLOW_PYMUPDF_SIGNING=1 to enable it for this session."
            )

        try:
            import fitz as fitz_module  # type: ignore
            return fitz_module
        except Exception as exc:
            raise RuntimeError(f"PyMuPDF is not available: {exc}") from exc
