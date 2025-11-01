from __future__ import annotations

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from desktop_app.config import load_config
from desktop_app.state.session import SessionState
from desktop_app.api.client import ApiClient
from desktop_app.views.login_dialog import LoginDialog
from desktop_app.views.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    if sys.platform == "darwin":
        try:
            app.setStyle("macOS")
        except Exception:
            pass
        try:
            app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar, False)
        except AttributeError:
            pass

    # Set macOS menubar app name and metadata
    QApplication.setApplicationName("Signature Extractor")
    QApplication.setApplicationDisplayName("Signature Extractor")
    QApplication.setOrganizationName("Signature Tools")
    QApplication.setOrganizationDomain("signature-tools.local")

    cfg = load_config()
    session = SessionState()
    client = ApiClient(cfg.api_base_url, session)

    # By default, skip login dialog and go straight to main window
    win = MainWindow(client, session)
    win.resize(1200, 800)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
