from __future__ import annotations

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox


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

        self.login_btn = QPushButton("Login")
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
