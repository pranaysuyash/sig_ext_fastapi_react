from __future__ import annotations

import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect


class GlassPanel(QWidget):
    """Semi-transparent panel with a subtle shadow to mimic glassmorphism."""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("glassPanel")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # Enhanced shadow for better visual depth
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(32)
        shadow.setOffset(0, 16)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(shadow)
        
        # Apply platform-appropriate styling with enhanced glassmorphism
        if sys.platform == "darwin":
            # On macOS, use more translucent background for better glassmorphism effect
            # Use different styling based on dark/light mode detection
            from PySide6.QtWidgets import QApplication
            app = QApplication.instance()
            if app:
                palette = app.palette()
                # Detect dark mode
                window_color = palette.color(palette.currentColorGroup(), QPalette.ColorRole.Window)
                is_dark_mode = window_color.lightness() < 128
                if is_dark_mode:
                    # Dark mode: very translucent with subtle border
                    self.setStyleSheet(
                        """
                        QWidget#glassPanel {
                            background-color: rgba(255, 255, 255, 12);
                            border: 1px solid rgba(255, 255, 255, 25);
                            border-radius: 16px;
                        }
                        """
                    )
                else:
                    # Light mode: slightly more opaque but still glassy
                    self.setStyleSheet(
                        """
                        QWidget#glassPanel {
                            background-color: rgba(255, 255, 255, 18);
                            border: 1px solid rgba(255, 255, 255, 30);
                            border-radius: 16px;
                        }
                        """
                    )
            else:
                # Fallback
                self.setStyleSheet(
                    """
                    QWidget#glassPanel {
                        background-color: rgba(255, 255, 255, 15);
                        border: 1px solid rgba(255, 255, 255, 30);
                        border-radius: 16px;
                    }
                    """
                )
        else:
            # On other platforms, use more solid styling
            self.setStyleSheet(
                """
                QWidget#glassPanel {
                    background-color: rgba(240, 240, 240, 80);
                    border: 1px solid rgba(200, 200, 200, 80);
                    border-radius: 16px;
                }
                """
            )
