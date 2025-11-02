from __future__ import annotations

import atexit
import io
import logging
import os
import sys
from functools import partial
from typing import TYPE_CHECKING, Any, Callable, Optional, Protocol, cast

import numpy as np
from PIL import Image as PILImage

# Early imports for AsyncRunner helper class
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal


class AsyncRunner(QObject):
    """Helper class to run functions asynchronously and emit results."""

    finished = Signal(object)  # Emits the result
    error = Signal(Exception)  # Emits any exception

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """Run the function and emit the result or error."""
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(e)


def run_async(func, *args, **kwargs):
    """Run a function asynchronously and return a future-like object.

    This is a compatibility function that mimics QtConcurrent.run behavior.
    """
    runner = AsyncRunner(func, *args, **kwargs)

    class Future:
        def __init__(self, runner):
            self.runner = runner
            self._result = None
            self._error = None
            self._finished = False
            runner.finished.connect(self._on_finished)
            runner.error.connect(self._on_error)

        def _on_finished(self, result):
            self._result = result
            self._finished = True

        def _on_error(self, error):
            self._error = error
            self._finished = True

        def result(self):
            if self._error:
                raise self._error
            return self._result

        def isFinished(self):
            return self._finished

    future = Future(runner)

    # Run in thread pool
    thread_pool = QThreadPool.globalInstance()
    runnable = QRunnable.create(lambda: runner.run())
    runnable.setAutoDelete(True)
    thread_pool.start(runnable)

    return future
from PySide6.QtCore import QTimer, Qt, QPoint, QBuffer, QIODevice, QUrl
from PySide6.QtGui import QColor, QDesktopServices, QFont, QFontMetrics, QImage, QKeySequence, QPalette, QPixmap, QShortcut, QTransform
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSlider,
    QSizePolicy,
    QStatusBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from desktop_app.api.client import ApiClient
from desktop_app.library import storage as lib
from desktop_app.license.storage import is_licensed
from desktop_app.resources.icons import get_icon, set_button_icon
from desktop_app.widgets.glass_panel import GlassPanel
from desktop_app.widgets.image_view import ImageView
from desktop_app.views.export_dialog import ExportDialog
from desktop_app.views.help_dialog import HelpDialog
from desktop_app.views.license_dialog import LicenseDialog

if TYPE_CHECKING:
    from PySide6.QtCore import QEvent

    class _MainWindowProtocol(Protocol):
        """Protocol defining methods from QMainWindow that mixins depend on."""
        api_client: ApiClient
        status_bar: QStatusBar
        tab_widget: Any
        session: Any

        def palette(self) -> QPalette: ...
        def setPalette(self, palette: QPalette) -> None: ...
        def setWindowFilePath(self, path: str) -> None: ...
        def setStyleSheet(self, styleSheet: str) -> None: ...
        def resizeEvent(self, event: QEvent) -> None: ...

LOG = logging.getLogger(__name__)

ShortcutKey = QKeySequence | QKeySequence.StandardKey | str


def _rgba(color: QColor) -> str:
    """Return a Qt stylesheet-friendly RGBA string for the given QColor."""
    return f"rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()})"


class ElidingButton(QPushButton):
    """A QPushButton that elides text when it doesn't fit."""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._full_text = text

    def setText(self, text):
        self._full_text = text
        super().setText(text)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._full_text:
            fm = QFontMetrics(self.font())
            elided = fm.elidedText(self._full_text, Qt.ElideRight, self.width() - 10)
            super().setText(elided)


class ExtractionTabMixin:
    """Signature extraction tab, color handling, and library management.

    This mixin is designed to be used with QMainWindow and provides
    the extraction tab UI and functionality. For type checking purposes,
    it expects the including class to provide QMainWindow methods.
    """

    # Declare attributes that will be provided by QMainWindow or other mixins
    # Using 'Any' to avoid circular imports and mypy issues with mixins
    api_client: Any
    status_bar: Any
    tab_widget: Any
    session: Any

    # Declare methods that will be provided by other mixins
    def _install_pane_click_filter(self, view, pane_name): ...
    def _update_coordinate_display(self): ...
    def _update_pane_borders(self): ...
    def _on_pane_clicked(self, pane: str): ...
    def _get_active_view(self): ...

    if TYPE_CHECKING:
        # Tell mypy that at runtime, self will be a QWidget with these methods
        def palette(self) -> QPalette: ...
        def setWindowFilePath(self, path: str) -> None: ...

    def _setup_extraction_ui(self) -> None:
        extraction_tab = QWidget()
        extraction_layout = QHBoxLayout(extraction_tab)

        # Cast self to QWidget for type checking (self will be a QMainWindow at runtime)
        parent_widget = cast(QWidget, self)
        left_panel = QWidget(parent_widget)
        left_panel.setObjectName("extractionControlsPanel")
        left_panel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        left_panel.setFixedWidth(300)  # Fixed width prevents compression
        controls = QVBoxLayout(left_panel)
        controls.setContentsMargins(16, 18, 16, 18)
        controls.setSpacing(10)

        # Store reference for responsive breakpoints
        self._left_panel = left_panel

        # Compute section and pane label colors for both macOS and non-macOS
        palette = cast(QWidget, self).palette()
        group = palette.currentColorGroup()
        text_color = palette.color(group, QPalette.ColorRole.WindowText)

        # Detect dark vs light mode
        base_color = palette.color(group, QPalette.ColorRole.Window)
        is_dark_mode = base_color.lightness() < 120

        # Section labels: use translucent only in dark mode, opaque in light mode
        section_color = QColor(text_color)
        if is_dark_mode:
            section_color.setAlpha(180)  # Subtle in dark mode
        else:
            section_color.setAlpha(235)  # Nearly opaque for readability in light mode
        section_color_hex = _rgba(section_color)
        pane_label_color = _rgba(text_color)

        if sys.platform == "darwin":
            left_panel.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
            border_color = palette.color(group, QPalette.ColorRole.Mid)

            if is_dark_mode:
                # Vibrant dark mode: deep, rich background with subtle blue tint
                panel_color = QColor(28, 28, 32, 248)
            else:
                # Vibrant light mode: bright, crisp white with warmth
                panel_color = QColor(251, 251, 253, 250)

            # Vibrant button styling with better contrast
            button_bg = QColor(panel_color)
            button_bg = button_bg.lighter(115 if is_dark_mode else 108)
            button_bg.setAlpha(220 if is_dark_mode else 180)
            button_bg_str = _rgba(button_bg)

            button_hover = QColor(button_bg)
            button_hover = button_hover.lighter(120 if is_dark_mode else 112)
            button_hover.setAlpha(min(button_hover.alpha() + 30, 255))
            button_hover_str = _rgba(button_hover)

            button_border = QColor(border_color)
            button_border = button_border.lighter(130 if is_dark_mode else 120)
            button_border.setAlpha(100 if is_dark_mode else 80)
            button_border_str = _rgba(button_border)

            disabled_bg = QColor(panel_color)
            disabled_bg.setAlpha(95)
            disabled_bg_str = _rgba(disabled_bg)

            # Disabled text: higher alpha in light mode for readability
            disabled_text = QColor(text_color)
            if is_dark_mode:
                disabled_text.setAlpha(120)  # More subtle in dark mode
            else:
                disabled_text.setAlpha(180)  # More readable in light mode (darker gray)
            disabled_text_str = _rgba(disabled_text)

            field_bg = QColor(panel_color)
            field_bg = field_bg.lighter(118)
            field_bg.setAlpha(185)
            field_bg_str = _rgba(field_bg)

            subtle_line = QColor(border_color)
            subtle_line.setAlpha(70)
            subtle_line_str = _rgba(subtle_line)

            left_panel.setStyleSheet(
                "QWidget#extractionControlsPanel {"
                f"  background-color: {_rgba(panel_color)};"
                f"  border-right: 1px solid {subtle_line_str};"
                f"  color: {text_color.name()};"
                "  font-size: 12px;"
                "}"
                "#extractionControlsPanel QLabel,"
                "#extractionControlsPanel QStatusBar,"
                "#extractionControlsPanel QToolButton {"
                "  background-color: transparent;"
                "  border: none;"
                f"  color: {text_color.name()};"
                "}"
                "#extractionControlsPanel QLineEdit,"
                "#extractionControlsPanel QComboBox {"
                f"  background-color: {field_bg_str};"
                f"  border: 1px solid {subtle_line_str};"
                "  border-radius: 8px;"
                "  padding: 6px 8px;"
                f"  color: {text_color.name()};"
                "}"
                "#extractionControlsPanel QLineEdit:focus,"
                "#extractionControlsPanel QComboBox:focus {"
                f"  border: 2px solid {'#007AFF' if is_dark_mode else '#0051D5'};"
                "  outline: none;"
                "}"
                "#extractionControlsPanel QComboBox::drop-down {"
                "  width: 22px;"
                "}"
                "#extractionControlsPanel QListWidget {"
                f"  background-color: {field_bg_str};"
                f"  border: 1px solid {subtle_line_str};"
                "  border-radius: 10px;"
                "  padding: 6px;"
                "}"
                "#extractionControlsPanel QListWidget:focus {"
                f"  border: 2px solid {'#007AFF' if is_dark_mode else '#0051D5'};"
                "}"
                "#extractionControlsPanel QListWidget::item:selected {"
                f"  background-color: {button_hover_str};"
                f"  color: {text_color.name()};"
                "}"
                "#extractionControlsPanel QSlider::groove:horizontal {"
                "  background: rgba(100, 100, 100, 180);"  # Visible gray groove
                "  height: 6px;"
                "  border-radius: 3px;"
                "  margin: 0;"
                "}"
                "#extractionControlsPanel QSlider::handle:horizontal {"
                "  background: rgba(255, 255, 255, 230);"  # Bright white handle
                "  border: 1px solid rgba(180, 180, 180, 200);"
                "  width: 16px;"
                "  height: 16px;"
                "  margin: -6px 0;"
                "  border-radius: 8px;"
                "}"
                f"QWidget#extractionControlsPanel QPushButton {{ padding: 7px 14px; border-radius: 8px; border: 1px solid {button_border_str};"
                f"  background-color: {button_bg_str}; color: {text_color.name()}; font-weight: 500; }}"
                f"QWidget#extractionControlsPanel QPushButton:hover {{ background-color: {button_hover_str}; }}"
                f"QWidget#extractionControlsPanel QPushButton:focus {{ border: 2px solid {'#007AFF' if is_dark_mode else '#0051D5'}; outline: none; }}"
                f"QWidget#extractionControlsPanel QPushButton:disabled {{ color: {disabled_text_str}; background-color: {disabled_bg_str}; border-color: {subtle_line_str}; }}"
                f"QWidget#extractionControlsPanel QCheckBox {{ color: {text_color.name()}; spacing: 6px; }}"
            )

        self.open_btn = ElidingButton()
        set_button_icon(self.open_btn, "open", "Open & Upload Image", use_emoji=False)
        self.open_btn.setObjectName("openFileButton")
        self.open_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.open_btn.clicked.connect(self.on_open)
        controls.addWidget(self._make_section_label("Upload", section_color_hex, top_margin=0))
        controls.addWidget(self.open_btn)

        controls.addWidget(self._make_section_label("Threshold", section_color_hex))
        threshold_row = QHBoxLayout()
        self.threshold = QSlider(Qt.Orientation.Horizontal)
        self.threshold.setObjectName("thresholdSlider")
        self.threshold.setRange(0, 255)
        self.threshold.setValue(200)
        self.threshold.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        threshold_row.addWidget(self.threshold, 1)
        self.threshold_value_label = QLabel("200")
        self.threshold_value_label.setMinimumWidth(30)  # Reduced from 35 for better flexibility
        self.threshold_value_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.threshold_value_label.setToolTip("Current threshold value")
        threshold_row.addWidget(self.threshold_value_label, 0)

        # Auto-threshold badge - hidden until auto mode is enabled
        self.auto_threshold_badge = QLabel("")
        self.auto_threshold_badge.setMinimumWidth(45)  # Reduced from 50 for better flexibility
        self.auto_threshold_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.auto_threshold_badge.setStyleSheet(
            "border: 1px solid rgba(0, 122, 255, 80);"
            "background-color: rgba(0, 122, 255, 20);"
            "color: rgba(0, 122, 255, 200);"
            "border-radius: 6px;"
            "padding: 2px 6px;"
            "font-size: 10px;"
            "font-weight: 600;"
        )
        self.auto_threshold_badge.setVisible(False)
        threshold_row.addWidget(self.auto_threshold_badge, 0)

        self.auto_threshold_cb = QCheckBox("Auto")
        self.auto_threshold_cb.setObjectName("autoThresholdCheck")
        self.auto_threshold_cb.setToolTip("Let the backend compute an optimal threshold based on the selection")
        self.auto_threshold_cb.setChecked(False)
        self.auto_threshold_cb.stateChanged.connect(self._on_auto_threshold_toggled)
        threshold_row.addWidget(self.auto_threshold_cb, 0)
        controls.addLayout(threshold_row)

        self.color_label = QLabel("Color: #000000")
        self.color_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.pick_color_btn = QPushButton()
        set_button_icon(self.pick_color_btn, "color", "Pick Color", use_emoji=False)
        self.pick_color_btn.setObjectName("pickColorButton")
        self.pick_color_btn.clicked.connect(self.on_pick_color)
        color_row = QHBoxLayout()
        color_row.addWidget(self.color_label, 1)
        color_row.addWidget(self.pick_color_btn, 0)
        controls.addLayout(color_row)

        swatch_row = QHBoxLayout()
        swatch_row.setSpacing(8)
        swatch_row.addWidget(self._make_secondary_label("History", section_color_hex))
        self.color_history_layout = QHBoxLayout()
        self.color_history_layout.setSpacing(6)
        swatch_row.addLayout(self.color_history_layout)
        swatch_row.addWidget(self._make_secondary_label("Presets", section_color_hex))
        self.color_presets_layout = QHBoxLayout()
        self.color_presets_layout.setSpacing(6)
        swatch_row.addLayout(self.color_presets_layout)
        swatch_row.addStretch(1)
        controls.addLayout(swatch_row)

        controls.addWidget(self._make_section_label("View", section_color_hex))
        view_row1 = QHBoxLayout()
        self.zoom_in_btn = QPushButton("+")
        self.zoom_in_btn.setObjectName("zoomInButton")
        self.zoom_in_btn.setToolTip("Zoom In (Ctrl/Cmd +)")
        self.zoom_out_btn = QPushButton("−")
        self.zoom_out_btn.setObjectName("zoomOutButton")
        self.zoom_out_btn.setToolTip("Zoom Out (Ctrl/Cmd −)")
        self.zoom_combo = QComboBox()
        self.zoom_combo.setObjectName("zoomCombo")
        self.zoom_combo.setEditable(True)
        self.zoom_combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.zoom_combo.addItems(["25%", "50%", "75%", "100%", "125%", "150%", "200%", "Fit"])
        self.zoom_combo.setCurrentText("100%")
        self.zoom_combo.setToolTip("Set zoom for the active pane. Enter a percentage or choose Fit.")
        self.zoom_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.zoom_combo.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self.zoom_combo.setMinimumWidth(60)  # Ensure minimum width for usability
        line_edit = self.zoom_combo.lineEdit()
        if line_edit is not None:
            line_edit.setPlaceholderText("Zoom")
            if sys.platform == "darwin":
                try:
                    line_edit.setClearButtonEnabled(True)
                except AttributeError:
                    pass
        view_row1.addWidget(self.zoom_in_btn)
        view_row1.addWidget(self.zoom_out_btn)
        view_row1.addWidget(self.zoom_combo)
        controls.addLayout(view_row1)

        view_row2 = QHBoxLayout()
        self.fit_btn = QPushButton("Fit")
        self.fit_btn.setObjectName("fitButton")
        self.fit_btn.setToolTip("Fit image (Ctrl/Cmd 1)")
        self.reset_view_btn = QPushButton("Reset")
        self.reset_view_btn.setObjectName("resetViewButton")
        self.reset_view_btn.setToolTip("Reset view (Ctrl/Cmd 0)")
        view_row2.addWidget(self.fit_btn)
        view_row2.addWidget(self.reset_view_btn)
        controls.addLayout(view_row2)

        controls.addWidget(self._make_section_label("Image", section_color_hex))
        rotate_row = QHBoxLayout()
        self.rotate_ccw_btn = QPushButton("↺")
        self.rotate_ccw_btn.setObjectName("rotateCCWButton")
        self.rotate_ccw_btn.setToolTip("Rotate CCW (Ctrl/Cmd [)")
        self.rotate_cw_btn = QPushButton("↻")
        self.rotate_cw_btn.setObjectName("rotateCWButton")
        self.rotate_cw_btn.setToolTip("Rotate CW (Ctrl/Cmd ])")
        rotate_row.addWidget(self.rotate_ccw_btn)
        rotate_row.addWidget(self.rotate_cw_btn)
        controls.addLayout(rotate_row)

        controls.addWidget(self._make_section_label("Selection", section_color_hex))
        self.toggle_mode_btn = ElidingButton()
        self.toggle_mode_btn.setObjectName("toggleModeButton")
        self.toggle_mode_btn.setToolTip("Toggle between Select and Pan modes")
        self.toggle_mode_btn.setCheckable(True)
        self.toggle_mode_btn.setChecked(True)
        self.toggle_mode_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        set_button_icon(self.toggle_mode_btn, "mode_select", "Selection Mode: Select", use_emoji=False)
        self.clear_sel_btn = ElidingButton("Clear Selection")
        self.clear_sel_btn.setObjectName("clearSelectionButton")
        self.clear_sel_btn.setToolTip("Clear current selection")
        self.clear_sel_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.clean_session_btn = ElidingButton("Clean Viewport")
        self.clean_session_btn.setObjectName("cleanViewportButton")
        self.clean_session_btn.setToolTip("Clear the current upload and reset all panes")
        self.clean_session_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        controls.addWidget(self.toggle_mode_btn)
        controls.addWidget(self.clear_sel_btn)
        controls.addWidget(self.clean_session_btn)

        controls.addWidget(self._make_section_label("Export & Save", section_color_hex))
        export_row_1 = QHBoxLayout()
        self.export_btn = ElidingButton("Export...")
        self.export_btn.setObjectName("exportButton")
        self.export_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        export_icon = get_icon("export")
        if not export_icon.isNull():
            self.export_btn.setIcon(export_icon)
        self.export_btn.setToolTip("Export with advanced options (background, trim, format) - Ctrl/Cmd E")
        self.export_btn.clicked.connect(self.on_export)
        self.export_btn.setEnabled(False)
        self.copy_btn = QPushButton("Copy")
        self.copy_btn.setObjectName("copyButton")
        self.copy_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        copy_icon = get_icon("copy")
        if not copy_icon.isNull():
            self.copy_btn.setIcon(copy_icon)
        self.copy_btn.setToolTip("Copy result to clipboard (preserves transparency) - Ctrl/Cmd C")
        self.copy_btn.clicked.connect(self.on_copy)
        self.copy_btn.setEnabled(False)
        export_row_1.addWidget(self.export_btn)
        export_row_1.addWidget(self.copy_btn)
        controls.addLayout(export_row_1)

        export_row_2 = QHBoxLayout()
        self.save_to_library_btn = ElidingButton("Save to Library")
        self.save_to_library_btn.setObjectName("saveToLibraryButton")
        self.save_to_library_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        save_icon = get_icon("save")
        if not save_icon.isNull():
            self.save_to_library_btn.setIcon(save_icon)
        self.save_to_library_btn.setToolTip("Quick save as PNG to local library")
        self.save_to_library_btn.clicked.connect(self.on_save_to_library)
        self.save_to_library_btn.setEnabled(False)

        self.export_json_btn = ElidingButton("Export JSON")
        self.export_json_btn.setObjectName("exportJsonButton")
        self.export_json_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        export_json_icon = get_icon("export")
        if not export_json_icon.isNull():
            self.export_json_btn.setIcon(export_json_icon)
        self.export_json_btn.setToolTip("Save selection, threshold, color, and session info to JSON")
        self.export_json_btn.clicked.connect(self.on_export_json)
        self.export_json_btn.setEnabled(False)
        export_row_2.addWidget(self.save_to_library_btn)
        export_row_2.addWidget(self.export_json_btn)
        controls.addLayout(export_row_2)

        # Store section label for responsive hiding
        self._library_section_label = self._make_section_label("My Signatures", section_color_hex)
        controls.addWidget(self._library_section_label)
        self.library_list = QListWidget()
        self.library_list.setObjectName("libraryList")
        self.library_list.itemDoubleClicked.connect(self.on_library_item_open)
        self.library_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.library_list.customContextMenuRequested.connect(self.on_library_context_menu)
        self.library_list.itemSelectionChanged.connect(self._update_library_controls)
        self.library_list.setMinimumHeight(80)  # Reduced from 120 for better flexibility on small screens
        self.library_list.setTextElideMode(Qt.TextElideMode.ElideRight)  # Elide long filenames
        if sys.platform == "darwin":
            self.library_list.setStyleSheet(
                "QListWidget#libraryList {"
                "background-color: rgba(255, 255, 255, 20);"
                "border: 1px solid rgba(255, 255, 255, 30);"
                "border-radius: 8px;"
                "padding: 6px;"
                "}"
                "QListWidget#libraryList::item { height: 24px; border-radius: 8px; }"
                "QListWidget#libraryList::item:selected { background-color: rgba(255,255,255,46); }"
            )
        controls.addWidget(self.library_list)

        self.delete_from_library_btn = ElidingButton("Delete Selected")
        self.delete_from_library_btn.setObjectName("deleteLibraryButton")
        delete_icon = get_icon("delete")
        if not delete_icon.isNull():
            self.delete_from_library_btn.setIcon(delete_icon)
        self.delete_from_library_btn.setToolTip("Remove the selected signature from My Signatures")
        self.delete_from_library_btn.clicked.connect(self.on_delete_selected_library)
        self.delete_from_library_btn.setEnabled(False)
        controls.addWidget(self.delete_from_library_btn)
        
        controls.addSpacing(20)
        
        # Add friendly welcome/help text to fill blank space - let theme system style it
        welcome_label = QLabel(
            "✨ <b>Quick Start</b><br><br>"
            "1️⃣ Click <b>Open & Upload Image</b><br>"
            "2️⃣ Drag to select signature area<br>"
            "3️⃣ Preview updates automatically<br>"
            "4️⃣ <b>Export</b> or <b>Copy</b> when ready<br><br>"
            "💡 Tip: Adjust threshold and color for best results"
        )
        welcome_label.setObjectName("instructionsPanel")  # Let theme system style it
        welcome_label.setWordWrap(True)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        welcome_label.setTextFormat(Qt.TextFormat.RichText)
        # Store Quick Start for responsive hiding
        self._welcome_label = welcome_label
        controls.addWidget(welcome_label)
        controls.addStretch(1)

        if sys.platform == "darwin":
            accent = cast(QWidget, self).palette().color(cast(QWidget, self).palette().currentColorGroup(), QPalette.ColorRole.Highlight).name()
            # Adapt button styling to dark/light mode
            if is_dark_mode:
                btn_border = "rgba(255, 255, 255, 13)"
                btn_bg = "rgba(255, 255, 255, 20)"
            else:
                btn_border = "rgba(0, 0, 0, 20)"
                btn_bg = "rgba(0, 0, 0, 8)"

            self.toggle_mode_btn.setStyleSheet(
                "QPushButton#toggleModeButton {"
                "padding: 6px 12px;"
                "border-radius: 8px;"
                f"border: 1px solid {btn_border};"
                f"background-color: {btn_bg};"
                "}"
                f"QPushButton#toggleModeButton:checked {{ background-color: {accent}; color: white; }}"
            )
            for btn in (
                self.open_btn,
                self.pick_color_btn,
                self.zoom_in_btn,
                self.zoom_out_btn,
                self.fit_btn,
                self.reset_view_btn,
                self.rotate_ccw_btn,
                self.rotate_cw_btn,
                self.toggle_mode_btn,
                self.clear_sel_btn,
                self.clean_session_btn,
                self.export_btn,
                self.copy_btn,
                self.save_to_library_btn,
                self.export_json_btn,
                self.delete_from_library_btn,
            ):
                btn.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)

        self._images_layout = QVBoxLayout()
        self._src_container = QWidget()
        src_layout = QVBoxLayout(self._src_container)
        src_layout.setContentsMargins(0, 0, 0, 0)
        self.source_label = QLabel("Source")
        self.source_label.setObjectName("sourcePaneLabel")
        if sys.platform == "darwin":
            self.source_label.setStyleSheet(
                f"font-size: 13px; font-weight: 600; letter-spacing: 0.3px; color: {pane_label_color};"
            )
        src_layout.addWidget(self.source_label)
        self.src_view = ImageView(parent_widget)
        self.src_view.setObjectName("sourceImageView")
        self.src_view.setAccessibleName("Source image pane")
        self.src_view.setAccessibleDescription("Original image with selection tool. Click and drag to select signature area")
        self._install_pane_click_filter(self.src_view, "source")
        self.src_view.fileDropped.connect(self._on_source_file_dropped)
        src_layout.addWidget(self.src_view)
        self._images_layout.addWidget(self._src_container, stretch=3)

        self.preview_container = QWidget()
        preview_layout = QVBoxLayout(self.preview_container)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        self.preview_label = QLabel("Crop preview")
        self.preview_label.setVisible(False)
        self.preview_label.setObjectName("previewPaneLabel")
        if sys.platform == "darwin":
            self.preview_label.setStyleSheet(
                "font-size: 12px; font-weight: 600; letter-spacing: 0.4px;"
                f"color: {pane_label_color};"
            )
        preview_layout.addWidget(self.preview_label)
        self.preview_view = ImageView(self)
        self.preview_view.setObjectName("previewImageView")
        self.preview_view.setAccessibleName("Preview pane")
        self.preview_view.setAccessibleDescription("Preview of selected signature area")
        self.preview_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.preview_view.toggle_selection_mode(False)
        self.preview_view.setVisible(False)
        self._install_pane_click_filter(self.preview_view, "preview")
        self._install_pane_click_filter(self.preview_container, "preview")
        preview_layout.addWidget(self.preview_view)
        # Add empty-state overlay for preview
        self.preview_empty = QLabel("Drag on the Source to see a crop preview")
        self.preview_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_empty.setStyleSheet("opacity:0.7; font-size:12px; padding:24px;")
        self.preview_empty.setVisible(False)
        preview_layout.addWidget(self.preview_empty)
        self.preview_container.setVisible(False)

        result_container = QWidget()
        result_layout = QVBoxLayout(result_container)
        result_layout.setContentsMargins(0, 0, 0, 0)
        self.result_label = QLabel("Result")
        self.result_label.setVisible(False)
        self.result_label.setObjectName("resultPaneLabel")
        if sys.platform == "darwin":
            self.result_label.setStyleSheet(
                "font-size: 12px; font-weight: 600; letter-spacing: 0.4px;"
                f"color: {pane_label_color};"
            )
        result_layout.addWidget(self.result_label)
        self.res_view = ImageView(self)
        self.res_view.setObjectName("resultImageView")
        self.res_view.setAccessibleName("Result image pane")
        self.res_view.setAccessibleDescription("Final processed signature ready for export")
        self.res_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.res_view.toggle_selection_mode(False)  # Disable selection mode for result view
        self._install_pane_click_filter(self.res_view, "result")
        self.res_view.setVisible(False)
        result_layout.addWidget(self.res_view)
        # Add empty-state overlay for result
        self.result_empty = QLabel("Process a selection to see the result")
        self.result_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_empty.setStyleSheet("opacity:0.7; font-size:12px; padding:24px;")
        self.result_empty.setVisible(False)
        result_layout.addWidget(self.result_empty)

        self.preview_result_panel = GlassPanel(parent_widget)
        self.preview_result_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        stack_layout = QVBoxLayout(self.preview_result_panel)
        stack_layout.setContentsMargins(16, 16, 16, 16)
        stack_layout.setSpacing(12)
        stack_layout.addWidget(self.preview_container, 1)
        stack_layout.addWidget(result_container, 1)
        self._images_layout.addWidget(self.preview_result_panel, stretch=2)

        # Wrap left panel in scroll area for responsive behavior
        left_scroll = QScrollArea(parent_widget)
        left_scroll.setWidget(left_panel)
        left_scroll.setWidgetResizable(True)
        left_scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        left_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        left_scroll.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        left_scroll.setFixedWidth(320)  # Slightly wider to account for scrollbar

        extraction_layout.addWidget(left_scroll, 0)
        extraction_layout.addLayout(self._images_layout, 1)

        self._extraction_tab_index = self.tab_widget.addTab(extraction_tab, "📝 Signature Extraction")

        self.zoom_in_btn.clicked.connect(self._on_zoom_in)
        self.zoom_out_btn.clicked.connect(self._on_zoom_out)
        self.fit_btn.clicked.connect(self._on_fit)
        self.reset_view_btn.clicked.connect(self._on_reset_zoom)
        self.toggle_mode_btn.clicked.connect(self.on_toggle_mode)
        self.clear_sel_btn.clicked.connect(self.on_clear_selection)
        self.clean_session_btn.clicked.connect(self.on_clean_session)
        self.rotate_cw_btn.clicked.connect(lambda: self.on_rotate(90))
        self.rotate_ccw_btn.clicked.connect(lambda: self.on_rotate(-90))
        self.zoom_combo.activated.connect(self._on_zoom_combo_activated)
        line_edit = self.zoom_combo.lineEdit()
        if line_edit is not None:
            line_edit.editingFinished.connect(self._on_zoom_combo_edit_finished)

        self.sel_info = QLabel("Selection: –")
        if sys.platform == "darwin":
            # Use semi-transparent version of text color instead of hardcoded white
            self.sel_info.setStyleSheet(f"font-size: 11px; color: {pane_label_color}; padding: 4px;")
        else:
            self.sel_info.setStyleSheet("font-size: 11px; color: #666; padding: 4px;")
        controls.addWidget(self.sel_info)

        self.source_coord_tooltips_cb = QCheckBox("Show coordinate tooltips")
        self.source_coord_tooltips_cb.setToolTip("Display image pixel coordinates while hovering or selecting")
        self.source_coord_tooltips_cb.setChecked(True)
        self.source_coord_tooltips_cb.stateChanged.connect(self._on_source_coord_tooltips_toggled)
        controls.addWidget(self.source_coord_tooltips_cb)

        # Set up logical tab order for keyboard navigation
        self._setup_tab_order()

        self._set_preview_panel_visible(False)
        self._init_extraction_state()

    def _init_extraction_state(self) -> None:
        self._color_hex = "#000000"
        self._update_color_ui()
        self._color_history: list[str] = []
        self._color_presets = ["#000000", "#007AFF", "#FF7A59", "#FFFFFF"]
        self._refresh_color_history()
        self._populate_color_presets()
        self._remember_color(self._color_hex, suppress_preview=True)
        self._last_result_png: bytes | None = None
        self._last_local_path: str | None = None
        self._current_image_data: bytes | None = None
        self._licensed = is_licensed()
        self._active_pane = "source"
        self._auto_threshold_enabled = False
        self._updating_zoom_combo = False
        self._last_valid_zoom_text = "100%"
        self._temp_files: list[str] = []
        atexit.register(self._cleanup_temp_files)

        self._preview_timer = QTimer(cast(QWidget, self))
        self._preview_timer.setSingleShot(True)
        self._preview_timer.timeout.connect(self.on_preview)

        # Health check timer - check backend every 15 seconds
        self._health_timer = QTimer(cast(QWidget, self))
        self._health_timer.setInterval(15000)  # 15 seconds
        self._health_timer.timeout.connect(self._check_backend_health)
        self._health_timer.start()
        # Initial health check
        self._check_backend_health()

        self.src_view.selectionChanged.connect(self.on_selection_changed)
        self.src_view.zoomChanged.connect(self._update_coordinate_display)
        self.src_view.viewChanged.connect(self._update_coordinate_display)
        self.src_view.zoomChanged.connect(self._update_pane_labels_with_zoom)
        self.preview_view.zoomChanged.connect(self._update_coordinate_display)
        self.preview_view.viewChanged.connect(self._update_coordinate_display)
        self.preview_view.zoomChanged.connect(self._update_pane_labels_with_zoom)
        self.res_view.zoomChanged.connect(self._update_coordinate_display)
        self.res_view.viewChanged.connect(self._update_coordinate_display)
        self.res_view.zoomChanged.connect(self._update_pane_labels_with_zoom)
        self.threshold.valueChanged.connect(self.on_adjustment_changed)

        self._update_action_states()
        self._refresh_library_list()
        self._update_library_controls()
        self._update_pane_borders()

        # Apply initial breakpoint labels
        QTimer.singleShot(0, self._apply_left_panel_breakpoint)

    def _setup_tab_order(self) -> None:
        """Configure logical tab order for keyboard navigation through extraction controls."""
        # Main workflow order: Open → Mode toggle → Clear → View controls → Processing controls
        parent_widget = cast(QWidget, self)
        parent_widget.setTabOrder(self.open_btn, self.toggle_mode_btn)
        parent_widget.setTabOrder(self.toggle_mode_btn, self.clear_sel_btn)
        parent_widget.setTabOrder(self.clear_sel_btn, self.zoom_in_btn)
        parent_widget.setTabOrder(self.zoom_in_btn, self.zoom_out_btn)
        parent_widget.setTabOrder(self.zoom_out_btn, self.fit_btn)
        parent_widget.setTabOrder(self.fit_btn, self.reset_view_btn)
        parent_widget.setTabOrder(self.reset_view_btn, self.zoom_combo)
        parent_widget.setTabOrder(self.zoom_combo, self.rotate_ccw_btn)
        parent_widget.setTabOrder(self.rotate_ccw_btn, self.rotate_cw_btn)
        parent_widget.setTabOrder(self.rotate_cw_btn, self.pick_color_btn)
        parent_widget.setTabOrder(self.pick_color_btn, self.threshold)
        parent_widget.setTabOrder(self.threshold, self.auto_threshold_cb)
        parent_widget.setTabOrder(self.auto_threshold_cb, self.copy_btn)
        parent_widget.setTabOrder(self.copy_btn, self.export_btn)
        parent_widget.setTabOrder(self.export_btn, self.save_to_library_btn)
        parent_widget.setTabOrder(self.save_to_library_btn, self.library_list)
        parent_widget.setTabOrder(self.library_list, self.delete_from_library_btn)
        parent_widget.setTabOrder(self.delete_from_library_btn, self.clean_session_btn)
        parent_widget.setTabOrder(self.clean_session_btn, self.source_coord_tooltips_cb)

        parent_qobject = cast(QObject, self)
        shortcut_specs: list[tuple[ShortcutKey, Callable[[], None]]] = [
            (QKeySequence.StandardKey.Open, self.on_open),
            (QKeySequence.StandardKey.Copy, self.on_copy),
            (QKeySequence.StandardKey.ZoomIn, self._on_zoom_in),
            (QKeySequence.StandardKey.ZoomOut, self._on_zoom_out),
            ("Ctrl+0", self._on_reset_zoom),
            ("Meta+0", self._on_reset_zoom),
            ("Ctrl+1", self._on_fit),
            ("Meta+1", self._on_fit),
            ("Ctrl+E", self.on_export),
            ("Meta+E", self.on_export),
            ("Ctrl+D", self.on_clear_selection),
            ("Ctrl+Shift+X", self.on_clean_session),
            ("Ctrl+T", self.on_toggle_mode),
            ("Ctrl+L", self.on_save_to_library),
        ]
        self._shortcuts: list[QShortcut] = []
        for key_spec, handler in shortcut_specs:
            shortcut = QShortcut(QKeySequence(key_spec), parent_qobject)
            shortcut.activated.connect(handler)
            self._shortcuts.append(shortcut)

    def _cleanup_temp_files(self) -> None:
        """Clean up temporary files created during rotation and library operations."""
        for temp_path in self._temp_files:
            try:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    LOG.debug("Cleaned up temp file: %s", temp_path)
            except Exception as e:
                LOG.warning("Failed to clean up temp file %s: %s", temp_path, e)
        self._temp_files.clear()

    def _track_temp_file(self, file_path: str) -> None:
        """Track a temporary file for cleanup. Cleans up old temp files before adding new one."""
        # Clean up old temp files first (except _last_local_path which may still be in use)
        old_temps = [f for f in self._temp_files if f != self._last_local_path]
        for temp_path in old_temps:
            try:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    LOG.debug("Cleaned up old temp file: %s", temp_path)
            except Exception as e:
                LOG.warning("Failed to clean up old temp file %s: %s", temp_path, e)
        self._temp_files = [f for f in self._temp_files if f == self._last_local_path]

        # Track the new temp file
        self._temp_files.append(file_path)

    def on_open(self):
        # If login is required, uncomment the following block:
        # if not self.session.access_token:
        #     QMessageBox.warning(self, "Not authenticated", "Please login first (Menu > Login)")
        #     return
        try:
            file_path = self._native_open_file("Select image", "Images (*.png *.jpg *.jpeg)")
            if not file_path:
                return
            self._load_image_from_path(file_path)
        except KeyboardInterrupt:
            # User cancelled dialog or operation
            self.status_bar.showMessage("Upload cancelled", 2000)
            return
        except Exception as e:
            # Immediately flip health indicator to offline on upload failure
            if hasattr(self, "backend_status_label"):
                self.backend_status_label.setText("Backend: Offline")
                self.backend_status_label.setStyleSheet("color: #cc0000; padding: 2px 8px;")
            self._handle_backend_exception(e, context="Upload failed")
            self.status_bar.showMessage("Upload failed", 3000)

    def _load_image_from_path(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)

        self._last_local_path = file_path

        with open(file_path, "rb") as f:
            self._current_image_data = f.read()

        if sys.platform == "darwin":
            cast(QWidget, self).setWindowFilePath(file_path)

        # Load and display image immediately (UI thread)
        image = self._load_image_with_exif(file_path)
        if image.isNull():
            raise RuntimeError("Could not load selected image into viewer")

        self.src_view.set_image(image)
        # Auto-fit with margin for better initial view
        QTimer.singleShot(50, lambda: self.src_view.fit(margin_percent=5.0))
        self._on_pane_clicked("source")

        # Upload to backend asynchronously
        self.status_bar.showMessage("Uploading image...", 0)
        self.open_btn.setEnabled(False)  # Disable during upload

        runner = AsyncRunner(self.api_client.upload_image, file_path)
        runner.finished.connect(lambda result: self._on_upload_finished(file_path, result))
        runner.error.connect(lambda error: self._on_upload_error(file_path, error))

        # Run in thread pool
        thread_pool = QThreadPool.globalInstance()
        runnable = QRunnable.create(lambda: runner.run())
        runnable.setAutoDelete(True)
        thread_pool.start(runnable)

    def _on_upload_finished(self, file_path: str, payload) -> None:
        """Handle completion of async upload."""
        self.open_btn.setEnabled(True)  # Re-enable
        try:
            session_id = payload.get("id")
            if not session_id:
                raise RuntimeError("Upload succeeded but no session id returned")

            self.session.session_id = session_id
            if hasattr(self, "session_id_label"):
                self.session_id_label.setText(f"Session: {session_id[:8]}...")
                self.session_id_label.setToolTip(f"Full session ID: {session_id}")
            self.status_bar.showMessage("Image uploaded successfully", 3000)

            self._last_result_png = None
            self.preview_view.clear_image()
            self.res_view.scene().clear()
            self.export_btn.setEnabled(False)
            self.save_to_library_btn.setEnabled(False)
            # Keep panel mounted but show empty overlays
            self._set_preview_panel_visible(True)
            self.preview_label.setVisible(True)
            self.result_label.setVisible(True)
            self.preview_view.setVisible(False)
            self.res_view.setVisible(False)
            self.preview_empty.setVisible(True)
            self.result_empty.setVisible(True)

            self._update_action_states()
            self._update_view_actions_enabled()
            self._update_coordinate_display()
            self._update_pane_borders()
        except Exception as e:
            # Immediately flip health indicator to offline on upload failure
            if hasattr(self, "backend_status_label"):
                self.backend_status_label.setText("Backend: Offline")
                self.backend_status_label.setStyleSheet("color: #cc0000; padding: 2px 8px;")
            self._handle_backend_exception(e, context="Upload failed")
            self.status_bar.showMessage("Upload failed", 3000)

    def _on_upload_error(self, file_path: str, error) -> None:
        """Handle error in async upload."""
        self.open_btn.setEnabled(True)  # Re-enable
        # Immediately flip health indicator to offline on upload failure
        if hasattr(self, "backend_status_label"):
            self.backend_status_label.setText("Backend: Offline")
            self.backend_status_label.setStyleSheet("color: #cc0000; padding: 2px 8px;")
        self._handle_backend_exception(error, context="Upload failed")
        self.status_bar.showMessage("Upload failed", 3000)

    def _on_source_file_dropped(self, file_path: str) -> None:
        try:
            self._load_image_from_path(file_path)
        except Exception as exc:
            self._handle_backend_exception(exc, context="Upload via drag-and-drop failed")
            self.status_bar.showMessage("Upload failed", 3000)

    # Demo helpers for automated flows (no dialogs/backends)
    def demo_load_image(self, file_path: str) -> None:
        """Load an image into the Source pane without opening dialogs or calling backend.

        Assigns a deterministic session id suitable for offline demo flows.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)
        with open(file_path, "rb") as f:
            self._current_image_data = f.read()
        image = self._load_image_with_exif(file_path)
        if image.isNull():
            raise RuntimeError("Could not load image")
        self.src_view.set_image(image)
        self._on_pane_clicked("source")
        self.session.session_id = "demo-session"
        self.status_bar.showMessage("Demo image loaded", 1500)
        self._update_action_states()
        self._update_coordinate_display()
        self._update_pane_borders()
        if sys.platform == "darwin":
            cast(QWidget, self).setWindowFilePath(file_path)

    def demo_create_sample_image(self, width: int = 400, height: int = 300, color: str = "#ffffff") -> None:
        """Create a simple in-memory image and load it into Source."""
        from PySide6.QtGui import QImage, QColor
        img = QImage(width, height, QImage.Format.Format_RGB32)
        img.fill(QColor(color))
        self._current_image_data = None
        self.src_view.set_image(img)
        self._on_pane_clicked("source")
        self.session.session_id = "demo-session"
        self.status_bar.showMessage("Demo image created", 1200)
        self._update_action_states()
        self._update_coordinate_display()
        self._update_pane_borders()
        if sys.platform == "darwin":
            cast(QWidget, self).setWindowFilePath("")

    def demo_select_rect(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Programmatically set a selection rectangle in image/scene coordinates."""
        from PySide6.QtCore import QRectF, QPointF, QRect
        rect_scene = QRectF(QPointF(x1, y1), QPointF(x2, y2)).normalized()
        tl_view = self.src_view.mapFromScene(rect_scene.topLeft())
        br_view = self.src_view.mapFromScene(rect_scene.bottomRight())
        self.src_view._last_rect = QRect(tl_view, br_view).normalized()
        xs = [rect_scene.left(), rect_scene.right()]
        ys = [rect_scene.top(), rect_scene.bottom()]
        self.src_view._last_rect_scene_bounds = QRectF(QPointF(min(xs), min(ys)), QPointF(max(xs), max(ys)))
        # Trigger downstream preview/update like a user selection
        self.on_selection_changed(self.src_view._last_rect)

    def demo_generate_local_result(self) -> None:
        """Generate a PNG result locally from the current selection (no backend)."""
        from PySide6.QtCore import QBuffer, QIODevice
        if not self.src_view.has_image():
            raise RuntimeError("No source image")
        x1, y1, x2, y2 = self.src_view.selected_rect_image_coords()
        if x1 == x2 or y1 == y2:
            raise RuntimeError("No selection")
        cropped = self.src_view.crop_selection()
        if not cropped or cropped.isNull():
            raise RuntimeError("Invalid crop")
        buf = QBuffer()
        if not buf.open(QIODevice.OpenModeFlag.WriteOnly):
            raise RuntimeError("Buffer open failed")
        cropped.save(buf, b"PNG")
        # QBuffer.data() -> QByteArray; call .data() again to get Python bytes for mypy/runtime
        self._last_result_png = buf.data().data()
        buf.close()
        self.res_view.load_image_bytes(self._last_result_png)
        self._on_pane_clicked("result")
        self._update_action_states(preview_ready=True)
        self.status_bar.showMessage("Local result generated", 1500)
        self._update_coordinate_display()
        self._update_pane_borders()

    def _load_image_with_exif(self, file_path: str) -> QImage:
        """Load image and apply EXIF orientation correction."""
        try:
            # Use PIL to read EXIF and rotate if needed
            pil_img = cast(PILImage.Image, PILImage.open(file_path))
            
            # Check for EXIF orientation tag
            exif = pil_img.getexif()
            if exif:
                orientation = exif.get(0x0112)  # 274 is the Orientation tag
                if orientation:
                    # Apply rotation based on EXIF orientation
                    if orientation == 3:
                        pil_img = pil_img.rotate(180, expand=True)
                    elif orientation == 6:
                        pil_img = pil_img.rotate(270, expand=True)
                    elif orientation == 8:
                        pil_img = pil_img.rotate(90, expand=True)
            
            # Convert PIL image to QImage, preserving alpha if present
            has_alpha = pil_img.mode in ('RGBA', 'LA') or (pil_img.mode == 'P' and 'transparency' in pil_img.info)
            if has_alpha:
                pil_img = pil_img.convert("RGBA")
                data = pil_img.tobytes("raw", "RGBA")
                qimage = QImage(data, pil_img.width, pil_img.height, QImage.Format.Format_RGBA8888)
            else:
                pil_img = pil_img.convert("RGB")
                data = pil_img.tobytes("raw", "RGB")
                qimage = QImage(data, pil_img.width, pil_img.height, QImage.Format.Format_RGB888)
            return qimage.copy()  # Make a deep copy
        except Exception as e:
            # Fallback to basic QImage loading if EXIF fails
            LOG.warning("EXIF orientation correction failed: %s, using basic load", e)
            return QImage(file_path)

    def on_pick_color(self):
        # Initialize color picker with current color
        color_hex = self._native_color_picker(self._color_hex)
        if color_hex:
            self._color_hex = color_hex  # already #RRGGBB
            self._update_color_ui()
            self._last_result_png = None
            self.res_view.clear_image()
            self._update_action_states(preview_ready=False)
            self.schedule_preview()
            self._remember_color(self._color_hex)

    def on_preview(self):
        """Process the selected region and show the result."""
        self.status_bar.showMessage("Processing selection...", 0)
        if not self.session.session_id:
            QMessageBox.warning(cast(QWidget, self), "No image uploaded", "Please open & upload an image first")
            return
        # Selection
        x1, y1, x2, y2 = self.src_view.selected_rect_image_coords()

        # Debug logging
        LOG.debug("on_preview called")
        LOG.debug("Session ID: %s", self.session.session_id)
        LOG.debug("Selection coords: (%d, %d) → (%d, %d)", x1, y1, x2, y2)
        LOG.debug("Color: %s, Threshold: %d", self._color_hex, self.threshold.value())

        if x1 == x2 or y1 == y2:
            self.status_bar.showMessage("No region selected - drag on the source image to select a region", 4000)
            LOG.warning("on_preview called with zero-size selection: (%d,%d)→(%d,%d)", x1, y1, x2, y2)
            return

        # Validate coordinates
        if x1 >= x2 or y1 >= y2:
            LOG.error("Invalid selection coordinates: x1=%d >= x2=%d or y1=%d >= y2=%d", x1, x2, y1, y2)
            QMessageBox.warning(cast(QWidget, self), "Invalid selection", "Selection coordinates are invalid. Please try again.")
            return

        # Process asynchronously
        self.status_bar.showMessage("Processing...", 0)
        self.export_btn.setEnabled(False)  # Disable during processing

        import time
        start_time = time.time()

        runner = AsyncRunner(
            self.api_client.process_image,
            session_id=self.session.session_id,
            x1=x1, y1=y1, x2=x2, y2=y2,
            color=self._color_hex,
            threshold=int(self.threshold.value())
        )
        runner.finished.connect(lambda result: self._on_process_finished(result, start_time))
        runner.error.connect(lambda error: self._on_process_error(error, start_time))

        # Run in thread pool
        thread_pool = QThreadPool.globalInstance()
        runnable = QRunnable.create(lambda: runner.run())
        runnable.setAutoDelete(True)
        thread_pool.start(runnable)

    def _on_process_finished(self, png_bytes, start_time: float) -> None:
        """Handle completion of async processing."""
        try:
            import time
            elapsed = time.time() - start_time
            LOG.debug("Received %d bytes from backend in %.2f seconds", len(png_bytes), elapsed)

            self._last_result_png = png_bytes
            self.res_view.load_image_bytes(png_bytes)
            # Show result view, hide empty overlay
            self.result_empty.setVisible(False)
            self.res_view.setVisible(True)
            # Enable actions now that a preview exists
            self._update_action_states(preview_ready=True)
            self.status_bar.showMessage("Preview ready", 2000)
        except Exception as e:
            LOG.error("Processing failed: %s", e, exc_info=True)
            # Immediately flip health indicator to offline on processing failure
            if hasattr(self, "backend_status_label"):
                self.backend_status_label.setText("Backend: Offline")
                self.backend_status_label.setStyleSheet("color: #cc0000; padding: 2px 8px;")
            self._handle_backend_exception(e, context="Process failed")
            self.status_bar.showMessage("Processing failed", 3000)

    def _on_process_error(self, error, start_time: float) -> None:
        """Handle error in async processing."""
        LOG.error("Processing failed: %s", error, exc_info=True)
        # Immediately flip health indicator to offline on processing failure
        if hasattr(self, "backend_status_label"):
            self.backend_status_label.setText("Backend: Offline")
            self.backend_status_label.setStyleSheet("color: #cc0000; padding: 2px 8px;")
        self._handle_backend_exception(error, context="Process failed")
        self.status_bar.showMessage("Processing failed", 3000)

    def on_clear_selection(self):
        self.src_view.clear_selection()
        self.sel_info.setText("Selection: –")
        self.preview_view.clear_image()
        self.export_btn.setEnabled(False)
        self.save_to_library_btn.setEnabled(False)
        # Don't collapse panel - just show empty overlays
        self.preview_view.setVisible(False)
        self.preview_empty.setVisible(True)
        self.res_view.setVisible(False)
        self.result_empty.setVisible(True)
        self._update_view_actions_enabled()
        self._update_coordinate_display()

    def _check_backend_health(self) -> None:
        """Check backend availability asynchronously with exponential backoff."""
        # Initialize retry state on first call
        if not hasattr(self, '_health_check_attempt'):
            self._health_check_attempt = 0

        self._health_check_attempt += 1
        max_attempts = 5

        # Update UI to show checking state
        if hasattr(self, "backend_status_label"):
            self.backend_status_label.setText("⏳ Backend: Checking...")
            self.backend_status_label.setStyleSheet("color: #a37f00; padding: 2px 8px;")

        # Run health check asynchronously
        def _do_health_check():
            try:
                if hasattr(self.api_client, "health_check"):
                    return self.api_client.health_check(timeout=2.0)
                else:
                    # If client does not implement health_check (tests), assume online
                    return True, {"status": "assumed-healthy"}
            except Exception as e:
                return False, {"error": str(e)}

        runner = AsyncRunner(_do_health_check)
        runner.finished.connect(self._on_health_check_finished)
        runner.error.connect(self._on_health_check_error)

        # Run in thread pool
        thread_pool = QThreadPool.globalInstance()
        runnable = QRunnable.create(lambda: runner.run())
        runnable.setAutoDelete(True)
        thread_pool.start(runnable)

    def _on_health_check_finished(self, result) -> None:
        """Handle completion of async health check."""
        ok, payload = result
        self._backend_online = bool(ok)

        if hasattr(self, "backend_status_label"):
            if ok:
                # Success - reset attempt counter
                self._health_check_attempt = 0

                # Extract version if available
                version = payload.get("version", "unknown") if isinstance(payload, dict) else "unknown"

                self.backend_status_label.setText("● Backend: Online")
                self.backend_status_label.setStyleSheet("color: #2e7d32; padding: 2px 8px;")
                self.backend_status_label.setToolTip(
                    f"Connected to {self.api_client.base_url}\n"
                    f"Version: {version}\n"
                    f"Click to open health page"
                )
                # Make clickable
                self.backend_status_label.mousePressEvent = lambda e: self._open_url(f"{self.api_client.base_url}/health")

                # Enable actions that depend on backend
                self.open_btn.setEnabled(True)
            else:
                # Failure - check if we should retry
                if self._health_check_attempt < max_attempts:
                    # Exponential backoff: 100ms, 500ms, 1s, 2s, 5s
                    delays = [100, 500, 1000, 2000, 5000]
                    delay = delays[min(self._health_check_attempt - 1, len(delays) - 1)]

                    LOG.debug("Health check failed (attempt %d/%d), retrying in %dms",
                             self._health_check_attempt, max_attempts, delay)

                    # Schedule retry
                    QTimer.singleShot(delay, self._check_backend_health)
                else:
                    # Max attempts reached - mark as offline
                    error_msg = payload.get("error", "Unknown error") if isinstance(payload, dict) else str(payload)

                    self.backend_status_label.setText("● Backend: Offline")
                    self.backend_status_label.setStyleSheet("color: #c62828; padding: 2px 8px;")
                    self.backend_status_label.setToolTip(
                        f"Cannot reach {self.api_client.base_url}\n"
                        f"Error: {error_msg}\n"
                        f"Click for troubleshooting"
                    )
                    # Make clickable
                    self.backend_status_label.mousePressEvent = lambda e: self._open_document("docs/HELP.md")

                    # Disable upload action when offline
                    self.open_btn.setEnabled(False)

    def _on_health_check_error(self, error) -> None:
        """Handle health check exception."""
        LOG.error("Health check error: %s", error, exc_info=True)
        # Treat as failed check
        self._on_health_check_finished((False, {"error": str(error)}))

    def _handle_backend_exception(self, e: Exception, *, context: str = "Error") -> None:
        """Show user-friendly errors for backend/network issues."""
        # Default detail
        detail = str(e)
        title = context

        # Map common request exceptions to helpful messages
        cls = e.__class__
        mod = getattr(cls, "__module__", "")
        name = getattr(cls, "__name__", "")
        if mod.startswith("requests") and name in {"ConnectionError", "Timeout"}:
            base_url = getattr(self.api_client, "base_url", "http://127.0.0.1:8001")
            detail = (
                f"The backend at {base_url} is unreachable.\n\n"
                "Make sure the server is running.\n"
                "Tip: In the app menu, open Help → Open Backend Health to verify."
            )
        elif isinstance(e, FileNotFoundError):
            # Surface simple messages as-is
            detail = str(e)

        QMessageBox.critical(cast(QWidget, self), title, detail)
        # Update backend status indicator after errors
        try:
            self._check_backend_health()
        except Exception:
            pass

    def on_clean_session(self):
        if not (self.src_view.has_image() or self.preview_view.has_image() or self.res_view.has_image() or self.session.session_id):
            return
        self.src_view.clear_image()
        self.preview_view.clear_image()
        self.res_view.clear_image()
        # Keep panel mounted to prevent layout jump - show empty overlays instead
        self.preview_view.setVisible(False)
        self.preview_empty.setVisible(True)
        self.res_view.setVisible(False)
        self.result_empty.setVisible(True)
        self.sel_info.setText("Selection: –")
        self.session.session_id = ""
        if hasattr(self, "session_id_label"):
            self.session_id_label.setText("No session")
            self.session_id_label.setToolTip("")
        self._last_result_png = None
        self._current_image_data = None
        self._last_local_path = None
        self.status_bar.showMessage("Viewport cleaned", 3000)
        self._update_action_states()
        self._update_view_actions_enabled()
        self._update_coordinate_display()
        if sys.platform == "darwin":
            cast(QWidget, self).setWindowFilePath("")

    def on_selection_changed(self, _rect) -> None:
        # Update selection info and crop preview
        x1, y1, x2, y2 = self.src_view.selected_rect_image_coords()
        w, h = max(0, x2 - x1), max(0, y2 - y1)
        if w > 0 and h > 0:
            self.sel_info.setText(f"Selection: {w}×{h} at ({x1},{y1})")
            # Show preview/result panes now that we have a selection
            self._set_preview_panel_visible(True)

            # Reset preview and result view rotations when making a new selection
            # This ensures the crop preview is shown in the correct orientation
            self.preview_view.setTransform(QTransform())
            self.preview_view._rotation = 0.0
            self.res_view.setTransform(QTransform())
            self.res_view._rotation = 0.0

            cropped = self.src_view.crop_selection()
            if cropped and not cropped.isNull():
                LOG.debug("Crop preview size: %d×%d", cropped.width(), cropped.height())
                self.preview_view.set_image(cropped)
                self.preview_view.fit()
                # Show preview view, hide empty overlay
                self.preview_view.setVisible(True)
                self.preview_empty.setVisible(False)
            else:
                self.preview_view.clear_image()
            if self._auto_threshold_enabled:
                if self._apply_auto_threshold():
                    self.status_bar.showMessage("Selection changed - scheduling preview (auto threshold)", 1000)
                    self.schedule_preview()
                else:
                    self.status_bar.showMessage("Selection changed - scheduling preview (auto threshold failed)", 1000)
                    self.schedule_preview()
            else:
                self.status_bar.showMessage("Selection changed - scheduling preview", 1000)
                self.schedule_preview()
        else:
            self.sel_info.setText("Selection: –")
            self.preview_view.clear_image()
            self.save_to_library_btn.setEnabled(False)
            # Don't collapse panel - just show empty overlay
            self.preview_view.setVisible(False)
            self.preview_empty.setVisible(True)
        self._update_view_actions_enabled()
        self._update_coordinate_display()

    def on_adjustment_changed(self, value: int) -> None:
        # Update the threshold value label and badge
        if self._auto_threshold_enabled:
            self.threshold_value_label.setText(str(value))
            self.auto_threshold_badge.setText(f"AUTO")
            self.auto_threshold_badge.setVisible(True)
        else:
            self.threshold_value_label.setText(str(value))
            self.auto_threshold_badge.setVisible(False)
        # Debounce live preview when threshold changes
        self.schedule_preview()

    def schedule_preview(self):
        # Only schedule if we have a valid selection and an uploaded session
        if not self.session.session_id:
            self.status_bar.showMessage("Preview not scheduled - no session", 1000)
            return
        x1, y1, x2, y2 = self.src_view.selected_rect_image_coords()
        if x1 == x2 or y1 == y2:
            self.status_bar.showMessage(f"Preview not scheduled - zero size selection ({x1},{y1})→({x2},{y2})", 1000)
            return
        # Debounce 200ms - stop any existing timer first to prevent restart issues
        self._preview_timer.stop()
        self.status_bar.showMessage(f"Scheduling preview in 200ms for selection ({x1},{y1})→({x2},{y2})", 1000)
        self._preview_timer.start(200)

    def _on_auto_threshold_toggled(self, state: int):
        enabled = bool(state)
        self._auto_threshold_enabled = enabled
        self.threshold.setDisabled(enabled)

        if enabled:
            applied = self._apply_auto_threshold()
            if applied:
                # Show badge in auto mode
                self.threshold_value_label.setText(str(self.threshold.value()))
                self.auto_threshold_badge.setText("AUTO")
                self.auto_threshold_badge.setVisible(True)
                self.schedule_preview()
            else:
                self.status_bar.showMessage("Auto threshold needs a selection", 2000)
        else:
            # Back to manual mode - hide badge
            self.threshold_value_label.setText(str(self.threshold.value()))
            self.auto_threshold_badge.setVisible(False)
            self.status_bar.showMessage("Manual threshold control enabled", 2000)
            self.schedule_preview()

    def _apply_auto_threshold(self) -> bool:
        computed = self._compute_auto_threshold()
        if computed is None:
            return False
        value = int(round(computed))
        # Avoid unnecessary updates if value unchanged
        if value == self.threshold.value():
            return True
        self.threshold.blockSignals(True)
        self.threshold.setValue(value)
        self.threshold.blockSignals(False)
        self.status_bar.showMessage(f"Auto threshold applied: {value}", 2000)
        return True

    def _compute_auto_threshold(self) -> Optional[float]:
        cropped = self.src_view.crop_selection()
        if not cropped or cropped.isNull():
            return None
        buffer = QBuffer()
        if not buffer.open(QIODevice.OpenModeFlag.WriteOnly):
            return None
        cropped.save(buffer, "PNG")
        # Convert QByteArray to Python bytes explicitly for type checkers
        data = buffer.data().data()
        buffer.close()
        try:
            pil_img = PILImage.open(io.BytesIO(data))
            gray = pil_img.convert("L")
            arr = np.array(gray)
            if arr.size == 0:
                return None
            return float(self._otsu_threshold(arr))
        except Exception as exc:
            logging.warning("Auto threshold computation failed: %s", exc)
            return None

    def _otsu_threshold(self, gray: np.ndarray) -> int:
        # Optimize for large crops: downscale to max 512px on longest side before computing Otsu
        # This keeps latency predictable while maintaining accuracy
        h, w = gray.shape[:2] if gray.ndim >= 2 else (gray.size, 1)
        max_dim = max(h, w)
        if max_dim > 512:
            scale = 512 / max_dim
            new_h, new_w = int(h * scale), int(w * scale)
            if new_h > 0 and new_w > 0:
                from PIL import Image as PILImage
                gray_img = PILImage.fromarray(gray.astype(np.uint8))
                gray = np.array(gray_img.resize((new_w, new_h), PILImage.Resampling.BILINEAR))

        histogram, _ = np.histogram(gray, bins=256, range=(0, 256))
        total = gray.size
        if total == 0:
            return 0
        sum_total = float(np.dot(np.arange(256), histogram))
        sum_background = 0.0
        weight_background = 0
        max_variance = 0.0
        threshold = 0

        for level in range(256):
            weight_background += histogram[level]
            if weight_background == 0:
                continue
            weight_foreground = total - weight_background
            if weight_foreground == 0:
                break
            sum_background += level * histogram[level]
            mean_background = sum_background / weight_background
            mean_foreground = (sum_total - sum_background) / weight_foreground
            variance_between = weight_background * weight_foreground * (mean_background - mean_foreground) ** 2
            if variance_between > max_variance:
                max_variance = variance_between
                threshold = level

        return threshold

    def on_toggle_mode(self):
        """Toggle between selection mode and pan mode."""
        current_mode = self.src_view._selection_mode
        new_mode = not current_mode
        self.src_view.toggle_selection_mode(new_mode)
        if new_mode:
            self.toggle_mode_btn.setChecked(True)
            set_button_icon(self.toggle_mode_btn, 'mode_select', "Selection Mode: Select", use_emoji=False)
        else:
            self.toggle_mode_btn.setChecked(False)
            set_button_icon(self.toggle_mode_btn, 'mode_pan', "Pan Mode", use_emoji=False)

    def _on_source_coord_tooltips_toggled(self, state: int) -> None:
        """Toggle coordinate tooltips in Source, Preview, and Result image views."""
        enabled = bool(state)
        if hasattr(self, 'src_view') and self.src_view:
            self.src_view.enable_coordinate_tooltips(enabled)
        if hasattr(self, 'preview_view') and self.preview_view:
            self.preview_view.enable_coordinate_tooltips(enabled)
        if hasattr(self, 'res_view') and self.res_view:
            self.res_view.enable_coordinate_tooltips(enabled)

    def on_export(self):
        """Open the export dialog with professional options."""
        if not self._last_result_png:
            return
        
        self.status_bar.showMessage("Opening export dialog...", 1000)
        dialog = ExportDialog(self._last_result_png, self)
        if dialog.exec():
            self.status_bar.showMessage(f"Exported successfully", 3000)
        else:
            self.status_bar.showMessage("Export cancelled", 2000)
    
    def on_export_json(self):
        """Export basic metadata as JSON (selection, color, threshold, session, image size)."""
        try:
            x1, y1, x2, y2 = self.src_view.selected_rect_image_coords()
            img = self.src_view.image()
            meta = {
                "session_id": self.session.session_id or "",
                "selection": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                "threshold": int(self.threshold.value()),
                "color": self._color_hex,
                "image_size": {"width": int(img.width()) if img else 0, "height": int(img.height()) if img else 0}
            }
            import json
            default_name = "signature.json"
            file_path = self._native_save_file("Export Metadata As", default_name, "JSON (*.json)")
            if not file_path:
                return
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2)
            self.status_bar.showMessage(f"Saved metadata: {file_path}", 3000)
        except Exception as e:
            QMessageBox.critical(cast(QWidget, self), "Export JSON Failed", str(e))
    
    def on_save_to_library(self):
        """Quick save to library with default PNG format and metadata."""
        if getattr(self, "tab_widget", None) and self.tab_widget.currentIndex() != getattr(self, "_extraction_tab_index", 0):
            return
        if not self._last_result_png:
            return
        self.status_bar.showMessage("Saving to library...", 0)
        try:
            # Collect metadata from current extraction
            metadata = None
            try:
                x1, y1, x2, y2 = self.src_view.selected_rect_image_coords()
                img = self.src_view.image()
                metadata = {
                    "session_id": self.session.session_id or "",
                    "selection": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                    "threshold": int(self.threshold.value()),
                    "color": self._color_hex,
                    "image_size": {"width": int(img.width()) if img else 0, "height": int(img.height()) if img else 0}
                }
            except Exception:
                pass  # Save without metadata if extraction fails
            
            saved_path = lib.save_png_to_library(self._last_result_png, metadata)
            self.status_bar.showMessage(f"Saved: {saved_path}", 4000)
            self._refresh_library_list()
            if hasattr(self, "_refresh_toolbar_action_states"):
                self._refresh_toolbar_action_states()
        except Exception as e:
            QMessageBox.critical(cast(QWidget, self), "Save failed", str(e))
            self.status_bar.showMessage("Save failed", 3000)
    
    def _refresh_library_list(self):
        """Refresh library list in Extraction tab with coordinate tooltips."""
        self.library_list.clear()
        items = list(lib.list_items(limit=50))
        if not items:
            # Show friendly empty state with guidance
            empty1 = QListWidgetItem("📝 No signatures in your library yet")
            empty1.setFlags(Qt.ItemFlag.NoItemFlags)
            empty1.setForeground(Qt.GlobalColor.gray)
            empty1.setToolTip("After extracting a signature preview, click 'Save to Library' to add it here.")
            self.library_list.addItem(empty1)

            empty2 = QListWidgetItem("Tip: Hover saved items to see coordinates & metadata")
            empty2.setFlags(Qt.ItemFlag.NoItemFlags)
            empty2.setForeground(Qt.GlobalColor.gray)
            self.library_list.addItem(empty2)
        else:
            for it in items:
                text = f"{it.display_name}  ·  {it.pretty_time}"
                item = QListWidgetItem(text)
                item.setData(Qt.ItemDataRole.UserRole, it.path)
                item.setToolTip(it.tooltip_text)  # Add coordinate tooltip
                self.library_list.addItem(item)
        self._update_library_controls()

    def _update_library_controls(self):
        has_selection = bool(self.library_list.selectedItems())
        self.delete_from_library_btn.setEnabled(has_selection)

    def _set_preview_panel_visible(self, visible: bool) -> None:
        """Show or collapse the preview/result stack - natural resize to content."""
        self.preview_result_panel.setVisible(visible)
        self.preview_container.setVisible(visible)
        self.preview_label.setVisible(visible)
        self.preview_view.setVisible(visible)
        self.result_label.setVisible(visible)
        self.res_view.setVisible(visible)
        if visible:
            self.preview_result_panel.updateGeometry()
            self.preview_result_panel.adjustSize()

    def on_library_item_open(self, item: QListWidgetItem):
        path = item.data(Qt.ItemDataRole.UserRole)
        if not path:
            return
        try:
            with open(path, "rb") as f:
                data = f.read()
            # Load into Source view and create a new backend session so user can reprocess
            # Store image data for rotate operations
            self._current_image_data = data
            self.src_view.load_image_bytes(data)
            self.src_view.clear_selection()
            # Auto-fit with margin for better initial view
            QTimer.singleShot(50, lambda: self.src_view.fit(margin_percent=5.0))
            self._on_pane_clicked("source")
            # Upload to backend to establish a fresh session
            from tempfile import NamedTemporaryFile
            tmp = NamedTemporaryFile(suffix=".png", delete=False)
            tmp.write(data)
            tmp.flush()
            tmp.close()
            # Keep temp file path for rotate operations
            self._last_local_path = tmp.name
            self._track_temp_file(tmp.name)
            if sys.platform == "darwin":
                cast(QWidget, self).setWindowFilePath(path)

            # Upload to backend asynchronously
            self.status_bar.showMessage("Uploading to create session...", 0)
            runner = AsyncRunner(self.api_client.upload_image, tmp.name)
            runner.finished.connect(lambda result: self._on_library_upload_finished(tmp.name, result))
            runner.error.connect(lambda error: self._on_library_upload_error(tmp.name, error))

            # Run in thread pool
            thread_pool = QThreadPool.globalInstance()
            runnable = QRunnable.create(lambda: runner.run())
            runnable.setAutoDelete(True)
            thread_pool.start(runnable)
        except Exception as e:
            self._handle_backend_exception(e, context="Open failed")

    def _on_library_upload_finished(self, tmp_path: str, payload) -> None:
        """Handle completion of async library item upload."""
        try:
            session_id = payload.get("id") or ""
            if not session_id:
                raise RuntimeError("Upload succeeded but no session id returned")

            self.session.session_id = session_id
            if hasattr(self, "session_id_label"):
                self.session_id_label.setText(f"Session: {session_id[:8]}...")
                self.session_id_label.setToolTip(f"Full session ID: {session_id}")

            # Clear any previous result/preview; user can select and it will auto-preview
            self._last_result_png = None
            self.preview_view.clear_image()
            self.res_view.scene().clear()
            # Keep stack visible with empty overlays
            self._set_preview_panel_visible(True)
            self.preview_label.setVisible(True)
            self.result_label.setVisible(True)
            self.preview_view.setVisible(False)
            self.res_view.setVisible(False)
            self.preview_empty.setVisible(True)
            self.result_empty.setVisible(True)

            self._update_action_states(preview_ready=False)
            self._update_view_actions_enabled()
            self._update_library_controls()
            self.status_bar.showMessage("Loaded into Source from library", 3000)
        except Exception as e:
            if hasattr(self, "backend_status_label"):
                self.backend_status_label.setText("Backend: Offline")
                self.backend_status_label.setStyleSheet("color: #cc0000; padding: 2px 8px;")
            self._handle_backend_exception(e, context="Open failed")
            self.status_bar.showMessage("Upload failed", 3000)

    def _on_library_upload_error(self, tmp_path: str, error) -> None:
        """Handle error in async library item upload."""
        if hasattr(self, "backend_status_label"):
            self.backend_status_label.setText("Backend: Offline")
            self.backend_status_label.setStyleSheet("color: #cc0000; padding: 2px 8px;")
        self._handle_backend_exception(error, context="Open failed")
        self.status_bar.showMessage("Upload failed", 3000)

    def on_library_context_menu(self, pos: QPoint):
        item = self.library_list.itemAt(pos)
        if not item:
            return
        path = item.data(Qt.ItemDataRole.UserRole)
        menu = QMenu(cast(QWidget, self))
        open_act = menu.addAction("Open")
        del_act = menu.addAction("Delete")
        act = menu.exec(self.library_list.mapToGlobal(pos))
        if act == open_act:
            self.on_library_item_open(item)
        elif act == del_act:
            if lib.delete_item(path):
                self._refresh_library_list()
                self.status_bar.showMessage("Deleted", 2000)
            else:
                QMessageBox.warning(cast(QWidget, self), "Delete failed", "Could not delete the selected file.")
        self._update_library_controls()

    def on_delete_selected_library(self):
        items = self.library_list.selectedItems()
        if not items:
            return
        confirm = QMessageBox.question(
            self,
            "Delete signature",
            "Remove the selected signature from My Signatures?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return

        failed = []
        for item in items:
            path = item.data(Qt.ItemDataRole.UserRole)
            if not path:
                continue
            if not lib.delete_item(path):
                failed.append(path)

        self._refresh_library_list()
        self._update_library_controls()

        if failed:
            formatted = "\n".join(failed)
            QMessageBox.warning(cast(QWidget, self), "Delete failed", f"Could not delete:\n{formatted}")
            return

        self.status_bar.showMessage("Deleted", 2000)

    def on_rotate(self, degrees: int):
        """Rotate the active pane. Source rotates image+session, others rotate display only."""
        active = self._active_pane

        if active == "source":
            if not self._current_image_data:
                QMessageBox.information(cast(QWidget, self), "No image", "Open an image first.")
                return

            # Backup state before rotation in case upload fails
            old_image_data = self._current_image_data
            old_local_path = self._last_local_path
            old_session_id = self.session.session_id

            try:
                from tempfile import NamedTemporaryFile
                from PIL import Image as PILImage

                with PILImage.open(io.BytesIO(self._current_image_data)) as pil_img:
                    pil_img.load()
                    has_transparency = (
                        "A" in pil_img.getbands()
                        or "transparency" in pil_img.info
                    )
                    if has_transparency:
                        working = pil_img.convert("RGBA")
                        rotated = working.rotate(-degrees, expand=True, fillcolor=(0, 0, 0, 0))
                    else:
                        if pil_img.mode not in ("RGB", "L"):
                            working = pil_img.convert("RGB")
                        else:
                            working = pil_img
                        rotated = working.rotate(-degrees, expand=True)

                buffer = io.BytesIO()
                rotated.save(buffer, format="PNG")
                png_bytes = buffer.getvalue()

                tmp = NamedTemporaryFile(suffix=".png", delete=False)
                tmp.write(png_bytes)
                tmp.flush()
                tmp.close()

                self._current_image_data = png_bytes
                self._last_local_path = tmp.name
                self._track_temp_file(tmp.name)

                # Upload to backend asynchronously
                self.status_bar.showMessage("Uploading rotated image...", 0)
                self.rotate_cw_btn.setEnabled(False)  # Disable during upload
                self.rotate_ccw_btn.setEnabled(False)

                # Store backup state for revert in case of failure
                self._rotation_backup = {
                    'old_image_data': old_image_data,
                    'old_local_path': old_local_path,
                    'old_session_id': old_session_id
                }

                runner = AsyncRunner(self.api_client.upload_image, tmp.name)
                runner.finished.connect(lambda result: self._on_rotate_upload_finished(tmp.name, result))
                runner.error.connect(lambda error: self._on_rotate_upload_error(tmp.name, error))

                # Run in thread pool
                thread_pool = QThreadPool.globalInstance()
                runnable = QRunnable.create(lambda: runner.run())
                runnable.setAutoDelete(True)
                thread_pool.start(runnable)
            except Exception as e:
                # Revert state on rotation/save failure
                self._current_image_data = old_image_data
                self._last_local_path = old_local_path
                self.session.session_id = old_session_id
                LOG.warning("Rotation failed, reverted to previous state: %s", e)
                self._handle_backend_exception(e, context="Rotate failed")
                self.status_bar.showMessage("Rotate failed - state reverted", 3000)
                self._update_view_actions_enabled()
            return

    def _on_rotate_upload_finished(self, tmp_path: str, payload) -> None:
        """Handle completion of async rotation upload."""
        # Re-enable rotation buttons
        self.rotate_cw_btn.setEnabled(True)
        self.rotate_ccw_btn.setEnabled(True)

        try:
            session_id = payload.get("id") or ""
            if not session_id:
                raise RuntimeError("Upload succeeded but no session id returned")

            qimg = self._load_image_with_exif(tmp_path)
            if qimg.isNull():
                raise RuntimeError("Could not load rotated image into viewer")

            self.src_view.set_image(qimg)
            # Auto-fit after rotation for better view
            QTimer.singleShot(50, lambda: self.src_view.fit(margin_percent=5.0))
            self.session.session_id = session_id
            if hasattr(self, "session_id_label"):
                self.session_id_label.setText(f"Session: {session_id[:8]}...")
                self.session_id_label.setToolTip(f"Full session ID: {session_id}")

            # Reset previous outputs and CLEAR SELECTION (coordinates no longer valid)
            self._last_result_png = None
            self.preview_view.clear_image()
            self.res_view.scene().clear()
            # Keep stack visible with empty overlays
            self._set_preview_panel_visible(True)
            self.preview_label.setVisible(True)
            self.result_label.setVisible(True)
            self.preview_view.setVisible(False)
            self.res_view.setVisible(False)
            self.preview_empty.setVisible(True)
            self.result_empty.setVisible(True)
            self.src_view.clear_selection()
            self.sel_info.setText("Selection: –")
            self._update_action_states()
            self._update_view_actions_enabled()
            self.status_bar.showMessage("Rotated source and re-uploaded - make a new selection", 3000)
            if sys.platform == "darwin":
                cast(QWidget, self).setWindowFilePath(self._last_local_path or "")

            # Clear backup state on success
            if hasattr(self, '_rotation_backup'):
                delattr(self, '_rotation_backup')
        except Exception as e:
            # Revert to backup state on upload failure
            if hasattr(self, '_rotation_backup'):
                backup = self._rotation_backup
                self._current_image_data = backup['old_image_data']
                self._last_local_path = backup['old_local_path']
                self.session.session_id = backup['old_session_id']
                delattr(self, '_rotation_backup')
                LOG.warning("Rotation upload failed, reverted to previous state: %s", e)
            if hasattr(self, "backend_status_label"):
                self.backend_status_label.setText("Backend: Offline")
                self.backend_status_label.setStyleSheet("color: #cc0000; padding: 2px 8px;")
            self._handle_backend_exception(e, context="Rotate failed")
            self.status_bar.showMessage("Rotate failed - state reverted", 3000)
            self._update_view_actions_enabled()

    def _on_rotate_upload_error(self, tmp_path: str, error) -> None:
        """Handle error in async rotation upload."""
        # Re-enable rotation buttons
        self.rotate_cw_btn.setEnabled(True)
        self.rotate_ccw_btn.setEnabled(True)

        # Revert to backup state on upload failure
        if hasattr(self, '_rotation_backup'):
            backup = self._rotation_backup
            self._current_image_data = backup['old_image_data']
            self._last_local_path = backup['old_local_path']
            self.session.session_id = backup['old_session_id']
            delattr(self, '_rotation_backup')
            LOG.warning("Rotation upload failed, reverted to previous state: %s", error)
        if hasattr(self, "backend_status_label"):
            self.backend_status_label.setText("Backend: Offline")
            self.backend_status_label.setStyleSheet("color: #cc0000; padding: 2px 8px;")
        self._handle_backend_exception(error, context="Rotate failed")
        self.status_bar.showMessage("Rotate failed - state reverted", 3000)
        self._update_view_actions_enabled()

    def _update_color_ui(self):
        # Update color label text and swatch background
        hexc = self._color_hex
        self.color_label.setText(f"Color: {hexc}")
        # Choose text color based on luminance for readability
        try:
            r = int(hexc[1:3], 16); g = int(hexc[3:5], 16); b = int(hexc[5:7], 16)
            lum = 0.299*r + 0.587*g + 0.114*b
            text_color = '#000000' if lum > 186 else '#ffffff'
        except Exception:
            text_color = '#000000'
        self.color_label.setStyleSheet(f"background-color: {hexc}; color: {text_color}; border: 1px solid #ccc; padding: 4px 8px; border-radius: 8px;")

    def _remember_color(self, color: str, suppress_preview: bool = False) -> None:
        qcolor = QColor(color)
        if not qcolor.isValid():
            return
        normalized = qcolor.name().upper()
        if normalized in self._color_history:
            self._color_history.remove(normalized)
        self._color_history.insert(0, normalized)
        self._color_history = self._color_history[:3]
        self._refresh_color_history()

    def _refresh_color_history(self) -> None:
        self._clear_layout(self.color_history_layout)
        if not self._color_history:
            return
        for color in self._color_history:
            btn = self._make_color_button(color)
            btn.setToolTip(f"Recent: {color}")
            btn.clicked.connect(partial(self._apply_color_from_button, color))
            self.color_history_layout.addWidget(btn)

    def _populate_color_presets(self) -> None:
        self._clear_layout(self.color_presets_layout)
        for color in self._color_presets:
            btn = self._make_color_button(color)
            btn.setToolTip(f"Preset: {color}")
            btn.clicked.connect(partial(self._apply_color_from_button, color))
            self.color_presets_layout.addWidget(btn)

    def _apply_color_from_button(self, color: str) -> None:
        qcolor = QColor(color)
        if not qcolor.isValid():
            return
        normalized = qcolor.name()
        if normalized != self._color_hex:
            self._color_hex = normalized
            self._update_color_ui()
        self._remember_color(normalized, suppress_preview=True)
        self._last_result_png = None
        self.res_view.clear_image()
        self._update_action_states(preview_ready=False)
        self.schedule_preview()

    def _make_section_label(self, text: str, color_hex: Optional[str], *, top_margin: int = 12) -> QLabel:
        label = QLabel(text.upper())
        margin = max(top_margin, 0)
        if color_hex is None:
            # Use bright white for maximum contrast
            color_hex = "#FFFFFF"
        label.setStyleSheet(
            "font-size: 10px; font-weight: 700; letter-spacing: 1.2px;"
            f"margin-top: {margin}px; margin-bottom: 4px; color: {color_hex};"
        )
        return label

    def _make_secondary_label(self, text: str, color_hex: Optional[str]) -> QLabel:
        label = QLabel(text)
        if color_hex is None:
            # Use bright white for readability instead of calculated dim color
            color_hex = "#FFFFFF"
        label.setStyleSheet(
            "font-size: 11px; font-weight: 500; letter-spacing: 0.3px;"
            f"color: {color_hex};"
        )
        return label

    def _make_color_button(self, color: str) -> QToolButton:
        btn = QToolButton(cast(QWidget, self))
        btn.setAutoRaise(True)
        btn.setFixedSize(22, 22)
        btn.setStyleSheet(
            "QToolButton {"
            f"background-color: {color};"
            "border: 1px solid rgba(0,0,0,64);"
            "border-radius: 8px;"
            "}"
            "QToolButton:hover {"
            "border-color: rgba(0,0,0,115);"
            "}"
        )
        return btn

    @staticmethod
    def _clear_layout(layout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
            elif item.layout():
                ExtractionTabMixin._clear_layout(item.layout())

    # -------- License/Evaluation helpers --------
    def _update_action_states(self, preview_ready: bool = False):
        """Enable or disable actions based on whether a processed preview exists."""
        has_preview = bool(preview_ready or self._last_result_png)
        self.export_btn.setEnabled(has_preview)
        self.export_json_btn.setEnabled(True)  # Allow exporting metadata even without preview
        self.save_to_library_btn.setEnabled(has_preview)
        self.copy_btn.setEnabled(has_preview)
        self._update_view_actions_enabled()
        self._adjust_pane_layout()  # Dynamically adjust layout based on content
        if hasattr(self, "_refresh_toolbar_action_states"):
            self._refresh_toolbar_action_states()

    def _adjust_pane_layout(self):
        """Intelligently resize panes: minimize source, maximize result when extraction active.

        Note: This method is disabled to allow users to manually resize panes.
        The automatic resizing was interfering with user control.
        """
        # DISABLED: Automatic layout adjustment was preventing manual resizing
        # Original behavior kept panes changing size automatically which was confusing
        # Users should have full control over pane sizes
        pass

    def _update_pane_labels_with_zoom(self):
        """Update pane labels to show current zoom percentage."""
        if self.src_view.has_image():
            zoom = self.src_view.get_zoom_percent()
            self.source_label.setText(f"Source {zoom:.0f}%")
        else:
            self.source_label.setText("Source")

        if self.preview_view.has_image():
            zoom = self.preview_view.get_zoom_percent()
            self.preview_label.setText(f"Crop preview {zoom:.0f}%")
        else:
            self.preview_label.setText("Crop preview")

        if self.res_view.has_image():
            zoom = self.res_view.get_zoom_percent()
            self.result_label.setText(f"Result {zoom:.0f}%")
        else:
            self.result_label.setText("Result")

    def _update_view_actions_enabled(self):
        """Enable/disable zoom and rotate buttons based on active pane and content."""
        has_source = self.src_view.has_image()
        has_preview = self.preview_view.has_image()
        has_result = self.res_view.has_image()

        active_has_image = {
            "source": has_source,
            "preview": has_preview,
            "result": has_result,
        }.get(self._active_pane, False)

        for btn in (self.zoom_in_btn, self.zoom_out_btn, self.fit_btn, self.reset_view_btn):
            btn.setEnabled(active_has_image)
        self.zoom_combo.setEnabled(active_has_image)

        rotate_enabled = False
        if self._active_pane == "source":
            rotate_enabled = self._current_image_data is not None
        elif self._active_pane == "preview":
            rotate_enabled = has_preview
        elif self._active_pane == "result":
            rotate_enabled = has_result

        self.rotate_cw_btn.setEnabled(rotate_enabled)
        self.rotate_ccw_btn.setEnabled(rotate_enabled)
        has_any = has_source or has_preview or has_result or bool(self.session.session_id)
        self.clean_session_btn.setEnabled(has_any)

    def on_copy(self):
        if not self._last_result_png:
            return
        try:
            img = QImage.fromData(self._last_result_png, "PNG")
            if img.isNull():
                raise RuntimeError("Could not decode result image for clipboard")

            # Ensure proper alpha handling across platforms
            # Convert to ARGB32_Premultiplied to avoid dim colors on Windows
            if img.hasAlphaChannel():
                img = img.convertToFormat(QImage.Format.Format_ARGB32_Premultiplied)

            QApplication.clipboard().setPixmap(QPixmap.fromImage(img))
            self.status_bar.showMessage("Copied to clipboard", 2000)
        except Exception as e:
            QMessageBox.critical(cast(QWidget, self), "Copy Failed", str(e))

    def on_enter_license(self):
        dlg = LicenseDialog(self)
        if dlg.exec():
            self._licensed = is_licensed()
            self.status_bar.showMessage("Thanks! License saved.", 3000)
            # No gating; just keep a record for future features
            self._update_action_states(preview_ready=bool(self._last_result_png))

    def on_buy_license(self):
        # Open Gumroad product page (set GUMROAD_PRODUCT_URL in environment or .env)
        url = os.getenv("GUMROAD_PRODUCT_URL", "https://gumroad.com/l/signature-extractor")
        QDesktopServices.openUrl(url)

    # No activation prompt; purchase is optional and handled via menu link.

    def _open_document(self, relative_path: str) -> None:
        """Open a markdown document in a nice dialog with rendered HTML."""
        try:
            dialog = HelpDialog(relative_path, self)
            dialog.exec()
        except Exception as exc:
            QMessageBox.warning(cast(QWidget, self), "Unable to open document", str(exc))

    def _open_url(self, url: str) -> None:
        try:
            QDesktopServices.openUrl(QUrl(url))
        except Exception as exc:
            QMessageBox.warning(cast(QWidget, self), "Unable to open URL", str(exc))

    def _on_zoom_in(self):
        """Zoom in on active pane."""
        active_view = self._get_active_view()
        if active_view and active_view.has_image():
            active_view.zoom_in()
            # Sync zoom combo to reflect new zoom level
            zoom_percent = active_view.get_zoom_percent()
            zoom_text = f"{zoom_percent:.0f}%"
            self._updating_zoom_combo = True
            self.zoom_combo.setCurrentText(zoom_text)
            self._last_valid_zoom_text = zoom_text
            self._updating_zoom_combo = False
        self._update_coordinate_display()
    
    def _on_zoom_out(self):
        """Zoom out on active pane."""
        active_view = self._get_active_view()
        if active_view and active_view.has_image():
            active_view.zoom_out()
            # Sync zoom combo to reflect new zoom level
            zoom_percent = active_view.get_zoom_percent()
            zoom_text = f"{zoom_percent:.0f}%"
            self._updating_zoom_combo = True
            self.zoom_combo.setCurrentText(zoom_text)
            self._last_valid_zoom_text = zoom_text
            self._updating_zoom_combo = False
        self._update_coordinate_display()
    
    def _on_reset_zoom(self):
        """Reset zoom to 100% on active pane."""
        active_view = self._get_active_view()
        if active_view and active_view.has_image():
            active_view.reset_zoom()
            active_view.centerOn(active_view.sceneRect().center())
            # Sync zoom combo to show 100%
            self._updating_zoom_combo = True
            self.zoom_combo.setCurrentText("100%")
            self._last_valid_zoom_text = "100%"
            self._updating_zoom_combo = False
        self._update_coordinate_display()

    def _on_fit(self):
        """Fit to window on active pane."""
        active_view = self._get_active_view()
        if active_view and active_view.has_image():
            active_view.fit()
            # Sync zoom combo to show "Fit"
            self._updating_zoom_combo = True
            self.zoom_combo.setCurrentText("Fit")
            self._last_valid_zoom_text = "Fit"
            self._updating_zoom_combo = False
        self._update_coordinate_display()

    def _on_zoom_combo_activated(self, index: int):
        if self._updating_zoom_combo:
            return
        text = self.zoom_combo.itemText(index)
        self._apply_zoom_text(text)

    def _on_zoom_combo_edit_finished(self):
        if self._updating_zoom_combo:
            return
        text = self.zoom_combo.currentText()
        self._apply_zoom_text(text)

    def _apply_zoom_text(self, text: str):
        text = (text or "").strip()
        if not text:
            return
        if text.lower() == "fit":
            self._on_fit()
            # Update combo to show "Fit" and cache it
            self._updating_zoom_combo = True
            self.zoom_combo.setCurrentText("Fit")
            self._last_valid_zoom_text = "Fit"
            self._updating_zoom_combo = False
            return

        # Get current valid zoom before attempting change
        active_view = self._get_active_view()
        if not active_view or not active_view.has_image():
            self._update_coordinate_display()
            return
        current_zoom = active_view.get_zoom_percent()

        if text.endswith("%"):
            text = text[:-1]
        try:
            value = float(text)
        except ValueError:
            self.status_bar.showMessage("Invalid zoom value - enter a number like 150 or 'Fit'", 3000)
            # Restore last valid value from cache
            fallback = getattr(self, "_last_valid_zoom_text", f"{current_zoom:.0f}%")
            self._updating_zoom_combo = True
            self.zoom_combo.setCurrentText(fallback)
            self._updating_zoom_combo = False
            self._update_coordinate_display()
            return
        if value <= 0:
            self.status_bar.showMessage("Zoom value must be greater than 0", 3000)
            # Restore last valid value from cache
            fallback = getattr(self, "_last_valid_zoom_text", f"{current_zoom:.0f}%")
            self._updating_zoom_combo = True
            self.zoom_combo.setCurrentText(fallback)
            self._updating_zoom_combo = False
            self._update_coordinate_display()
            return

        active_view.set_zoom_percent(value)
        # Normalize combo text to show actual applied zoom (may differ slightly due to rounding)
        actual_zoom = active_view.get_zoom_percent()
        display_text = f"{actual_zoom:.0f}%"
        self._updating_zoom_combo = True
        self.zoom_combo.setCurrentText(display_text)
        self._last_valid_zoom_text = display_text
        self._updating_zoom_combo = False
        self._update_coordinate_display()

    def _apply_left_panel_breakpoint(self):
        """Apply breakpoint-based label shortening and section collapsing for narrow panels."""
        # Shorten labels when panel width is less than 300px
        panel_width = self._left_panel.width() if hasattr(self, '_left_panel') else 300

        # Also check main window width for global narrow mode
        window_width = self.width() if hasattr(self, 'width') else 1200
        is_narrow = window_width < 1000

        if panel_width < 300 or is_narrow:
            # Shorten long button texts
            self.open_btn.setText("Open")
            self.toggle_mode_btn.setText("Mode")
            self.clear_sel_btn.setText("Clear")
            self.clean_session_btn.setText("Clean")
            self.export_btn.setText("Export")
            self.save_to_library_btn.setText("Save")
            self.export_json_btn.setText("JSON")
            self.delete_from_library_btn.setText("Delete")

            # Collapse non-essential sections in narrow mode
            if is_narrow:
                if hasattr(self, '_welcome_label'):
                    self._welcome_label.hide()
                if hasattr(self, '_library_section_label'):
                    self._library_section_label.hide()
                if hasattr(self, 'library_list'):
                    self.library_list.hide()
                if hasattr(self, 'delete_from_library_btn'):
                    self.delete_from_library_btn.hide()
        else:
            # Restore full button texts
            self.open_btn.setText("Open & Upload Image")
            # Update toggle mode text based on current state
            if self.toggle_mode_btn.isChecked():
                self.toggle_mode_btn.setText("Selection Mode: Select")
            else:
                self.toggle_mode_btn.setText("Pan Mode")
            self.clear_sel_btn.setText("Clear Selection")
            self.clean_session_btn.setText("Clean Viewport")
            self.export_btn.setText("Export...")
            self.save_to_library_btn.setText("Save to Library")
            self.export_json_btn.setText("Export JSON")
            self.delete_from_library_btn.setText("Delete Selected")

            # Show all sections when not narrow
            if hasattr(self, '_welcome_label'):
                self._welcome_label.show()
            if hasattr(self, '_library_section_label'):
                self._library_section_label.show()
            if hasattr(self, 'library_list'):
                self.library_list.show()
            if hasattr(self, 'delete_from_library_btn'):
                self.delete_from_library_btn.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Defer update to ensure layouts settle before querying viewport sizes
        QTimer.singleShot(0, self._update_coordinate_display)
        QTimer.singleShot(0, self._apply_left_panel_breakpoint)
    
