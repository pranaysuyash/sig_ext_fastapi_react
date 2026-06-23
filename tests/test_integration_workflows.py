"""Integration tests for major SignKit workflows.

Each test covers an end-to-end user journey through multiple modules,
verifying that components compose correctly in real usage.
"""

import io
import os
import tempfile
from pathlib import Path

import cv2
import numpy as np
import pytest
from PIL import Image

from desktop_app.processing.extractor import SignatureExtractor, SecurityValidator
from desktop_app.processing.vault import NotaryVault
from desktop_app.processing.watermark import WatermarkEngine
from desktop_app.pdf.signer import PDFSigner, sign_pdf

FIXTURES_DIR = Path(__file__).parent.parent / "desktop_app" / "tests" / "fixtures"


def _create_signature_image(width=400, height=200) -> str:
    """Create a synthetic signature image on white background and return its path."""
    img = np.ones((height, width, 3), dtype=np.uint8) * 255

    # Draw a wavy "signature" line in black
    pts = []
    for x in range(50, width - 50):
        y_offset = int(20 * np.sin(x / 15.0)) + height // 2
        pts.append([x, y_offset])
    pts_arr = np.array(pts, dtype=np.int32).reshape((-1, 1, 2))
    cv2.polylines(img, [pts_arr], isClosed=False, color=(0, 0, 0), thickness=3)

    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    cv2.imwrite(tmp.name, img)
    return tmp.name


@pytest.fixture
def signature_image():
    path = _create_signature_image()
    yield path
    os.unlink(path)


@pytest.fixture
def vault_dir():
    d = tempfile.mkdtemp(prefix="signkit_vault_test_")
    yield d
    import shutil
    shutil.rmtree(d, ignore_errors=True)


@pytest.fixture
def sample_pdf():
    path = FIXTURES_DIR / "sample.pdf"
    if not path.exists():
        pytest.skip(f"Sample PDF not found at {path}")
    return str(path)


# ---------------------------------------------------------------------------
# Workflow 1: Image → Extract → PNG bytes
# ---------------------------------------------------------------------------
class TestImageExtractWorkflow:
    """Load an image, create a session, select a region, get processed PNG."""

    def test_extract_produces_valid_transparent_png(self, signature_image):
        extractor = SignatureExtractor()
        session_id = extractor.create_session(signature_image)

        session = extractor.get_session(session_id)
        assert session is not None
        h, w = session.dimensions

        png_bytes = extractor.process_selection(
            session_id,
            x1=40, y1=40, x2=w - 40, y2=h - 40,
            threshold=128,
            color="#000000",
        )

        assert len(png_bytes) > 100
        img = Image.open(io.BytesIO(png_bytes))
        assert img.mode == "RGBA"
        assert img.size[0] > 0 and img.size[1] > 0

    def test_extract_with_auto_clean(self, signature_image):
        extractor = SignatureExtractor()
        session_id = extractor.create_session(signature_image)
        session = extractor.get_session(session_id)
        h, w = session.dimensions

        png_bytes = extractor.process_selection(
            session_id,
            x1=40, y1=40, x2=w - 40, y2=h - 40,
            threshold=128,
            color="#000000",
            auto_clean=True,
        )
        img = Image.open(io.BytesIO(png_bytes))
        assert img.mode == "RGBA"

    def test_extract_with_custom_color(self, signature_image):
        extractor = SignatureExtractor()
        session_id = extractor.create_session(signature_image)
        session = extractor.get_session(session_id)
        h, w = session.dimensions

        png_bytes = extractor.process_selection(
            session_id,
            x1=40, y1=40, x2=w - 40, y2=h - 40,
            threshold=128,
            color="#0000FF",
        )
        img = Image.open(io.BytesIO(png_bytes))
        arr = np.array(img)
        # Where alpha > 0, blue channel should dominate
        visible = arr[arr[:, :, 3] > 0]
        if len(visible) > 0:
            assert visible[:, 2].mean() > visible[:, 0].mean()  # B > R


# ---------------------------------------------------------------------------
# Workflow 2: Extract → Vault → Retrieve (encrypted round-trip)
# ---------------------------------------------------------------------------
class TestVaultRoundTripWorkflow:
    """Extract a signature, store it encrypted in the vault, retrieve it."""

    def test_store_and_retrieve_preserves_bytes(self, signature_image, vault_dir):
        extractor = SignatureExtractor()
        session_id = extractor.create_session(signature_image)
        session = extractor.get_session(session_id)
        h, w = session.dimensions

        png_bytes = extractor.process_selection(
            session_id,
            x1=40, y1=40, x2=w - 40, y2=h - 40,
            threshold=128,
            color="#000000",
        )

        vault = NotaryVault(vault_dir=vault_dir)
        sig_id = vault.store_signature(png_bytes, {"source": "test", "label": "my sig"})

        retrieved = vault.retrieve_signature(sig_id)
        assert retrieved == png_bytes

        sigs = vault.list_signatures()
        assert any(s["id"] == sig_id for s in sigs)

    def test_vault_delete_removes_blob(self, signature_image, vault_dir):
        extractor = SignatureExtractor()
        session_id = extractor.create_session(signature_image)
        session = extractor.get_session(session_id)
        h, w = session.dimensions

        png_bytes = extractor.process_selection(
            session_id, x1=40, y1=40, x2=w - 40, y2=h - 40,
            threshold=128, color="#000000",
        )

        vault = NotaryVault(vault_dir=vault_dir)
        sig_id = vault.store_signature(png_bytes, {"source": "test"})
        vault.delete_signature(sig_id)

        assert not (Path(vault_dir) / "blobs" / f"{sig_id}.enc").exists()
        with pytest.raises(ValueError):
            vault.retrieve_signature(sig_id)


# ---------------------------------------------------------------------------
# Workflow 3: Extract → Watermark → Verify (steganographic round-trip)
# ---------------------------------------------------------------------------
class TestWatermarkRoundTripWorkflow:
    """Extract a signature, embed a watermark, verify it survives."""

    def test_watermark_embeds_and_verifies(self, signature_image):
        extractor = SignatureExtractor()
        session_id = extractor.create_session(signature_image)
        session = extractor.get_session(session_id)
        h, w = session.dimensions

        png_bytes = extractor.process_selection(
            session_id,
            x1=40, y1=40, x2=w - 40, y2=h - 40,
            threshold=128,
            color="#000000",
        )

        engine = WatermarkEngine()
        meta = {"app": "SignKit", "user": "test@example.com", "version": "1.0"}
        watermarked = engine.embed_watermark(png_bytes, meta)

        assert len(watermarked) > 0
        recovered = engine.verify_watermark(watermarked)
        assert recovered is not None
        assert recovered["app"] == "SignKit"
        assert recovered["user"] == "test@example.com"


# ---------------------------------------------------------------------------
# Workflow 4: Full pipeline — Extract → Vault → PDF Sign → Save
# ---------------------------------------------------------------------------
class TestFullSigningPipeline:
    """End-to-end: extract signature from image, store in vault, sign a PDF."""

    def test_end_to_end_pdf_signing(self, signature_image, vault_dir, sample_pdf):
        # 1. Extract signature
        extractor = SignatureExtractor()
        session_id = extractor.create_session(signature_image)
        session = extractor.get_session(session_id)
        h, w = session.dimensions

        png_bytes = extractor.process_selection(
            session_id,
            x1=40, y1=40, x2=w - 40, y2=h - 40,
            threshold=128,
            color="#000000",
        )

        # 2. Store in vault
        vault = NotaryVault(vault_dir=vault_dir)
        sig_id = vault.store_signature(png_bytes, {"source": "integration_test"})

        # 3. Retrieve from vault and write to temp file for signer
        sig_bytes = vault.retrieve_signature(sig_id)
        sig_tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        sig_tmp.write(sig_bytes)
        sig_tmp.close()

        # 4. Sign the PDF
        output_pdf = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        output_pdf.close()

        try:
            success = sign_pdf(
                sample_pdf,
                output_pdf.name,
                signatures=[{
                    "page": 0,
                    "sig_path": sig_tmp.name,
                    "x": 100.0,
                    "y": 600.0,
                    "width": 150.0,
                    "height": 50.0,
                }],
            )
            assert success is True

            # Verify output PDF exists and is non-trivial
            output_size = os.path.getsize(output_pdf.name)
            input_size = os.path.getsize(sample_pdf)
            assert output_size > input_size * 0.5  # signed PDF should be comparable size
            assert output_size > 1000

        finally:
            os.unlink(sig_tmp.name)
            os.unlink(output_pdf.name)


# ---------------------------------------------------------------------------
# Workflow 5: Auto-detect signature region
# ---------------------------------------------------------------------------
class TestAutoDetectWorkflow:
    """Load an image containing a signature, auto-detect its bounding box."""

    def test_auto_detect_finds_region(self, signature_image):
        extractor = SignatureExtractor()
        session_id = extractor.create_session(signature_image)

        bbox = extractor.auto_detect_signature(session_id)
        assert bbox is not None
        x1, y1, x2, y2 = bbox
        assert x2 > x1
        assert y2 > y1

    def test_auto_detect_then_extract(self, signature_image):
        """Auto-detect → process the detected region → valid PNG."""
        extractor = SignatureExtractor()
        session_id = extractor.create_session(signature_image)

        bbox = extractor.auto_detect_signature(session_id)
        assert bbox is not None
        x1, y1, x2, y2 = bbox

        png_bytes = extractor.process_selection(
            session_id,
            x1=x1, y1=y1, x2=x2, y2=y2,
            threshold=128,
            color="#000000",
        )
        img = Image.open(io.BytesIO(png_bytes))
        assert img.mode == "RGBA"
        assert img.size[0] > 0


# ---------------------------------------------------------------------------
# Workflow 6: SVG export path
# ---------------------------------------------------------------------------
class TestSVGExportWorkflow:
    """Extract signature as SVG vector output."""

    def test_svg_export_produces_valid_svg(self, signature_image):
        extractor = SignatureExtractor()
        session_id = extractor.create_session(signature_image)
        session = extractor.get_session(session_id)
        h, w = session.dimensions

        svg_str = extractor.process_selection_svg(
            session_id,
            x1=40, y1=40, x2=w - 40, y2=h - 40,
            threshold=128,
            color="#000000",
        )
        assert svg_str.startswith("<?xml")
        assert "<svg" in svg_str
        assert "</svg>" in svg_str
        assert 'fill="#000000"' in svg_str


# ---------------------------------------------------------------------------
# Workflow 7: Quality analysis
# ---------------------------------------------------------------------------
class TestQualityAnalysisWorkflow:
    """Extract and analyze signature quality metrics."""

    def test_quality_analysis_returns_metrics(self, signature_image):
        extractor = SignatureExtractor()
        session_id = extractor.create_session(signature_image)
        session = extractor.get_session(session_id)
        h, w = session.dimensions

        result = extractor.analyze_quality(
            session_id,
            x1=40, y1=40, x2=w - 40, y2=h - 40,
        )
        assert "score" in result
        assert "rating" in result
        assert "issues" in result
        assert "metrics" in result
        assert 0 <= result["score"] <= 100
        assert result["rating"] in ("Excellent", "Good", "Poor")
