"""Custom widgets used in the extraction tab."""

from __future__ import annotations

import sys

from PySide6.QtGui import QFontMetrics
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton


class ElidingButton(QPushButton):
    """A QPushButton that elides text when it doesn't fit."""

    def __init__(self, text="", parent=None):
        if sys.platform == "darwin":
            try:
                from desktop_app.widgets.modern_mac_button import ModernMacButton
                ModernMacButton.__init__(self, text, parent)
                self._full_text = text
                return
            except (NameError, Exception):
                pass
        super().__init__(text, parent)
        self._full_text = text
        from PySide6.QtWidgets import QSizePolicy
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(30)
        if text:
            self.setToolTip(text)

    def setText(self, text):
        self._full_text = text
        super().setText(text)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._full_text:
            fm = QFontMetrics(self.font())
            elided = fm.elidedText(self._full_text, Qt.ElideRight, self.width() - 10)
            super().setText(elided)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
