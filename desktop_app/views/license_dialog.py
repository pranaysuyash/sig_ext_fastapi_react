from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
)
import sys
from typing import Optional

from desktop_app.license.storage import save_license
from desktop_app.widgets.modern_mac_button import ModernMacButton


def _create_button(
    text: str = "",
    parent: Optional[QDialog] = None,
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
        self.cancel_btn = _create_button("Cancel", self)
        self.ok_btn = _create_button("Activate", self, primary=True)
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
