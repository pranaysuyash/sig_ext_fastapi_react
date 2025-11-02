from __future__ import annotations

import sys
from typing import cast, Dict, Any

from PySide6.QtCore import QEvent
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication


class ThemeMixin:
    """Provides macOS-aware theming helpers for the main window."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_theme_state: Dict[str, Any] = {}
        self._supports_vibrancy = sys.platform == "darwin"

    def event(self, event: QEvent) -> bool:
        """Handle appearance changes live."""
        try:
            if event.type() in (QEvent.Type.ApplicationPaletteChange, QEvent.Type.StyleChange):
                # Reapply theme when system appearance changes
                self._apply_theme()
        except Exception:
            pass  # Prevent crashes from theme updates
        return super().event(event)  # type: ignore

    def _get_palette_colors(self, palette: QPalette) -> Dict[str, QColor]:
        """Extract colors from system palette."""
        # Get base colors
        try:
            window = palette.color(QPalette.ColorGroup.Active, QPalette.ColorRole.Window)
            base = palette.color(QPalette.ColorGroup.Active, QPalette.ColorRole.Base)
        except TypeError:
            window = palette.color(QPalette.ColorRole.Window)
            base = palette.color(QPalette.ColorRole.Base)

        if not window.isValid():
            window_brush = getattr(palette, "window", None)
            if callable(window_brush):
                window = window_brush().color()
            else:
                window = QColor(240, 240, 245)

        if not base.isValid():
            base = QColor(255, 255, 255)

        # Detect dark mode using perceptual luminance
        window_lum = (0.299 * window.red() + 0.587 * window.green() + 0.114 * window.blue())
        base_lum = (0.299 * base.red() + 0.587 * base.green() + 0.114 * base.blue())
        is_dark = (window_lum < 120) and (base_lum < 120)

        return {
            "window": window,
            "base": base,
            "text": palette.color(QPalette.ColorGroup.Active, QPalette.ColorRole.Text),
            "button": palette.color(QPalette.ColorGroup.Active, QPalette.ColorRole.Button),
            "highlight": palette.color(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight),
            "highlighted_text": palette.color(QPalette.ColorGroup.Active, QPalette.ColorRole.HighlightedText),
            "disabled_text": palette.color(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text),
            "tooltip_base": palette.color(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipBase),
            "tooltip_text": palette.color(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipText),
            "is_dark": QColor(0, 0, 0) if is_dark else QColor(255, 255, 255),
        }

    def _apply_theme(self) -> None:
        """Apply platform-aware styling, leaning on macOS defaults when available."""
        if sys.platform == "darwin":
            # Apply vibrant macOS-style theming
            app = QApplication.instance()
            if app:
                palette = app.palette()
                colors = self._get_palette_colors(palette)

                is_dark_mode = colors["is_dark"].red() == 0

                # Get DPI scaling safely
                try:
                    dpr = self.devicePixelRatioF()
                except (AttributeError, RuntimeError):
                    dpr = 1.0

                # Check if theme changed to avoid redundant reapplication
                theme_key = f"{is_dark_mode}_{colors['highlight'].name()}"
                if theme_key == self._last_theme_state.get('key'):
                    return
                self._last_theme_state['key'] = theme_key

                # Scale values for HiDPI
                def scale(px: int) -> int:
                    return max(1, int(px * dpr))

                accent = colors["highlight"]
                accent_r, accent_g, accent_b = accent.red(), accent.green(), accent.blue()

                text_color = colors["text"]
                disabled_color = colors["disabled_text"]
                button_bg = colors["button"]

                # Calculate derived colors
                r_scale = scale(7)

                if is_dark_mode:
                    # Dark mode with proper shadows and depth
                    stylesheet = f"""
                        /* Main window background */
                        QMainWindow {{
                            background-color: rgb({colors["window"].red()}, {colors["window"].green()}, {colors["window"].blue()});
                        }}

                        /* Base widget transparency - scoped carefully */
                        QWidget {{
                            background-color: transparent;
                            color: rgba({text_color.red()}, {text_color.green()}, {text_color.blue()}, 230);
                        }}

                        /* Buttons with proper Mac styling and shadows */
                        QPushButton {{
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba({button_bg.red()}, {button_bg.green()}, {button_bg.blue()}, 40),
                                stop:1 rgba({button_bg.red()}, {button_bg.green()}, {button_bg.blue()}, 25));
                            border: 1px solid rgba(255, 255, 255, 0.15);
                            border-radius: {r_scale}px;
                            padding: {scale(7)}px {scale(16)}px;
                            font-weight: 500;
                            color: rgba({text_color.red()}, {text_color.green()}, {text_color.blue()}, 240);
                            /* Subtle shadow for depth */
                            margin: 1px;
                        }}

                        QPushButton:hover {{
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba({accent_r}, {accent_g}, {accent_b}, 55),
                                stop:1 rgba({accent_r}, {accent_g}, {accent_b}, 35));
                            border-color: rgba({accent_r}, {accent_g}, {accent_b}, 180);
                        }}

                        QPushButton:pressed {{
                            background: rgba({accent_r}, {accent_g}, {accent_b}, 75);
                            border-color: rgba({accent_r}, {accent_g}, {accent_b}, 200);
                            padding-top: {scale(8)}px;
                            padding-bottom: {scale(6)}px;
                        }}

                        QPushButton:focus {{
                            border: 2px solid rgba({accent_r}, {accent_g}, {accent_b}, 200);
                            padding: {scale(6)}px {scale(15)}px;
                        }}

                        QPushButton:disabled {{
                            background: rgba(255, 255, 255, 0.05);
                            border-color: rgba(255, 255, 255, 0.08);
                            color: rgba({disabled_color.red()}, {disabled_color.green()}, {disabled_color.blue()}, 180);
                        }}

                        /* Solid content areas */
                        QListWidget, QTextEdit, QLineEdit, QSpinBox, QComboBox {{
                            background-color: rgba({colors["base"].red()}, {colors["base"].green()}, {colors["base"].blue()}, 240);
                            border: 1px solid rgba(255, 255, 255, 0.12);
                            border-radius: {scale(8)}px;
                            padding: {scale(4)}px;
                            color: rgba({text_color.red()}, {text_color.green()}, {text_color.blue()}, 240);
                        }}

                        /* List widget specific styling */
                        QListWidget {{
                            padding: {scale(6)}px {scale(4)}px {scale(6)}px {scale(8)}px;
                        }}

                        QListWidget::item {{
                            padding: {scale(6)}px {scale(10)}px;
                            margin: {scale(2)}px {scale(2)}px {scale(2)}px 0px;
                            border-radius: {scale(6)}px;
                        }}

                        QListWidget::item:selected {{
                            background-color: rgba({accent_r}, {accent_g}, {accent_b}, 90);
                            color: rgba(255, 255, 255, 250);
                        }}

                        QListWidget::item:hover {{
                            background-color: rgba(255, 255, 255, 0.10);
                        }}

                        /* Scrollbar - minimal Mac style */
                        QScrollBar:vertical {{
                            background: transparent;
                            width: {scale(10)}px;
                            margin: {scale(2)}px 0px {scale(2)}px 0px;
                        }}

                        QScrollBar::handle:vertical {{
                            background: rgba(255, 255, 255, 0.25);
                            border-radius: {scale(4)}px;
                            min-height: {scale(30)}px;
                        }}

                        QScrollBar::handle:vertical:hover {{
                            background: rgba({accent_r}, {accent_g}, {accent_b}, 120);
                        }}

                        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
                        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                            background: none;
                            border: none;
                        }}

                        /* Panels with depth */
                        QWidget#pdfControlsPanel, QWidget#extractionControlsPanel, QWidget#_left_panel {{
                            background-color: rgba({colors["base"].red()}, {colors["base"].green()}, {colors["base"].blue()}, 20);
                            border: 1px solid rgba(255, 255, 255, 0.08);
                            border-radius: {scale(12)}px;
                            padding: {scale(16)}px;
                        }}

                        /* Instructions/Welcome panels */
                        QLabel#instructionsPanel {{
                            padding: {scale(16)}px;
                            background-color: rgba(255, 255, 255, 13);
                            color: rgba(255, 255, 255, 210);
                            border: 1px solid rgba(255, 255, 255, 26);
                            border-radius: {scale(8)}px;
                            font-size: 12px;
                            line-height: 1.5;
                        }}

                        /* Glass panels for image views */
                        QWidget#glassPanel {{
                            background-color: transparent;
                        }}

                        /* Image view containers - NO styling on QGraphicsView to prevent crashes */
                        QGraphicsView {{
                            border: none;
                        }}

                        /* Tabs with Mac styling */
                        QTabWidget::pane {{
                            border: 1px solid rgba(255, 255, 255, 0.10);
                            border-radius: {scale(10)}px;
                            padding: {scale(4)}px;
                            background-color: rgba({colors["base"].red()}, {colors["base"].green()}, {colors["base"].blue()}, 15);
                        }}

                        QTabBar::tab {{
                            background-color: transparent;
                            padding: {scale(8)}px {scale(18)}px;
                            margin-right: {scale(2)}px;
                            border-top-left-radius: {r_scale}px;
                            border-top-right-radius: {r_scale}px;
                            color: rgba({text_color.red()}, {text_color.green()}, {text_color.blue()}, 200);
                        }}

                        QTabBar::tab:selected {{
                            background-color: rgba({accent_r}, {accent_g}, {accent_b}, 45);
                            color: rgba({text_color.red()}, {text_color.green()}, {text_color.blue()}, 250);
                        }}

                        QTabBar::tab:hover {{
                            background-color: rgba(255, 255, 255, 0.08);
                        }}

                        /* Tooltips */
                        QToolTip {{
                            background-color: rgba({colors["tooltip_base"].red()}, {colors["tooltip_base"].green()}, {colors["tooltip_base"].blue()}, 245);
                            color: rgba({colors["tooltip_text"].red()}, {colors["tooltip_text"].green()}, {colors["tooltip_text"].blue()}, 250);
                            border: 1px solid rgba(255, 255, 255, 0.15);
                            border-radius: {scale(6)}px;
                            padding: {scale(4)}px {scale(8)}px;
                        }}

                        /* Status bar */
                        QStatusBar {{
                            background-color: rgba({colors["base"].red()}, {colors["base"].green()}, {colors["base"].blue()}, 25);
                            border-top: 1px solid rgba(255, 255, 255, 0.08);
                        }}

                        /* Pane labels */
                        QLabel#sourcePaneLabel, QLabel#previewPaneLabel, QLabel#resultPaneLabel {{
                            padding: {scale(4)}px;
                            color: rgba({text_color.red()}, {text_color.green()}, {text_color.blue()}, 220);
                        }}
                    """
                    self.setStyleSheet(stylesheet)
                else:
                    # Light mode with solid backgrounds and proper contrast
                    stylesheet = f"""
                        /* Main window background */
                        QMainWindow {{
                            background-color: rgb({colors["window"].red()}, {colors["window"].green()}, {colors["window"].blue()});
                        }}

                        /* Base widget - keep content solid */
                        QWidget {{
                            background-color: transparent;
                            color: rgba({text_color.red()}, {text_color.green()}, {text_color.blue()}, 255);
                        }}

                        /* Buttons with proper Mac styling */
                        QPushButton {{
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(255, 255, 255, 240),
                                stop:1 rgba(250, 250, 252, 240));
                            border: 1px solid rgba(0, 0, 0, 0.18);
                            border-radius: {r_scale}px;
                            padding: {scale(7)}px {scale(16)}px;
                            font-weight: 500;
                            color: rgba({text_color.red()}, {text_color.green()}, {text_color.blue()}, 255);
                        }}

                        QPushButton:hover {{
                            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba({accent_r}, {accent_g}, {accent_b}, 35),
                                stop:1 rgba({accent_r}, {accent_g}, {accent_b}, 20));
                            border-color: rgba({accent_r}, {accent_g}, {accent_b}, 140);
                        }}

                        QPushButton:pressed {{
                            background: rgba({accent_r}, {accent_g}, {accent_b}, 50);
                            border-color: rgba({accent_r}, {accent_g}, {accent_b}, 180);
                            padding-top: {scale(8)}px;
                            padding-bottom: {scale(6)}px;
                        }}

                        QPushButton:focus {{
                            border: 2px solid rgba({accent_r}, {accent_g}, {accent_b}, 180);
                            padding: {scale(6)}px {scale(15)}px;
                        }}

                        QPushButton:disabled {{
                            background: rgba(255, 255, 255, 0.50);
                            border-color: rgba(0, 0, 0, 0.10);
                            color: rgba({disabled_color.red()}, {disabled_color.green()}, {disabled_color.blue()}, 200);
                        }}

                        /* Solid content areas */
                        QListWidget, QTextEdit, QLineEdit, QSpinBox, QComboBox {{
                            background-color: rgba({colors["base"].red()}, {colors["base"].green()}, {colors["base"].blue()}, 255);
                            border: 1px solid rgba(0, 0, 0, 0.14);
                            border-radius: {scale(8)}px;
                            padding: {scale(4)}px;
                            color: rgba({text_color.red()}, {text_color.green()}, {text_color.blue()}, 255);
                        }}

                        /* List widget specific styling */
                        QListWidget {{
                            padding: {scale(6)}px {scale(4)}px {scale(6)}px {scale(8)}px;
                        }}

                        QListWidget::item {{
                            padding: {scale(6)}px {scale(10)}px;
                            margin: {scale(2)}px {scale(2)}px {scale(2)}px 0px;
                            border-radius: {scale(6)}px;
                        }}

                        QListWidget::item:selected {{
                            background-color: rgba({accent_r}, {accent_g}, {accent_b}, 50);
                            color: rgba({accent_r}, {accent_g}, {accent_b}, 255);
                        }}

                        QListWidget::item:hover {{
                            background-color: rgba(0, 0, 0, 0.05);
                        }}

                        /* Scrollbar - minimal Mac style */
                        QScrollBar:vertical {{
                            background: transparent;
                            width: {scale(10)}px;
                            margin: {scale(2)}px 0px {scale(2)}px 0px;
                        }}

                        QScrollBar::handle:vertical {{
                            background: rgba(0, 0, 0, 0.20);
                            border-radius: {scale(4)}px;
                            min-height: {scale(30)}px;
                        }}

                        QScrollBar::handle:vertical:hover {{
                            background: rgba({accent_r}, {accent_g}, {accent_b}, 140);
                        }}

                        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
                        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                            background: none;
                            border: none;
                        }}

                        /* Panels */
                        QWidget#pdfControlsPanel, QWidget#extractionControlsPanel, QWidget#_left_panel {{
                            background-color: rgba(255, 255, 255, 245);
                            border: 1px solid rgba(0, 0, 0, 0.10);
                            border-radius: {scale(12)}px;
                            padding: {scale(16)}px;
                        }}

                        /* Instructions/Welcome panels - Light mode */
                        QLabel#instructionsPanel {{
                            padding: {scale(16)}px;
                            background-color: rgba(0, 0, 0, 8);
                            color: #2b2b2b;
                            border: 1px solid rgba(0, 0, 0, 20);
                            border-radius: {scale(8)}px;
                            font-size: 12px;
                            line-height: 1.5;
                        }}

                        /* Glass panels for image views */
                        QWidget#glassPanel {{
                            background-color: transparent;
                        }}

                        /* Image view containers - NO styling on QGraphicsView to prevent crashes */
                        QGraphicsView {{
                            border: none;
                        }}

                        /* Tabs with Mac styling */
                        QTabWidget::pane {{
                            border: 1px solid rgba(0, 0, 0, 0.12);
                            border-radius: {scale(10)}px;
                            padding: {scale(4)}px;
                            background-color: rgba(255, 255, 255, 245);
                        }}

                        QTabBar::tab {{
                            background-color: transparent;
                            padding: {scale(8)}px {scale(18)}px;
                            margin-right: {scale(2)}px;
                            border-top-left-radius: {r_scale}px;
                            border-top-right-radius: {r_scale}px;
                            color: rgba({text_color.red()}, {text_color.green()}, {text_color.blue()}, 200);
                        }}

                        QTabBar::tab:selected {{
                            background-color: rgba({accent_r}, {accent_g}, {accent_b}, 40);
                            color: rgba({accent_r}, {accent_g}, {accent_b}, 255);
                        }}

                        QTabBar::tab:hover {{
                            background-color: rgba({accent_r}, {accent_g}, {accent_b}, 20);
                        }}

                        /* Tooltips */
                        QToolTip {{
                            background-color: rgba({colors["tooltip_base"].red()}, {colors["tooltip_base"].green()}, {colors["tooltip_base"].blue()}, 250);
                            color: rgba({colors["tooltip_text"].red()}, {colors["tooltip_text"].green()}, {colors["tooltip_text"].blue()}, 255);
                            border: 1px solid rgba(0, 0, 0, 0.15);
                            border-radius: {scale(6)}px;
                            padding: {scale(4)}px {scale(8)}px;
                        }}

                        /* Status bar */
                        QStatusBar {{
                            background-color: rgba(255, 255, 255, 240);
                            border-top: 1px solid rgba(0, 0, 0, 0.10);
                        }}

                        /* Pane labels */
                        QLabel#sourcePaneLabel, QLabel#previewPaneLabel, QLabel#resultPaneLabel {{
                            padding: {scale(4)}px;
                            color: rgba({text_color.red()}, {text_color.green()}, {text_color.blue()}, 230);
                        }}
                    """
                    self.setStyleSheet(stylesheet)
            else:
                # Fallback if no app instance
                self.setStyleSheet(
                    """
                    QLabel#sourcePaneLabel,
                    QLabel#previewPaneLabel,
                    QLabel#resultPaneLabel {
                        padding: 4px;
                    }
                """
                )
            self._setup_dark_mode_support()
            return

        # Non-macOS fallback with basic styling
        self.setStyleSheet(
            """
            QWidget { background-color: #f7f7f7; color: #222222; }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f0f0f0);
                border: 1px solid #d0d0d0;
                border-radius: 7px;
                padding: 7px 16px;
                font-weight: 500;
                color: #222222;
            }
            QPushButton:hover { background-color: #e0e0e0; border-color: #007AFF; }
            QPushButton:pressed { background-color: #d0d0d0; }
            QPushButton:disabled { background-color: #f8f8f8; color: #888888; }
            QLabel { font-size: 13px; color: #222222; }
        """
        )

    def _setup_dark_mode_support(self) -> None:
        """Align palette with system appearance on macOS."""
        if sys.platform != "darwin":
            return

        app = QApplication.instance()
        if not app:
            return

        app_typed = cast("QApplication", app)
        palette = app_typed.palette()  # type: ignore[attr-defined]
        self.setPalette(palette)

        for attr in ("src_view", "preview_view", "res_view"):
            view = getattr(self, attr, None)
            if view is None:
                continue
            view.setPalette(palette)
            view.viewport().setPalette(palette)


__all__ = ["ThemeMixin"]
