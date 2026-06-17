"""Tests for the PDF annotation editor."""

from pathlib import Path

import pytest


pytest.importorskip("pypdf")

from pypdf import PdfReader, PdfWriter  # noqa: E402

from desktop_app.pdf.annotations import PdfAnnotationEditor  # noqa: E402


def _make_blank_pdf(path: Path) -> None:
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    with path.open("wb") as handle:
        writer.write(handle)


def _annotation_list(page):
    annots = page.get("/Annots")
    if annots is None:
        return None
    try:
        return annots.get_object()
    except Exception:
        return annots


def test_add_highlight_annotation(tmp_path):
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    _make_blank_pdf(input_pdf)

    editor = PdfAnnotationEditor(str(input_pdf))
    result = editor.add_highlight(
        str(output_pdf),
        page_index=0,
        x=72,
        y=144,
        width=120,
        height=24,
        contents="Selected field highlight",
        author="tester",
    )

    assert result.output_path == str(output_pdf)
    assert result.annotation_count == 1

    reader = PdfReader(str(output_pdf))
    annots = _annotation_list(reader.pages[0])
    assert annots is not None
    assert len(annots) == 1


def test_add_note_annotation(tmp_path):
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    _make_blank_pdf(input_pdf)

    editor = PdfAnnotationEditor(str(input_pdf))
    result = editor.add_note(
        str(output_pdf),
        page_index=0,
        x=90,
        y=200,
        contents="Add a review comment",
        author="tester",
    )

    assert result.output_path == str(output_pdf)
    assert result.annotation_count == 1

    reader = PdfReader(str(output_pdf))
    annots = _annotation_list(reader.pages[0])
    assert annots is not None
    assert len(annots) == 1
