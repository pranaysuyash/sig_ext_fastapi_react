"""Shared fixtures for desktop_app tests."""

import os
import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings


@pytest.fixture(scope="session")
def qapp():
    """Create QApplication for the test session."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture(autouse=True)
def _disable_onboarding(qapp):
    """Disable onboarding dialog for all tests."""
    settings = QSettings("SignKit", "DesktopApp")
    settings.setValue("onboarding/show_on_startup", False)
    yield
