from __future__ import annotations

import logging
import sys
from typing import Optional, cast

from PySide6.QtCore import QSettings, QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QWidget, QTabWidget

from desktop_app.api.client import ApiClient
from desktop_app.resources.icons import get_icon
from desktop_app.state.session import SessionState
from desktop_app.views.onboarding_dialog import OnboardingDialog
from desktop_app.views.main_window_parts import (
    ExtractionTabMixin,
    NativeDialogsMixin,
    PaneStatusMixin,
    PdfTabMixin,
    ThemeMixin,
    ToolbarMixin,
    PDF_AVAILABLE,
    PDF_IMPORT_ERROR,
)

LOG = logging.getLogger(__name__)


class MainWindow(
    QMainWindow,
    ThemeMixin,
    PaneStatusMixin,
    NativeDialogsMixin,
    ToolbarMixin,
    ExtractionTabMixin,
    PdfTabMixin,
):
    """Top-level window that orchestrates extraction and PDF signing flows."""

    def __init__(self, api_client: ApiClient, session_state: SessionState, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.api_client = api_client
        self.session = session_state

        self.setWindowTitle("Signature Extractor (Desktop)")
        app_icon = get_icon("file")
        if not app_icon.isNull():
            self.setWindowIcon(app_icon)

        self._apply_theme()

        central = QWidget(self)
        self.setCentralWidget(central)
        root = QHBoxLayout(central)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
        self.tab_widget.setAccessibleName("Main workflow tabs")
        self.tab_widget.setAccessibleDescription("Switch between signature extraction and PDF signing workflows")
        if sys.platform == "darwin":
            self.tab_widget.setDocumentMode(True)
            self.tab_widget.setMovable(True)

        self._setup_extraction_ui()
        self._setup_pdf_ui()
        root.addWidget(self.tab_widget)

        self._init_status_bar()
        self._setup_main_toolbar()
        if PDF_AVAILABLE:
            self.status_bar.showMessage("Ready - PDF features enabled", 2000)
        else:
            detail = f"Ready - PDF features unavailable (install pypdfium2 and pikepdf)"
            if PDF_IMPORT_ERROR:
                LOG.warning("PDF features disabled: %s", PDF_IMPORT_ERROR)
                detail = f"{detail}: {PDF_IMPORT_ERROR}"
            self.status_bar.showMessage(detail, 4000)

        # macOS palette needs reapplication after views exist (see docs/APPLE_NATIVE_IMPROVEMENTS.md)
        self._setup_dark_mode_support()

        self._setup_menus()

        self._backend_online = False
        try:
            QTimer.singleShot(10, self._check_backend_health)
        except Exception:
            LOG.debug("Backend health check scheduling failed", exc_info=True)

        # Initialize responsive mode flags
        self._is_compact: bool = False
        self._is_narrow: bool = False

        # Restore window state from previous session
        self._restore_window_state()

        # Show onboarding dialog on first run
        QTimer.singleShot(500, self._maybe_show_onboarding)

    # ----- Onboarding -----
    def _maybe_show_onboarding(self) -> None:
        """Show onboarding dialog if this is the first run."""
        settings = QSettings("SignatureExtractor", "DesktopApp")
        should_show = settings.value("onboarding/show_on_startup", True, type=bool)

        if should_show:
            dialog = OnboardingDialog(self)

            # Set up backend health check callback
            def check_backend(callback):
                try:
                    if hasattr(self.api_client, "health_check"):
                        ok, payload = self.api_client.health_check(timeout=2.0)
                        if ok:
                            version = payload.get("version", "unknown") if isinstance(payload, dict) else "unknown"
                            callback(True, f"Version {version}")
                        else:
                            error = payload.get("error", "Unknown error") if isinstance(payload, dict) else str(payload)
                            callback(False, error)
                    else:
                        callback(True, "Connected")
                except Exception as e:
                    callback(False, str(e))

            dialog.set_backend_check_function(check_backend)

            # Show dialog and save preference
            if dialog.exec():
                settings.setValue("onboarding/show_on_startup", dialog.should_show_again())

    # ----- Window State Persistence -----
    def _restore_window_state(self) -> None:
        """Restore window geometry and last active tab from previous session."""
        settings = QSettings("SignatureExtractor", "DesktopApp")

        # Restore window geometry (size and position)
        geometry = settings.value("window/geometry")
        if geometry:
            try:
                self.restoreGeometry(geometry)
                LOG.debug("Restored window geometry from settings")
            except Exception as e:
                LOG.debug("Failed to restore window geometry: %s", e)
        else:
            # Default size if no saved geometry
            self.resize(1400, 900)

        # Restore window state (maximized, etc.)
        window_state = settings.value("window/state")
        if window_state:
            try:
                self.restoreState(window_state)
                LOG.debug("Restored window state from settings")
            except Exception as e:
                LOG.debug("Failed to restore window state: %s", e)

        # Restore last active tab
        last_tab_value = settings.value("window/last_tab", 0)
        try:
            last_tab = cast(int, int(last_tab_value))  # ensure QVariant/object converts cleanly
        except (TypeError, ValueError):
            last_tab = 0

        if 0 <= last_tab < self.tab_widget.count():
            self.tab_widget.setCurrentIndex(last_tab)
            LOG.debug("Restored last active tab: %d", last_tab)

    def _save_window_state(self) -> None:
        """Save window geometry and active tab for next session."""
        settings = QSettings("SignatureExtractor", "DesktopApp")

        # Save window geometry
        settings.setValue("window/geometry", self.saveGeometry())

        # Save window state
        settings.setValue("window/state", self.saveState())

        # Save current tab
        current_tab = self.tab_widget.currentIndex()
        settings.setValue("window/last_tab", current_tab)

        LOG.debug("Saved window state: tab=%d", current_tab)

    # ----- Responsive breakpoints -----
    def _apply_responsive_breakpoints(self) -> None:
        """Apply responsive layout changes based on window width.

        Breakpoints:
        - Wide (≥1400px): Full layout with all features visible
        - Compact (1000-1399px): Reduced sidebar, icon-heavy controls
        - Narrow (<1000px): Collapsed groups, single pane view
        """
        width: int = self.width()

        # Determine new states
        new_compact: bool = width < 1400
        new_narrow: bool = width < 1000

        # Only update if state changed
        if new_compact != self._is_compact or new_narrow != self._is_narrow:
            self._is_compact = new_compact
            self._is_narrow = new_narrow

            # Update sidebar if it exists
            if hasattr(self, '_left_panel'):
                self._left_panel.setProperty("compact", self._is_compact)
                self._left_panel.setProperty("narrow", self._is_narrow)

                # Adjust sidebar width
                if self._is_narrow:
                    self._left_panel.setFixedWidth(260)
                elif self._is_compact:
                    self._left_panel.setFixedWidth(280)
                else:
                    self._left_panel.setFixedWidth(300)

                # Refresh styles
                self._left_panel.style().unpolish(self._left_panel)
                self._left_panel.style().polish(self._left_panel)

            # Collapse/expand sections in narrow mode
            if hasattr(self, '_apply_narrow_mode'):
                self._apply_narrow_mode(self._is_narrow)

            LOG.debug("Responsive mode: compact=%s, narrow=%s, width=%d",
                     self._is_compact, self._is_narrow, width)

    # ----- Menu configuration -----
    def _setup_menus(self) -> None:
        menu_bar = self.menuBar()

        license_menu = menu_bar.addMenu("License")

        # Check current license status
        from desktop_app.license.storage import is_licensed, load_license
        is_active = is_licensed()

        # License status action (non-clickable info)
        if is_active:
            license_info = load_license()
            email_text = f" ({license_info.email})" if license_info and license_info.email else ""
            status_action = QAction(f"✓ Licensed{email_text}", self)
            status_action.setEnabled(False)
            license_menu.addAction(status_action)
            license_menu.addSeparator()
        else:
            status_action = QAction("⚠ No License (Trial Mode)", self)
            status_action.setEnabled(False)
            license_menu.addAction(status_action)
            license_menu.addSeparator()

        self.enter_license_action = QAction("Enter License Key…", self)
        self.enter_license_action.triggered.connect(self.on_enter_license)
        # Disable "Enter License" if already licensed
        if is_active:
            self.enter_license_action.setEnabled(False)
            self.enter_license_action.setText("License Already Active")
        license_menu.addAction(self.enter_license_action)

        self.buy_license_action = QAction("Buy License…", self)
        self.buy_license_action.triggered.connect(self.on_buy_license)
        license_menu.addAction(self.buy_license_action)

        help_menu = menu_bar.addMenu("Help")
        self.open_help_action = QAction("Help & Troubleshooting", self)
        self.open_help_action.triggered.connect(lambda: self._open_document("docs/HELP.md"))
        help_menu.addAction(self.open_help_action)

        self.open_shortcuts_action = QAction("Keyboard Shortcuts", self)
        self.open_shortcuts_action.triggered.connect(lambda: self._open_document("docs/SHORTCUTS.md"))
        help_menu.addAction(self.open_shortcuts_action)

        help_menu.addSeparator()

        self.check_health_action = QAction("Open Backend Health", self)
        self.check_health_action.triggered.connect(lambda: self._open_url(f"{self.api_client.base_url}/health"))
        help_menu.addAction(self.check_health_action)

    # ----- Qt overrides -----
    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.defer_coordinate_update()
        self._apply_responsive_breakpoints()

    def closeEvent(self, event) -> None:
        """Save window state before closing."""
        self._save_window_state()
        super().closeEvent(event)


__all__ = ["MainWindow"]
