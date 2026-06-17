"""Pure-Python PDF annotation helpers built on pypdf."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple
import uuid

try:
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import (
        ArrayObject,
        BooleanObject,
        DictionaryObject,
        FloatObject,
        NameObject,
        NumberObject,
        RectangleObject,
        TextStringObject,
    )

    PYPDF_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency path
    PdfReader = PdfWriter = object  # type: ignore[assignment]
    ArrayObject = BooleanObject = DictionaryObject = FloatObject = NameObject = NumberObject = RectangleObject = TextStringObject = object  # type: ignore[assignment]
    PYPDF_AVAILABLE = False


@dataclass(frozen=True)
class PdfAnnotationSpec:
    """One annotation request in PDF page coordinates."""

    page_index: int
    kind: str
    x: float
    y: float
    width: float
    height: float
    contents: str = ""
    author: str = ""
    color: Tuple[float, float, float] = (1.0, 1.0, 0.0)
    opacity: float = 0.2


@dataclass(frozen=True)
class PdfAnnotationResult:
    """Outcome of an annotation write operation."""

    output_path: str
    annotation_ids: Tuple[str, ...]
    annotation_count: int


class PdfAnnotationEditor:
    """Append review annotations to a PDF while preserving the document body."""

    def __init__(self, input_pdf_path: str):
        if not Path(input_pdf_path).exists():
            raise FileNotFoundError(f"PDF not found: {input_pdf_path}")
        self.input_pdf_path = input_pdf_path

    def add_highlight(
        self,
        output_path: str,
        *,
        page_index: int,
        x: float,
        y: float,
        width: float,
        height: float,
        contents: str = "",
        author: str = "",
        color: Tuple[float, float, float] = (1.0, 1.0, 0.0),
    ) -> PdfAnnotationResult:
        spec = PdfAnnotationSpec(
            page_index=page_index,
            kind="highlight",
            x=x,
            y=y,
            width=width,
            height=height,
            contents=contents,
            author=author,
            color=color,
        )
        return self.apply(output_path, [spec])

    def add_note(
        self,
        output_path: str,
        *,
        page_index: int,
        x: float,
        y: float,
        contents: str,
        author: str = "",
        width: float = 18.0,
        height: float = 18.0,
    ) -> PdfAnnotationResult:
        spec = PdfAnnotationSpec(
            page_index=page_index,
            kind="note",
            x=x,
            y=y,
            width=width,
            height=height,
            contents=contents,
            author=author,
            color=(1.0, 1.0, 0.0),
        )
        return self.apply(output_path, [spec])

    def apply(self, output_path: str, annotations: Sequence[PdfAnnotationSpec]) -> PdfAnnotationResult:
        if not PYPDF_AVAILABLE:
            raise RuntimeError("pypdf is not available for PDF annotations")
        if not annotations:
            raise ValueError("At least one annotation is required")

        reader = PdfReader(self.input_pdf_path)  # type: ignore[call-arg]
        writer = PdfWriter()  # type: ignore[call-arg]

        for page in reader.pages:
            writer.add_page(page)

        if getattr(reader, "metadata", None):
            try:
                writer.add_metadata({k: str(v) for k, v in reader.metadata.items() if v is not None})
            except Exception:
                pass

        annotation_ids: list[str] = []
        for spec in annotations:
            if spec.page_index < 0 or spec.page_index >= len(writer.pages):
                continue
            annot_id = self._append_annotation(writer, spec)
            if annot_id:
                annotation_ids.append(annot_id)

        with open(output_path, "wb") as out:
            writer.write(out)

        return PdfAnnotationResult(
            output_path=output_path,
            annotation_ids=tuple(annotation_ids),
            annotation_count=len(annotation_ids),
        )

    def _append_annotation(self, writer: PdfWriter, spec: PdfAnnotationSpec) -> str:
        page = writer.pages[spec.page_index]
        annotation_id = uuid.uuid4().hex

        rect = RectangleObject(
            [
                FloatObject(spec.x),
                FloatObject(spec.y),
                FloatObject(spec.x + max(spec.width, 1.0)),
                FloatObject(spec.y + max(spec.height, 1.0)),
            ]
        )

        annotation = DictionaryObject()
        annotation[NameObject("/Type")] = NameObject("/Annot")
        annotation[NameObject("/Rect")] = rect
        annotation[NameObject("/NM")] = TextStringObject(annotation_id)
        annotation[NameObject("/M")] = TextStringObject(self._pdf_date())
        annotation[NameObject("/F")] = NumberObject(4)

        if spec.author:
            annotation[NameObject("/T")] = TextStringObject(spec.author)
        if spec.contents:
            annotation[NameObject("/Contents")] = TextStringObject(spec.contents)
        if spec.color:
            annotation[NameObject("/C")] = ArrayObject([FloatObject(v) for v in spec.color])

        if spec.kind == "highlight":
            annotation[NameObject("/Subtype")] = NameObject("/Highlight")
            annotation[NameObject("/QuadPoints")] = ArrayObject(
                [
                    FloatObject(spec.x),
                    FloatObject(spec.y + spec.height),
                    FloatObject(spec.x + spec.width),
                    FloatObject(spec.y + spec.height),
                    FloatObject(spec.x),
                    FloatObject(spec.y),
                    FloatObject(spec.x + spec.width),
                    FloatObject(spec.y),
                ]
            )
            annotation[NameObject("/CA")] = FloatObject(max(0.05, min(spec.opacity, 1.0)))
        elif spec.kind == "note":
            annotation[NameObject("/Subtype")] = NameObject("/Text")
            annotation[NameObject("/Name")] = NameObject("/Note")
            annotation[NameObject("/Open")] = BooleanObject(False)
        else:
            annotation[NameObject("/Subtype")] = NameObject("/Text")
            annotation[NameObject("/Name")] = NameObject("/Note")
            annotation[NameObject("/Open")] = BooleanObject(False)

        annotation_ref = writer._add_object(annotation)
        annots = self._ensure_annots_array(page)
        annots.append(annotation_ref)
        page[NameObject("/Annots")] = annots
        return annotation_id

    def _ensure_annots_array(self, page) -> ArrayObject:
        annots = page.get(NameObject("/Annots"))
        if annots is None:
            return ArrayObject()

        try:
            return annots.get_object()
        except Exception:
            return annots

    def _pdf_date(self) -> str:
        now = datetime.now(timezone.utc)
        return now.strftime("D:%Y%m%d%H%M%S+00'00'")
