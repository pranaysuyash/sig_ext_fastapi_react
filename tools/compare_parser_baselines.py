"""Compare parser outputs on the local benchmark corpus."""

from __future__ import annotations

import os
import importlib.util
import sys
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "desktop_app" / "pdf"
FIXTURES = ROOT / "desktop_app" / "tests" / "fixtures"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("SIGNKIT_ALLOW_PYMUPDF_SIGNING", "1")


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, PDF_DIR / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def summarize_pdf(path: Path) -> dict[str, object]:
    reader = PdfReader(str(path))
    text_pages = 0
    widget_count = 0
    images = 0
    for page in reader.pages:
        if (page.extract_text() or "").strip():
            text_pages += 1
        annots = page.get("/Annots") or []
        for annot in annots:
            try:
                obj = annot.get_object()
            except Exception:
                obj = annot
            if str(obj.get("/Subtype", "")) == "/Widget":
                widget_count += 1
        try:
            images += len(page.images)
        except Exception:
            pass
    return {
        "pages": len(reader.pages),
        "text_pages": text_pages,
        "widget_count": widget_count,
        "images": images,
    }


def main() -> None:
    field_detection = load_module("field_detection_compare", "field_detection.py")
    form_fields = load_module("form_fields_compare", "form_fields.py")
    parser_adapters = load_module("parser_adapters_compare", "parser_adapters.py")

    detector = field_detection.SignatureFieldDetector()
    form_editor = form_fields.PdfFormFieldEditor()
    liteparse_status = parser_adapters.LiteParseAdapter().status()
    managed_status = parser_adapters.ManagedParserAdapter().status()

    benchmark_paths = [
        ROOT / "assets" / "demo_document.pdf",
        FIXTURES / "sample.pdf",
        FIXTURES / "signed_output.pdf",
        FIXTURES / "native_form_benchmark.pdf",
        FIXTURES / "checkbox_heavy_benchmark.pdf",
        FIXTURES / "mixed_layout_benchmark.pdf",
        FIXTURES / "scan_like_benchmark.pdf",
    ]
    rows = []
    for path in benchmark_paths:
        if not path.exists():
            continue
        summary = summarize_pdf(path)
        sig_candidates = detector.detect_pdf(str(path))
        try:
            form_candidates = form_editor.detect_pdf(str(path))
        except Exception:
            form_candidates = []
        rows.append(
            {
                "file": path.name,
                **summary,
                "signature_candidates": len(sig_candidates),
                "acroform_candidates": len(form_candidates),
                "heuristic_candidates": sum(1 for c in sig_candidates if c.source != "acroform"),
            }
        )

    print("# Parser Baseline Comparison")
    print()
    print(f"- LiteParse module: {liteparse_status.available} ({liteparse_status.notes})")
    print(f"- Managed parser adapter: {managed_status.available} ({managed_status.notes})")
    print("- Current local baseline: pypdf + pikepdf + pypdfium2 + PyMuPDF(opt-in)")
    print()
    print("| file | pages | text_pages | widget_count | images | signature_candidates | acroform_candidates | heuristic_candidates |")
    print("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for row in rows:
        print(
            f"| {row['file']} | {row['pages']} | {row['text_pages']} | {row['widget_count']} | {row['images']} | "
            f"{row['signature_candidates']} | {row['acroform_candidates']} | {row['heuristic_candidates']} |"
        )


if __name__ == "__main__":
    main()
