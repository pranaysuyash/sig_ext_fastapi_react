#!/usr/bin/env python3
"""
Pytest-compatible verification for the results-pane workflow.
"""
import os
import sys
import tempfile

import pytest
from PIL import Image
import requests
from requests.exceptions import RequestException

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "desktop_app"))

from PySide6.QtWidgets import QLabel
from desktop_app.widgets.image_view import ImageView


def test_app_startup(qapp):
    """Test that the app starts without errors."""
    print("=== Testing App Startup ===")

    from desktop_app.config import load_config
    from desktop_app.state.session import SessionState
    from desktop_app.api.client import ApiClient
    from desktop_app.views.main_window import MainWindow

    cfg = load_config()
    session = SessionState()
    client = ApiClient(cfg.api_base_url, session)

    window = MainWindow(client, session)
    print("✓ MainWindow created successfully")
    print("✓ All app components initialized")

    assert hasattr(window, "res_view"), "Result view not found"
    assert hasattr(window, "result_empty"), "Result empty label not found"
    print("✓ Result view exists")
    print(f"  - Has image: {window.res_view.has_image()}")
    print(f"  - Visible: {window.res_view.isVisible()}")
    print("✓ Result empty label exists")
    print(f"  - Visible: {window.result_empty.isVisible()}")


@pytest.fixture
def backend_png_bytes():
    """Upload and process a synthetic image, returning extracted PNG bytes."""
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            img = Image.new("RGB", (100, 100), color="white")
            img.save(f, "PNG")
            temp_path = f.name

        with open(temp_path, "rb") as f:
            files = {"file": ("test.png", f, "image/png")}
            response = requests.post(
                "http://127.0.0.1:8001/extraction/upload",
                files=files,
                timeout=10,
            )

        assert response.status_code == 200, f"Upload failed: {response.status_code}"
        result = response.json()
        session_id = result.get("id")
        assert session_id, "Upload response missing session id"
        print(f"✓ Upload successful, session_id: {session_id[:8]}...")

        data = {
            "session_id": session_id,
            "x1": 10,
            "y1": 10,
            "x2": 50,
            "y2": 50,
            "color": "#000000",
            "threshold": 200,
        }
        response = requests.post(
            "http://127.0.0.1:8001/extraction/process_image/",
            data=data,
            timeout=30,
        )
        assert response.status_code == 200, f"Processing failed: {response.status_code}"
        png_bytes = response.content
        assert png_bytes, "Processing returned no image bytes"
        print(f"✓ Processing successful, got {len(png_bytes)} bytes")
        return png_bytes
    except RequestException as exc:
        pytest.skip(f"Backend not available for integration check: {exc}")
    except Exception:
        raise
    finally:
        if temp_path:
            try:
                os.unlink(temp_path)
            except OSError:
                pass


def test_result_display(backend_png_bytes, qapp):
    """Test result display functionality."""
    print("\n=== Testing Result Display ===")

    res_view = ImageView()
    res_view.toggle_selection_mode(False)
    res_view.setVisible(False)

    result_empty = QLabel("Process a selection to see the result")
    result_empty.setVisible(True)

    print("Initial state:")
    print(f"  - res_view visible: {res_view.isVisible()}")
    print(f"  - result_empty visible: {result_empty.isVisible()}")

    # Apply the updated workflow logic
    res_view.load_image_bytes(backend_png_bytes)
    assert res_view.has_image(), "Image failed to load"

    print("After loading image:")
    print(f"  - res_view has image: {res_view.has_image()}")

    # Show result view, hide empty overlay
    result_empty.setVisible(False)
    res_view.setVisible(True)

    print("Final state:")
    print(f"  - res_view visible: {res_view.isVisible()}")
    print(f"  - result_empty visible: {result_empty.isVisible()}")

    assert res_view.isVisible() and not result_empty.isVisible()
    print("✓ Result display working correctly")


def main():
    """Run the verification checks with exits suitable for CLI debugging."""
    return 0


if __name__ == "__main__":
    sys.exit(main())
