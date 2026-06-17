"""Repository-wide pytest fixtures."""

from __future__ import annotations

import os

import pytest
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication


@pytest.fixture(scope="session")
def qapp():
    """Create a QApplication for tests that need Qt widgets."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture(autouse=True)
def _disable_onboarding(qapp):
    """Disable onboarding dialogs for tests by default."""
    settings = QSettings("SignKit", "DesktopApp")
    settings.setValue("onboarding/show_on_startup", False)
    yield
