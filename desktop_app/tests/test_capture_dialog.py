from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QLabel, QPushButton

from desktop_app.views.main_window_parts.extraction import _SignatureCaptureDialog


class _FakeCamera:
    def __init__(self, frame):
        self._frame = frame
        self.released = False

    def read(self):
        return True, self._frame

    def release(self):
        self.released = True


class _FakeCv2:
    COLOR_GRAY2RGB = 1
    COLOR_BGR2RGB = 2
    COLOR_BGRA2RGBA = 3
    CAP_DSHOW = 4
    CAP_ANY = 5

    def cvtColor(self, frame, code):
        if code == self.COLOR_GRAY2RGB:
            return np.dstack([frame, frame, frame])
        if code in {self.COLOR_BGR2RGB, self.COLOR_BGRA2RGBA}:
            return frame
        raise ValueError(f"unsupported conversion code: {code}")


def _make_dialog(monkeypatch: pytest.MonkeyPatch) -> _SignatureCaptureDialog:
    monkeypatch.setattr(_SignatureCaptureDialog, "_start_camera", lambda self: None)
    dialog = _SignatureCaptureDialog()
    dialog._preview = QLabel()
    dialog._capture_button = QPushButton()
    dialog._last_error = None
    dialog._frame_errors = 0
    return dialog


def test_capture_dialog_handles_grayscale_frames(qapp, monkeypatch: pytest.MonkeyPatch) -> None:
    dialog = _make_dialog(monkeypatch)
    frame = np.zeros((24, 32), dtype=np.uint8)
    frame[4:20, 6:26] = 128
    dialog._cap = _FakeCamera(frame)
    dialog._cv2 = _FakeCv2()

    dialog._update_frame()

    assert dialog._last_error is None
    assert dialog._preview.pixmap() is not None
    assert not dialog._preview.pixmap().isNull()


def test_capture_dialog_survives_unsupported_frame_shapes(qapp, monkeypatch: pytest.MonkeyPatch) -> None:
    dialog = _make_dialog(monkeypatch)
    dialog._cap = _FakeCamera(np.zeros((12, 12, 5), dtype=np.uint8))
    dialog._cv2 = _FakeCv2()

    dialog._update_frame()

    assert dialog._last_error is not None
    assert "Camera preview failed" in dialog._last_error
    assert dialog._capture_button.isEnabled() is False
