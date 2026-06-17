"""Tests for the canonical PDF stack profile and install guidance."""

import importlib.util
import json

from pathlib import Path

from desktop_app.pdf import stack_profile


def _profile_with_mocks(monkeypatch, importable_modules):
    """Configure deterministic module availability for stack profile tests."""

    def fake_is_importable(module: str) -> bool:
        return module in importable_modules

    monkeypatch.setattr(stack_profile, "_is_importable", fake_is_importable)


def test_default_profile_prefers_pikepdf_without_fitz(monkeypatch, tmp_path):
    monkeypatch.setenv("SIGNKIT_ALLOW_PYMUPDF_SIGNING", "0")
    monkeypatch.setenv("SIGNKIT_PDF_SCAN_PREPROCESS", "0")
    monkeypatch.delenv("SIGNKIT_PDF_BACKEND_TELEMETRY_PATH", raising=False)
    monkeypatch.delenv("SIGNKIT_DISABLE_PDF_BACKEND_TELEMETRY", raising=False)

    _profile_with_mocks(monkeypatch, {"pypdfium2", "pypdf", "pikepdf", "cv2", "pytesseract"})

    profile = stack_profile.get_pdf_stack_profile()

    assert profile["primary"]["rendering"] == "pypdfium2"
    assert profile["primary"]["signing"] == "pikepdf"
    assert profile["primary"]["annotations"] == "pypdf"
    assert profile["primary"]["scan_preprocess"] == "basic-only"
    assert profile["fallback_order"]["signing"] == ["pikepdf"]
    assert profile["fallback_order"]["annotations"] == ["pypdf"]
    assert profile["packages"]["fitz"]["available"] is False


def test_opt_in_profile_allows_fitz_before_pikepdf(monkeypatch):
    monkeypatch.setenv("SIGNKIT_ALLOW_PYMUPDF_SIGNING", "true")
    _profile_with_mocks(monkeypatch, {"pypdfium2", "pypdf", "fitz", "pikepdf", "cv2", "pytesseract"})

    assert stack_profile.choose_signer_backend() == "fitz"
    assert stack_profile.signing_backend_report() == "fitz -> pikepdf"


def test_scan_preprocess_hint_profile_and_install_message(monkeypatch):
    monkeypatch.setenv("SIGNKIT_PDF_SCAN_PREPROCESS", "1")
    monkeypatch.setenv("SIGNKIT_ALLOW_PYMUPDF_SIGNING", "0")
    _profile_with_mocks(monkeypatch, {"pypdfium2", "pypdf", "pikepdf", "cv2"})

    profile = stack_profile.get_pdf_stack_profile()
    assert profile["primary"]["scan_preprocess"] == "opencv-ocr"
    assert stack_profile.stack_install_hint() == "pip install pypdf pytesseract"


def test_signing_backend_telemetry_logs_path(tmp_path, monkeypatch):
    telemetry_path = tmp_path / "pdf_backends.jsonl"
    monkeypatch.setenv("SIGNKIT_PDF_BACKEND_TELEMETRY_PATH", str(telemetry_path))
    monkeypatch.setenv("SIGNKIT_DISABLE_PDF_BACKEND_TELEMETRY", "0")

    stack_profile.record_signing_backend_telemetry(
        "pikepdf",
        source="tests",
        reason="unit-test",
        extra={"plan": "unit"},
    )

    assert telemetry_path.exists()
    payload = json.loads(telemetry_path.read_text(encoding="utf-8").splitlines()[-1])
    assert payload["backend"] == "pikepdf"
    assert payload["source"] == "tests"
    assert payload["reason"] == "unit-test"
    assert payload["extra"]["plan"] == "unit"


def test_live_profile_matches_installed_pdf_packages(monkeypatch):
    """Smoke-test the actual environment without any monkeypatching of imports."""
    monkeypatch.setenv("SIGNKIT_ALLOW_PYMUPDF_SIGNING", "0")
    monkeypatch.setenv("SIGNKIT_PDF_SCAN_PREPROCESS", "0")

    profile = stack_profile.get_pdf_stack_profile()

    for module_name, package_key in (
        ("pypdfium2", "pypdfium2"),
        ("pypdf", "pypdf"),
        ("pikepdf", "pikepdf"),
    ):
        expected = importlib.util.find_spec(module_name) is not None
        assert profile["packages"][package_key]["available"] is expected

    assert profile["packages"]["fitz"]["available"] is False
    assert profile["primary"]["rendering"] in {"pypdfium2", "unavailable"}
    assert profile["primary"]["annotations"] in {"pypdf", "unavailable"}
