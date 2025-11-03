from __future__ import annotations

import os
import sys

# CRITICAL: Set macOS environment variables BEFORE importing QApplication
# This ensures Qt picks them up during initialization
os.environ.setdefault("QT_MAC_APPLICATION_NAME", "Signature Extractor")
os.environ.setdefault("QT_MAC_WANTS_LAYER", "1")  # Enable layer-backed views

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from desktop_app.config import load_config
from desktop_app.state.session import SessionState
from desktop_app.api.client import ApiClient
from desktop_app.views.login_dialog import LoginDialog
from desktop_app.views.main_window import MainWindow


def _configure_app_identity() -> None:
    """Configure application metadata for macOS menubar and About dialog."""
    QApplication.setOrganizationName("Signature Tools")
    QApplication.setOrganizationDomain("signature-tools.local")
    QApplication.setApplicationName("Signature Extractor")
    QApplication.setApplicationDisplayName("Signature Extractor")


def main():
    _configure_app_identity()
    app = QApplication(sys.argv)

    if sys.platform == "darwin":
        # Use native macOS style
        try:
            app.setStyle("macOS")
        except Exception:
            pass

        # Enable native menu bar
        try:
            app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar, False)
        except AttributeError:
            pass

        # Set font rendering for better text on macOS
        from PySide6.QtGui import QFont
        app_font = app.font()
        app_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        app.setFont(app_font)

        # Listen to macOS system appearance changes (light/dark mode)
        from PySide6.QtGui import QPalette
        app.setStyleSheet("")  # Clear any forced styles to allow system palette

    # Reinforce metadata after QApplication construction (Qt caches some values)
    app.setOrganizationName("Signature Tools")
    app.setOrganizationDomain("signature-tools.local")
    app.setApplicationName("Signature Extractor")
    app.setApplicationDisplayName("Signature Extractor")
    try:
        app.setDesktopFileName("Signature Extractor")
    except AttributeError:
        pass

    cfg = load_config()
    session = SessionState()
    client = ApiClient(cfg.api_base_url, session)

    # By default, skip login dialog and go straight to main window
    win = MainWindow(client, session)
    win.setMinimumSize(1000, 700)
    win.resize(1200, 800)
    win.show()
    
    # Ensure all UI updates are processed before starting the event loop
    app.processEvents()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
