from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
)

from desktop_app.license.storage import save_license


class LicenseDialog(QDialog):
    """Simple dialog to enter and save a license key (and optional email)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter License")
        self.setModal(True)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Paste your license key:"))
        self.key_edit = QLineEdit(self)
        self.key_edit.setPlaceholderText("XXXX-XXXX-XXXX or any provided key")
        layout.addWidget(self.key_edit)

        layout.addWidget(QLabel("Email (optional):"))
        self.email_edit = QLineEdit(self)
        self.email_edit.setPlaceholderText("you@example.com")
        layout.addWidget(self.email_edit)

        btn_row = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.ok_btn = QPushButton("Activate")
        self.ok_btn.setDefault(True)
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.ok_btn)
        layout.addLayout(btn_row)

        self.cancel_btn.clicked.connect(self.reject)
        self.ok_btn.clicked.connect(self._on_activate)

        self.resize(420, 160)

    def _on_activate(self):
        key = (self.key_edit.text() or "").strip()
        email = (self.email_edit.text() or "").strip() or None
        if not key:
            # Keep it simple: require non-empty key for MVP
            self.key_edit.setFocus()
            return
        save_license(key, email)
        self.accept()
