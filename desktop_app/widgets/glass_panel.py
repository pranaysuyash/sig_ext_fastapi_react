from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect


class GlassPanel(QWidget):
    """Semi-transparent panel with a subtle shadow to mimic glassmorphism."""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("glassPanel")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(32)
        shadow.setOffset(0, 16)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(shadow)
