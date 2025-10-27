from __future__ import annotations

import io
import os
from typing import Optional
import logging

import numpy as np
from PySide6.QtCore import Qt, QTimer, QPoint, QBuffer
from PySide6.QtGui import QAction, QImage, QColor, QPixmap, QTransform, QDesktopServices, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QLabel, QSlider, QColorDialog, QMessageBox, QListWidget, QListWidgetItem, QStatusBar,
    QMenu, QSizePolicy, QApplication, QCheckBox
)
from PIL import Image as PILImage
from PIL.ExifTags import TAGS

from desktop_app.api.client import ApiClient
from desktop_app.state.session import SessionState
from desktop_app.widgets.image_view import ImageView
from desktop_app.views.export_dialog import ExportDialog
from desktop_app.resources.icons import set_button_icon, get_icon
from desktop_app.license.storage import is_licensed, load_license
from desktop_app.views.license_dialog import LicenseDialog
from desktop_app.library import storage as lib


class MainWindow(QMainWindow):
    def __init__(self, api_client, session_state, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.session = session_state

        self.setWindowTitle("Signature Extractor (Desktop)")
        
        # Set application icon
        app_icon = get_icon('file')
        if not app_icon.isNull():
            self.setWindowIcon(app_icon)
        
        # Apply color theme
        self._apply_theme()

        # Central UI
        central = QWidget(self)
        self.setCentralWidget(central)
        root = QHBoxLayout(central)

        # Left panel with fixed width to avoid taking half the window
        left_panel = QWidget(self)
        left_panel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        left_panel.setFixedWidth(320)
        controls = QVBoxLayout(left_panel)
        self.open_btn = QPushButton()
        set_button_icon(self.open_btn, 'open', 'Open & Upload Image')
        self.open_btn.clicked.connect(self.on_open)
        controls.addWidget(self.open_btn)

        controls.addWidget(QLabel("Threshold"))
        self.threshold = QSlider(Qt.Horizontal)
        self.threshold.setRange(0, 255)
        self.threshold.setValue(200)
        controls.addWidget(self.threshold)

        # Color swatch + label
        self.color_label = QLabel("Color: #000000")
        self.pick_color_btn = QPushButton()
        set_button_icon(self.pick_color_btn, 'color', 'Pick Color')
        self.pick_color_btn.clicked.connect(self.on_pick_color)
        controls.addWidget(self.color_label)
        controls.addWidget(self.pick_color_btn)

        self.auto_threshold_cb = QCheckBox("Auto threshold")
        self.auto_threshold_cb.setToolTip("Let the backend compute an optimal threshold based on the selection")
        self.auto_threshold_cb.setChecked(False)
        self.auto_threshold_cb.stateChanged.connect(self._on_auto_threshold_toggled)
        controls.addWidget(self.auto_threshold_cb)

        # View Controls (grouped clearly)
        controls.addWidget(QLabel("View"))
        view_row1 = QHBoxLayout()
        self.zoom_in_btn = QPushButton("Zoom In")
        self.zoom_in_btn.setToolTip("Zoom In (Ctrl/Cmd +) - applies to active pane")
        self.zoom_out_btn = QPushButton("Zoom Out")
        self.zoom_out_btn.setToolTip("Zoom Out (Ctrl/Cmd -) - applies to active pane")
        view_row1.addWidget(self.zoom_in_btn)
        view_row1.addWidget(self.zoom_out_btn)
        controls.addLayout(view_row1)
        
        view_row2 = QHBoxLayout()
        self.fit_btn = QPushButton("Fit")
        self.fit_btn.setToolTip("Fit to View (Ctrl/Cmd 1) - applies to active pane")
        self.reset_view_btn = QPushButton("100%")
        self.reset_view_btn.setToolTip("Reset to 100% (Ctrl/Cmd 0) - applies to active pane")
        view_row2.addWidget(self.fit_btn)
        view_row2.addWidget(self.reset_view_btn)
        controls.addLayout(view_row2)
        
        # Image Controls (grouped clearly)
        controls.addWidget(QLabel("Image"))
        rotate_row = QHBoxLayout()
        self.rotate_ccw_btn = QPushButton("↺ CCW")
        self.rotate_ccw_btn.setToolTip("Rotate Counter-Clockwise 90° (Ctrl/Cmd [)")
        self.rotate_cw_btn = QPushButton("↻ CW")
        self.rotate_cw_btn.setToolTip("Rotate Clockwise 90° (Ctrl/Cmd ])")
        rotate_row.addWidget(self.rotate_ccw_btn)
        rotate_row.addWidget(self.rotate_cw_btn)
        controls.addLayout(rotate_row)
        
        # Selection Controls (grouped clearly)
        controls.addWidget(QLabel("Selection"))
        self.toggle_mode_btn = QPushButton("🎯 Mode: Select")
        self.toggle_mode_btn.setToolTip("Toggle between Select and Pan modes")
        self.clear_sel_btn = QPushButton("Clear Selection")
        self.clear_sel_btn.setToolTip("Clear current selection")
        controls.addWidget(self.toggle_mode_btn)
        controls.addWidget(self.clear_sel_btn)
        
        self.zoom_in_btn.clicked.connect(self._on_zoom_in)
        self.zoom_out_btn.clicked.connect(self._on_zoom_out)
        self.fit_btn.clicked.connect(self._on_fit)
        self.reset_view_btn.clicked.connect(self._on_reset_zoom)
        self.toggle_mode_btn.clicked.connect(self.on_toggle_mode)
        self.clear_sel_btn.clicked.connect(self.on_clear_selection)
        self.rotate_cw_btn.clicked.connect(lambda: self.on_rotate(90))
        self.rotate_ccw_btn.clicked.connect(lambda: self.on_rotate(-90))

        self.sel_info = QLabel("Selection: –")
        self.sel_info.setStyleSheet("font-size: 11px; color: #666; padding: 4px;")
        controls.addWidget(self.sel_info)

        # Export & Save (grouped clearly)
        controls.addWidget(QLabel("Export & Save"))
        self.export_btn = QPushButton("Export...")
        self.export_btn.setToolTip("Export with advanced options (background, trim, format) - Ctrl/Cmd E")
        self.export_btn.clicked.connect(self.on_export)
        self.export_btn.setEnabled(False)

        self.copy_btn = QPushButton("Copy")
        self.copy_btn.setToolTip("Copy result to clipboard (preserves transparency) - Ctrl/Cmd C")
        self.copy_btn.clicked.connect(self.on_copy)
        self.copy_btn.setEnabled(False)

        self.save_to_library_btn = QPushButton("Save to Library")
        self.save_to_library_btn.setToolTip("Quick save as PNG to local library")
        self.save_to_library_btn.clicked.connect(self.on_save_to_library)
        self.save_to_library_btn.setEnabled(False)

        # Export JSON metadata
        self.export_json_btn = QPushButton("Export JSON")
        self.export_json_btn.setToolTip("Save selection, threshold, color, and session info to JSON")
        self.export_json_btn.clicked.connect(self.on_export_json)
        self.export_json_btn.setEnabled(False)

        controls.addWidget(self.export_btn)
        controls.addWidget(self.copy_btn)
        controls.addWidget(self.save_to_library_btn)
        controls.addWidget(self.export_json_btn)

        # Library list
        controls.addWidget(QLabel("My Signatures"))
        self.library_list = QListWidget()
        self.library_list.itemDoubleClicked.connect(self.on_library_item_open)
        self.library_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.library_list.customContextMenuRequested.connect(self.on_library_context_menu)
        self.library_list.itemSelectionChanged.connect(self._update_library_controls)
        self.library_list.setMinimumHeight(120)
        controls.addWidget(self.library_list)

        self.delete_from_library_btn = QPushButton("Delete Selected")
        self.delete_from_library_btn.setToolTip("Remove the selected signature from My Signatures")
        self.delete_from_library_btn.clicked.connect(self.on_delete_selected_library)
        self.delete_from_library_btn.setEnabled(False)
        controls.addWidget(self.delete_from_library_btn)
        controls.addStretch(1)

        # Right image views
        images = QVBoxLayout()
        
        # Source pane with label
        src_container = QWidget()
        src_layout = QVBoxLayout(src_container)
        src_layout.setContentsMargins(0, 0, 0, 0)
        self.source_label = QLabel("Source")
        self.source_label.setStyleSheet("font-weight: bold; color: #007AFF; padding: 4px;")
        src_layout.addWidget(self.source_label)
        self.src_view = ImageView(self)
        self.src_view.setStyleSheet("border: 2px solid #007AFF;")  # Active by default
        self.src_view.mousePressEvent = self._wrap_mouse_press(self.src_view, "source")
        src_layout.addWidget(self.src_view)
        images.addWidget(src_container, 3)  # Give source view more space
        
        # Selection preview (cropped region) container - initially hidden
        self.preview_container = QWidget()
        preview_layout = QVBoxLayout(self.preview_container)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        self.preview_label = QLabel("Crop preview")
        self.preview_label.setVisible(False)
        self.preview_label.setStyleSheet("font-weight: normal; color: #666; padding: 4px;")
        preview_layout.addWidget(self.preview_label)
        self.preview_view = ImageView(self)
        self.preview_view.setMinimumHeight(100)
        self.preview_view.setMaximumHeight(150)
        self.preview_view.toggle_selection_mode(False)  # Preview is view-only
        self.preview_view.setStyleSheet("background-color: white; border: 1px solid #ccc;")
        self.preview_view.setVisible(False)
        self.preview_view.mousePressEvent = self._wrap_mouse_press(self.preview_view, "preview")
        # Allow clicking empty space in container to activate pane
        self.preview_container.mousePressEvent = self._wrap_mouse_press(self.preview_container, "preview")
        preview_layout.addWidget(self.preview_view)
        self.preview_container.setVisible(False)
        images.addWidget(self.preview_container, 1)

        # Result pane with label
        result_container = QWidget()
        result_layout = QVBoxLayout(result_container)
        result_layout.setContentsMargins(0, 0, 0, 0)
        self.result_label = QLabel("Result")
        self.result_label.setVisible(False)
        self.result_label.setStyleSheet("font-weight: normal; color: #666; padding: 4px;")
        result_layout.addWidget(self.result_label)
        self.res_view = ImageView(self)
        self.res_view.setMinimumHeight(100)
        self.res_view.setMaximumHeight(200)
        self.res_view.mousePressEvent = self._wrap_mouse_press(self.res_view, "result")
        # Set white background for result view for better visibility
        self.res_view.setStyleSheet("background-color: white; border: 1px solid #ccc;")
        self.res_view.setVisible(False)
        result_layout.addWidget(self.res_view)
        images.addWidget(result_container, 1)

        root.addWidget(left_panel, 0)
        root.addLayout(images, 1)

        # Status bar at bottom
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Session ID label (permanent widget on right side of status bar)
        self.session_id_label = QLabel("No session")
        self.session_id_label.setStyleSheet("color: #666; padding: 2px 8px;")
        self.status_bar.addPermanentWidget(self.session_id_label)
        # State
        self._color_hex = "#000000"
        self._update_color_ui()
        self._last_result_png = None
        self._last_local_path = None
        self._current_image_data = None  # Store raw image data for rotate ops
        self._licensed = is_licensed()
        self._active_pane = "source"  # Track which pane user clicked: "source", "preview", "result"
        self._auto_threshold_enabled = False

        # Live preview timer
        self._preview_timer = QTimer(self)
        self._preview_timer.setSingleShot(True)
        self._preview_timer.timeout.connect(self.on_preview)

        # React to selection and slider changes
        self.src_view.selectionChanged.connect(self.on_selection_changed)
        self.threshold.valueChanged.connect(self.on_adjustment_changed)

        # Menu bar: License actions
        license_menu = self.menuBar().addMenu("License")
        self.enter_license_action = QAction("Enter License…", self)
        self.enter_license_action.triggered.connect(self.on_enter_license)
        license_menu.addAction(self.enter_license_action)

        self.buy_license_action = QAction("Buy License…", self)
        self.buy_license_action.triggered.connect(self.on_buy_license)
        license_menu.addAction(self.buy_license_action)

        # Initialize action states and library
        self._update_action_states()
        self._refresh_library_list()
        self._update_library_controls()
        self._update_pane_borders()  # Set initial active pane border

        # -------- Shortcuts --------
        # Standard keys map to Cmd on macOS and Ctrl on others
        QShortcut(QKeySequence.Open, self, activated=self.on_open)
        QShortcut(QKeySequence.Copy, self, activated=self.on_copy)
        QShortcut(QKeySequence.ZoomIn, self, activated=self._on_zoom_in)
        QShortcut(QKeySequence.ZoomOut, self, activated=self._on_zoom_out)
        # Reset to 100%
        QShortcut(QKeySequence("Ctrl+0"), self, activated=self._on_reset_zoom)
        QShortcut(QKeySequence("Meta+0"), self, activated=self._on_reset_zoom)
        # Fit to view
        QShortcut(QKeySequence("Ctrl+1"), self, activated=self._on_fit)
        QShortcut(QKeySequence("Meta+1"), self, activated=self._on_fit)
        # Export
        QShortcut(QKeySequence("Ctrl+E"), self, activated=self.on_export)
        QShortcut(QKeySequence("Meta+E"), self, activated=self.on_export)
        # Rotate
        QShortcut(QKeySequence("Ctrl+]"), self, activated=lambda: self.on_rotate(90))
        QShortcut(QKeySequence("Meta+]"), self, activated=lambda: self.on_rotate(90))
        QShortcut(QKeySequence("Ctrl+["), self, activated=lambda: self.on_rotate(-90))
        QShortcut(QKeySequence("Meta+["), self, activated=lambda: self.on_rotate(-90))

    # Optionally, add login action if backend requires it
    # login_action = QAction("Login", self)
    # login_action.triggered.connect(self.request_login)
    # self.menuBar().addAction(login_action)

    # def request_login(self):
    #     if self.session.access_token:
    #         QMessageBox.information(self, "Already logged in", f"User: {self.session.user_email}")
    #         return
    #     QMessageBox.information(self, "Login required", "Use the Login action or restart to open the login dialog.")

    def on_open(self):
        # If login is required, uncomment the following block:
        # if not self.session.access_token:
        #     QMessageBox.warning(self, "Not authenticated", "Please login first (Menu > Login)")
        #     return
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select image", filter="Images (*.png *.jpg *.jpeg)")
            if not file_path:
                return
            self._last_local_path = file_path
            
            # Store raw image data for rotate operations
            with open(file_path, "rb") as f:
                self._current_image_data = f.read()
            
            self.status_bar.showMessage("Uploading image...", 0)
            payload = self.api_client.upload_image(file_path)
            
            # Load image with EXIF orientation correction
            image = self._load_image_with_exif(file_path)
            if image.isNull():
                raise RuntimeError("Could not load selected image into viewer")
            self.src_view.set_image(image)
            self._on_pane_clicked("source")
            
            # Update session ID in status bar (no popup)
            session_id = payload.get('id')
            self.session.session_id = session_id
            self.session_id_label.setText(f"Session: {session_id[:8]}...")
            self.session_id_label.setToolTip(f"Full session ID: {session_id}")
            self.status_bar.showMessage("Image uploaded successfully", 3000)
            
            # Clear previous outputs
            self.preview_view.clear_image()
            self.res_view.scene().clear()
            self.export_btn.setEnabled(False)
            self.save_to_library_btn.setEnabled(False)
            # Hide preview/result panes until selection is made
            self.preview_label.setVisible(False)
            self.preview_view.setVisible(False)
            self.preview_container.setVisible(False)
            self.result_label.setVisible(False)
            self.res_view.setVisible(False)
            # Show a small crop preview when selection exists; processing is auto-triggered on selection
            self._update_action_states()
            self._update_view_actions_enabled()
        except KeyboardInterrupt:
            # User cancelled dialog or operation
            self.status_bar.showMessage("Upload cancelled", 2000)
            return
        except Exception as e:
            import traceback
            error_details = f"{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
            QMessageBox.critical(self, "Upload failed", error_details)
            self.status_bar.showMessage("Upload failed", 3000)

    def _load_image_with_exif(self, file_path: str) -> QImage:
        """Load image and apply EXIF orientation correction."""
        try:
            # Use PIL to read EXIF and rotate if needed
            pil_img = PILImage.open(file_path)
            
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
            
            # Convert PIL image to QImage
            pil_img = pil_img.convert("RGB")
            data = pil_img.tobytes("raw", "RGB")
            qimage = QImage(data, pil_img.width, pil_img.height, QImage.Format_RGB888)
            return qimage.copy()  # Make a deep copy
        except Exception as e:
            # Fallback to basic QImage loading if EXIF fails
            import logging
            logging.warning(f"EXIF orientation correction failed: {e}, using basic load")
            return QImage(file_path)

    def on_pick_color(self):
        color = QColorDialog.getColor(QColor("black"), self, "Pick color")
        if color.isValid():
            self._color_hex = color.name()  # #RRGGBB
            self._update_color_ui()
            self.schedule_preview()

    def on_preview(self):
        """Process the selected region and show the result."""
        if not self.session.session_id:
            QMessageBox.warning(self, "No image uploaded", "Please open & upload an image first")
            return
        # Selection
        x1, y1, x2, y2 = self.src_view.selected_rect_image_coords()
        
        # Debug logging
        print(f"[DEBUG] on_preview called")
        print(f"[DEBUG] Session ID: {self.session.session_id}")
        print(f"[DEBUG] Selection coords: ({x1}, {y1}) → ({x2}, {y2})")
        print(f"[DEBUG] Color: {self._color_hex}, Threshold: {self.threshold.value()}")
        
        if x1 == x2 or y1 == y2:
            QMessageBox.warning(self, "No region selected", "Drag on the source image to select a region")
            return
        
        # Validate coordinates
        if x1 >= x2 or y1 >= y2:
            print(f"[ERROR] Invalid selection coordinates: x1={x1} >= x2={x2} or y1={y1} >= y2={y2}")
            QMessageBox.warning(self, "Invalid selection", "Selection coordinates are invalid. Please try again.")
            return
        
        self.status_bar.showMessage("Processing...", 0)
        try:
            png_bytes = self.api_client.process_image(
                session_id=self.session.session_id,
                x1=x1, y1=y1, x2=x2, y2=y2,
                color=self._color_hex,
                threshold=int(self.threshold.value()),
            )
            print(f"[DEBUG] Received {len(png_bytes)} bytes from backend")
            self._last_result_png = png_bytes
            self.res_view.load_image_bytes(png_bytes)
            # Enable actions now that a preview exists
            self._update_action_states(preview_ready=True)
            self.status_bar.showMessage("Preview ready", 2000)
        except Exception as e:
            print(f"[ERROR] Processing failed: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Process failed", str(e))
            self.status_bar.showMessage("Processing failed", 3000)

    def on_clear_selection(self):
        self.src_view.clear_selection()
        self.sel_info.setText("Selection: –")
        self.preview_view.clear_image()
        self.export_btn.setEnabled(False)
        self.save_to_library_btn.setEnabled(False)
        # Hide preview/result panes
        self.preview_label.setVisible(False)
        self.preview_view.setVisible(False)
        self.preview_container.setVisible(False)
        self.result_label.setVisible(False)
        self.res_view.setVisible(False)
        self._update_view_actions_enabled()

    def on_selection_changed(self, _rect):
        # Update selection info and crop preview
        x1, y1, x2, y2 = self.src_view.selected_rect_image_coords()
        w, h = max(0, x2 - x1), max(0, y2 - y1)
        if w > 0 and h > 0:
            self.sel_info.setText(f"Selection: {w}×{h} at ({x1},{y1})")
            # Show preview/result panes now that we have a selection
            self.preview_label.setVisible(True)
            self.preview_view.setVisible(True)
            self.preview_container.setVisible(True)
            self.result_label.setVisible(True)
            self.res_view.setVisible(True)
            
            cropped = self.src_view.crop_selection()
            if cropped and not cropped.isNull():
                self.preview_view.set_image(cropped)
                self.preview_view.fit()
            else:
                self.preview_view.clear_image()
            if self._auto_threshold_enabled:
                if self._apply_auto_threshold():
                    self.schedule_preview()
                else:
                    self.schedule_preview()
            else:
                self.schedule_preview()
        else:
            self.sel_info.setText("Selection: –")
            self.preview_view.clear_image()
            self.save_to_library_btn.setEnabled(False)
            # Hide preview/result panes
            self.preview_label.setVisible(False)
            self.preview_view.setVisible(False)
            self.preview_container.setVisible(False)
            self.result_label.setVisible(False)
            self.res_view.setVisible(False)
        self._update_view_actions_enabled()

    def on_adjustment_changed(self, _value: int):
        # Debounce live preview when threshold changes
        self.schedule_preview()

    def schedule_preview(self):
        # Only schedule if we have a valid selection and an uploaded session
        if not self.session.session_id:
            return
        x1, y1, x2, y2 = self.src_view.selected_rect_image_coords()
        if x1 == x2 or y1 == y2:
            return
        # Debounce 200ms
        self._preview_timer.start(200)

    def _on_auto_threshold_toggled(self, state: int):
        enabled = bool(state)
        self._auto_threshold_enabled = enabled
        self.threshold.setDisabled(enabled)

        if enabled:
            applied = self._apply_auto_threshold()
            if applied:
                self.schedule_preview()
            else:
                self.status_bar.showMessage("Auto threshold needs a selection", 2000)
        else:
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
        if not buffer.open(QBuffer.WriteOnly):
            return None
        cropped.save(buffer, "PNG")
        data = bytes(buffer.data())
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
            self.toggle_mode_btn.setText("🎯 Mode: Select")
        else:
            self.toggle_mode_btn.setText("✋ Mode: Pan")

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
            file_path, _ = QFileDialog.getSaveFileName(self, "Export Metadata As", default_name, "JSON (*.json)")
            if not file_path:
                return
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2)
            self.status_bar.showMessage(f"Saved metadata: {file_path}", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Export JSON Failed", str(e))
    
    def on_save_to_library(self):
        """Quick save to library with default PNG format."""
        if not self._last_result_png:
            return
        self.status_bar.showMessage("Saving to library...", 0)
        try:
            saved_path = lib.save_png_to_library(self._last_result_png)
            self.status_bar.showMessage(f"Saved: {saved_path}", 4000)
            self._refresh_library_list()
        except Exception as e:
            QMessageBox.critical(self, "Save failed", str(e))
            self.status_bar.showMessage("Save failed", 3000)
    
    def _refresh_library_list(self):
        self.library_list.clear()
        for it in lib.list_items(limit=50):
            text = f"{it.display_name}  ·  {it.pretty_time}"
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, it.path)
            self.library_list.addItem(item)
        self._update_library_controls()

    def _update_library_controls(self):
        has_selection = bool(self.library_list.selectedItems())
        self.delete_from_library_btn.setEnabled(has_selection)

    def on_library_item_open(self, item: QListWidgetItem):
        path = item.data(Qt.UserRole)
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
            self._on_pane_clicked("source")
            # Upload to backend to establish a fresh session
            from tempfile import NamedTemporaryFile
            import os
            tmp = NamedTemporaryFile(suffix=".png", delete=False)
            tmp.write(data)
            tmp.flush()
            tmp.close()
            # Keep temp file path for rotate operations
            self._last_local_path = tmp.name
            self.status_bar.showMessage("Uploading to create session...", 0)
            payload = self.api_client.upload_image(tmp.name)
            session_id = payload.get('id')
            self.session.session_id = session_id
            self.session_id_label.setText(f"Session: {session_id[:8]}...")
            self.session_id_label.setToolTip(f"Full session ID: {session_id}")
            # Clear any previous result/preview; user can select and it will auto-preview
            self._last_result_png = None
            self.preview_view.clear_image()
            self.preview_view.setVisible(False)
            self.preview_label.setVisible(False)
            self.preview_container.setVisible(False)
            self.res_view.scene().clear()
            self.res_view.setVisible(False)
            self.result_label.setVisible(False)
            self._update_action_states(preview_ready=False)
            self._update_view_actions_enabled()
            self._update_library_controls()
            self.status_bar.showMessage(f"Loaded into Source from library", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Open failed", str(e))
            import traceback
            traceback.print_exc()

    def on_library_context_menu(self, pos: QPoint):
        item = self.library_list.itemAt(pos)
        if not item:
            return
        path = item.data(Qt.UserRole)
        menu = QMenu(self)
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
                QMessageBox.warning(self, "Delete failed", "Could not delete the selected file.")
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
            path = item.data(Qt.UserRole)
            if not path:
                continue
            if not lib.delete_item(path):
                failed.append(path)

        self._refresh_library_list()
        self._update_library_controls()

        if failed:
            formatted = "\n".join(failed)
            QMessageBox.warning(self, "Delete failed", f"Could not delete:\n{formatted}")
            return

        self.status_bar.showMessage("Deleted", 2000)

    def on_rotate(self, degrees: int):
        """Rotate the active pane. Source rotates image+session, others rotate display only."""
        active = self._active_pane

        if active == "source":
            if not self._current_image_data:
                QMessageBox.information(self, "No image", "Open an image first.")
                return
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

                self.status_bar.showMessage("Uploading rotated image...", 0)
                payload = self.api_client.upload_image(tmp.name)

                qimg = self._load_image_with_exif(tmp.name)
                self.src_view.set_image(qimg)
                session_id = payload.get('id')
                self.session.session_id = session_id
                self.session_id_label.setText(f"Session: {session_id[:8]}...")
                self.session_id_label.setToolTip(f"Full session ID: {session_id}")
                self.status_bar.showMessage("Rotated source & re-uploaded", 3000)

                # Reset previous outputs and CLEAR SELECTION (coordinates no longer valid)
                self._last_result_png = None
                self.preview_view.clear_image()
                self.preview_view.setVisible(False)
                self.preview_label.setVisible(False)
                self.preview_container.setVisible(False)
                self.res_view.scene().clear()
                self.res_view.setVisible(False)
                self.result_label.setVisible(False)
                self.src_view.clear_selection()
                self.sel_info.setText("Selection: –")
                self._update_action_states()
                self.status_bar.showMessage("Rotated - please make a new selection", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Rotate failed", str(e))
                import traceback
                traceback.print_exc()
                self.status_bar.showMessage("Rotate failed", 3000)
            finally:
                self._update_view_actions_enabled()
            return

        # Preview pane rotation (display only)
        if active == "preview":
            if not self.preview_view.has_image():
                QMessageBox.information(self, "No preview", "Make a selection first to rotate the preview.")
                return
            self.preview_view.rotate_view(-degrees)
            self.status_bar.showMessage("Rotated preview view", 2000)
            self._update_view_actions_enabled()
            return

        # Result pane rotation (display only)
        if active == "result":
            if not self.res_view.has_image():
                QMessageBox.information(self, "No result", "Process a selection before rotating the result view.")
                return
            self.res_view.rotate_view(-degrees)
            self.status_bar.showMessage("Rotated result view", 2000)
            self._update_view_actions_enabled()
            return

    def _apply_theme(self):
        """Apply subtle blue accent color theme for personality."""
        import sys
        if sys.platform == 'darwin':
            # Prefer native macOS look; keep styling minimal
            self.setStyleSheet("")
        else:
            # Accent color: #007AFF (iOS blue)
            style = """
                QWidget { background-color: #f7f7f7; color: #222222; }
                QPushButton { background-color: #ffffff; border: 1px solid #d0d0d0; border-radius: 4px; padding: 6px 12px; font-size: 13px; color: #222222; }
                QPushButton:hover { background-color: #e0e0e0; border-color: #007AFF; }
                QPushButton:pressed { background-color: #d0d0d0; }
                QPushButton:disabled { background-color: #f8f8f8; color: #888888; }
                QLabel { font-size: 13px; color: #222222; }
                QSlider::groove:horizontal { border: 1px solid #d0d0d0; height: 6px; background: #f0f0f0; border-radius: 3px; }
                QSlider::handle:horizontal { background: #007AFF; border: 1px solid #0051d5; width: 16px; margin: -6px 0; border-radius: 8px; }
                QSlider::handle:horizontal:hover { background: #0051d5; }
            """
            self.setStyleSheet(style)

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
        self.color_label.setStyleSheet(f"background-color: {hexc}; color: {text_color}; border: 1px solid #ccc; padding: 4px 8px; border-radius: 4px;")

    # -------- License/Evaluation helpers --------
    def _update_action_states(self, preview_ready: bool = False):
        """Enable or disable actions based on whether a processed preview exists."""
        has_preview = bool(preview_ready or self._last_result_png)
        self.export_btn.setEnabled(has_preview)
        self.export_json_btn.setEnabled(True)  # Allow exporting metadata even without preview
        self.save_to_library_btn.setEnabled(has_preview)
        self.copy_btn.setEnabled(has_preview)
        self._update_view_actions_enabled()

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

        rotate_enabled = False
        if self._active_pane == "source":
            rotate_enabled = self._current_image_data is not None
        elif self._active_pane == "preview":
            rotate_enabled = has_preview
        elif self._active_pane == "result":
            rotate_enabled = has_result

        self.rotate_cw_btn.setEnabled(rotate_enabled)
        self.rotate_ccw_btn.setEnabled(rotate_enabled)

    def on_copy(self):
        if not self._last_result_png:
            return
        try:
            img = QImage.fromData(self._last_result_png, "PNG")
            if img.isNull():
                raise RuntimeError("Could not decode result image for clipboard")
            QApplication.clipboard().setPixmap(QPixmap.fromImage(img))
            self.status_bar.showMessage("Copied to clipboard", 2000)
        except Exception as e:
            QMessageBox.critical(self, "Copy Failed", str(e))

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

    # -------- Click-to-focus pane system --------
    def _wrap_mouse_press(self, view, pane_name):
        """Wrap mousePressEvent to detect pane clicks and call original handler."""
        original_handler = view.mousePressEvent
        def wrapped(event):
            self._on_pane_clicked(pane_name)
            original_handler(event)
        return wrapped
    
    def _on_pane_clicked(self, pane: str):
        """User clicked a pane - make it active."""
        if self._active_pane != pane:
            self._active_pane = pane
            self._update_pane_borders()
            self._update_view_actions_enabled()
            self.status_bar.showMessage(f"Active pane: {pane.capitalize()}", 2000)
            print(f"[UI] Active pane changed to: {pane}")
    
    def _update_pane_borders(self):
        """Update visual borders to show which pane is active."""
        # Source pane
        if self._active_pane == "source":
            self.src_view.setStyleSheet("border: 2px solid #007AFF;")
            self.source_label.setStyleSheet("font-weight: bold; color: #007AFF; padding: 4px;")
        else:
            self.src_view.setStyleSheet("border: 1px solid #ccc;")
            self.source_label.setStyleSheet("font-weight: normal; color: #666; padding: 4px;")
        
        # Preview pane
        if self._active_pane == "preview":
            self.preview_view.setStyleSheet("background-color: white; border: 2px solid #007AFF;")
            self.preview_label.setStyleSheet("font-weight: bold; color: #007AFF; padding: 4px;")
        else:
            self.preview_view.setStyleSheet("background-color: white; border: 1px solid #ccc;")
            self.preview_label.setStyleSheet("font-weight: normal; color: #666; padding: 4px;")

        # Result pane
        if self._active_pane == "result":
            self.res_view.setStyleSheet("background-color: white; border: 2px solid #007AFF;")
            self.result_label.setStyleSheet("font-weight: bold; color: #007AFF; padding: 4px;")
        else:
            self.res_view.setStyleSheet("background-color: white; border: 1px solid #ccc;")
            self.result_label.setStyleSheet("font-weight: normal; color: #666; padding: 4px;")
    
    def _on_zoom_in(self):
        """Zoom in on active pane."""
        if self._active_pane == "source":
            self.src_view.zoom_in()
        elif self._active_pane == "preview":
            self.preview_view.zoom_in()
        elif self._active_pane == "result":
            self.res_view.zoom_in()
    
    def _on_zoom_out(self):
        """Zoom out on active pane."""
        if self._active_pane == "source":
            self.src_view.zoom_out()
        elif self._active_pane == "preview":
            self.preview_view.zoom_out()
        elif self._active_pane == "result":
            self.res_view.zoom_out()
    
    def _on_reset_zoom(self):
        """Reset zoom to 100% on active pane."""
        if self._active_pane == "source":
            self.src_view.reset_zoom()
        elif self._active_pane == "preview":
            self.preview_view.reset_zoom()
        elif self._active_pane == "result":
            self.res_view.reset_zoom()
    
    def _on_fit(self):
        """Fit to window on active pane."""
        if self._active_pane == "source":
            self.src_view.fit()
        elif self._active_pane == "preview":
            self.preview_view.fit()
        elif self._active_pane == "result":
            self.res_view.fit()

