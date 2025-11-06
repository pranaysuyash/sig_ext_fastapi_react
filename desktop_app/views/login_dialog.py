from __future__ import annotations

import sys
from typing import cast, Optional

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox, QWidget

from desktop_app.widgets.modern_mac_button import ModernMacButton


def _create_button(
    text: str = "",
    parent: Optional[QWidget] = None,
    *,
    use_modern_mac: Optional[bool] = None,
    primary: bool = False,
    color: str = 'blue',
    compact: bool = False  # Dialog buttons are typically not compact
) -> QPushButton:
    """Create a button, using ModernMacButton on macOS if available and requested.

    Args:
        text: Button text
        parent: Parent widget
        use_modern_mac: Force modern button (default: auto-detect macOS)
        primary: True for primary action buttons (colored)
        color: One of 'blue', 'purple', 'pink', 'red', 'orange', 'yellow', 'green', 'teal'
        compact: True for smaller buttons (sidebar/toolbar), False for larger (dialogs)
    """
    if use_modern_mac is None:
        use_modern_mac = sys.platform == "darwin"

    if use_modern_mac:
        try:
            btn = ModernMacButton(
                text, parent,
                primary=primary,
                color=color,
                glass=True,
                compact=compact
            )
            return btn
        except (NameError, TypeError):
            # Fallback if ModernMacButton not available or doesn't support compact
            pass

    # Default to standard QPushButton
    return QPushButton(text, parent)


class LoginDialog(QDialog):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("Login")
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Email"))
        self.email = QLineEdit(self)
        self.email.setPlaceholderText("email@example.com")
        layout.addWidget(self.email)

        layout.addWidget(QLabel("Password"))
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        self.login_btn = _create_button("Login", self, primary=True)
        self.login_btn.clicked.connect(self._on_login)
        layout.addWidget(self.login_btn)

    def _on_login(self):
        username = self.email.text().strip()
        pwd = self.password.text()
        if not username or not pwd:
            QMessageBox.warning(self, "Missing fields", "Please enter email and password")
            return
        try:
            self.api_client.login(username, pwd)
            self.accept()
        except Exception as e:
            cls = e.__class__
            mod = getattr(cls, "__module__", "")
            name = getattr(cls, "__name__", "")
            if mod.startswith("requests") and name in {"ConnectionError", "Timeout"}:
                base_url = getattr(self.api_client, "base_url", "http://127.0.0.1:8001")
                msg = (
                    f"The backend at {base_url} is unreachable.\n\n"
                    "Please start the server and try again."
                )
                QMessageBox.critical(self, "Login failed", msg)
            else:
                QMessageBox.critical(self, "Login failed", str(e))
