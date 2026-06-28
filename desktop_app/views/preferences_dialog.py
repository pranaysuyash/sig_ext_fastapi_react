from __future__ import annotations

from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QVBoxLayout,
    QLabel,
)


class PreferencesDialog(QDialog):
    """Lightweight app preferences for the current SignKit macOS surface."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Preferences")
        self.setModal(True)
        self.setMinimumWidth(420)

        settings = QSettings("SignKit", "DesktopApp")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        title = QLabel("SignKit Preferences")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(title)

        description = QLabel(
            "Keep the app aligned with macOS conventions and control the few app-level behaviors "
            "that benefit from a persistent preference."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: palette(mid);")
        layout.addWidget(description)

        self.onboarding_cb = QCheckBox("Show onboarding on startup")
        self.onboarding_cb.setChecked(
            settings.value("onboarding/show_on_startup", True, type=bool)
        )
        layout.addWidget(self.onboarding_cb)

        note = QLabel(
            "System shortcuts, menus, and window behavior follow the macOS defaults automatically."
        )
        note.setWordWrap(True)
        note.setStyleSheet("color: palette(mid);")
        layout.addWidget(note)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._save_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _save_and_accept(self) -> None:
        settings = QSettings("SignKit", "DesktopApp")
        settings.setValue("onboarding/show_on_startup", self.onboarding_cb.isChecked())
        self.accept()
