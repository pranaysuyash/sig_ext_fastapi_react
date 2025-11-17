from __future__ import annotations

import os
import sys

# CRITICAL: Set macOS environment variables BEFORE importing QApplication
# This ensures Qt picks them up during initialization
os.environ.setdefault("QT_MAC_APPLICATION_NAME", "SignKit")
os.environ.setdefault("QT_MAC_WANTS_LAYER", "1")  # Enable layer-backed views

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from desktop_app.config import load_config
from desktop_app.state.session import SessionState
from desktop_app.api.client import ApiClient
from desktop_app.backend_manager import BackendManager
from desktop_app.views.login_dialog import LoginDialog
from desktop_app.views.main_window import MainWindow


def _configure_app_identity() -> None:
    """Configure application metadata for macOS menubar and About dialog."""
    QApplication.setOrganizationName("SignKit")
    QApplication.setOrganizationDomain("signkit.work")
    QApplication.setApplicationName("SignKit")
    QApplication.setApplicationDisplayName("SignKit")


def _resource_path(relative: str) -> str:
    """Get absolute path to resource, works for dev and PyInstaller bundle."""
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(base_path, relative)


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
    app.setOrganizationName("SignKit")
    app.setOrganizationDomain("signkit.work")
    app.setApplicationName("SignKit")
    app.setApplicationDisplayName("SignKit")
    try:
        app.setDesktopFileName("SignKit")
    except AttributeError:
        pass

    # Set application/dock icon from assets if available
    icon_paths = [
        "assets/files/signkit_icon_512x512.png",
        "assets/files/signkit_icon_256x256.png",
        "assets/files/signkit_icon_128x128.png",
    ]
    for rel in icon_paths:
        p = _resource_path(rel)
        if os.path.exists(p):
            app.setWindowIcon(QIcon(p))
            break

    cfg = load_config()
    session = SessionState()
    client = ApiClient(cfg.api_base_url, session)
    
    # Initialize backend manager for hybrid architecture
    backend_manager = BackendManager(port=8001, auto_start=True)
    
    # Try to start backend (non-blocking)
    backend_available = backend_manager.start()
    if backend_available:
        # Point client to the dynamically selected backend port
        client.base_url = f"http://127.0.0.1:{backend_manager.port}"
        print(f"Backend started successfully at {client.base_url} - cloud features enabled")
    else:
        print("Running in offline mode - core features available")

    # By default, skip login dialog and go straight to main window
    win = MainWindow(client, session, backend_manager)
    # Also set window icon explicitly
    for rel in icon_paths:
        p = _resource_path(rel)
        if os.path.exists(p):
            win.setWindowIcon(QIcon(p))
            break
    win.setMinimumSize(1000, 700)
    win.resize(1200, 800)
    win.show()
    
    # Ensure all UI updates are processed before starting the event loop
    app.processEvents()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
