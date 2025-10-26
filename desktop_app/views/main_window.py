from __future__ import annotations

import io
from typing import Optional
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QImage, QColor, QPixmap, QTransform
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QLabel, QSlider, QColorDialog, QMessageBox, QListWidget, QListWidgetItem, QStatusBar
)
from PIL import Image as PILImage
from PIL.ExifTags import TAGS

from desktop_app.api.client import ApiClient
from desktop_app.state.session import SessionState
from desktop_app.widgets.image_view import ImageView
from desktop_app.views.export_dialog import ExportDialog
from desktop_app.resources.icons import set_button_icon, get_icon


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

        # Left controls
        controls = QVBoxLayout()
        self.open_btn = QPushButton()
        set_button_icon(self.open_btn, 'open', 'Open & Upload Image')
        self.open_btn.clicked.connect(self.on_open)
        controls.addWidget(self.open_btn)

        controls.addWidget(QLabel("Threshold"))
        self.threshold = QSlider(Qt.Horizontal)
        self.threshold.setRange(0, 255)
        self.threshold.setValue(200)
        controls.addWidget(self.threshold)

        self.color_label = QLabel("Color: #000000")
        self.pick_color_btn = QPushButton()
        set_button_icon(self.pick_color_btn, 'color', 'Pick Color')
        self.pick_color_btn.clicked.connect(self.on_pick_color)
        controls.addWidget(self.color_label)
        controls.addWidget(self.pick_color_btn)

        # Zoom & reset controls
        zoom_row = QHBoxLayout()
        self.zoom_in_btn = QPushButton()
        self.zoom_out_btn = QPushButton()
        self.fit_btn = QPushButton()
        self.reset_view_btn = QPushButton()
        self.toggle_mode_btn = QPushButton()
        self.clear_sel_btn = QPushButton()
        
        set_button_icon(self.zoom_in_btn, 'zoom_in', None)  # Emoji only
        set_button_icon(self.zoom_out_btn, 'zoom_out', None)
        set_button_icon(self.fit_btn, 'fit', 'Fit')
        set_button_icon(self.reset_view_btn, 'reset', '100%')
        set_button_icon(self.toggle_mode_btn, 'select', 'Mode: Select')
        set_button_icon(self.clear_sel_btn, 'clear', 'Clear Selection')
        
        self.zoom_in_btn.clicked.connect(lambda: self.src_view.zoom_in())
        self.zoom_out_btn.clicked.connect(lambda: self.src_view.zoom_out())
        self.fit_btn.clicked.connect(lambda: self.src_view.fit())
        self.reset_view_btn.clicked.connect(lambda: self.src_view.reset_zoom())
        self.toggle_mode_btn.clicked.connect(self.on_toggle_mode)
        self.clear_sel_btn.clicked.connect(self.on_clear_selection)
        for w in (self.zoom_in_btn, self.zoom_out_btn, self.fit_btn, self.reset_view_btn):
            zoom_row.addWidget(w)
        controls.addLayout(zoom_row)
        controls.addWidget(self.toggle_mode_btn)
        controls.addWidget(self.clear_sel_btn)

        # Selection info
        self.sel_info = QLabel("Selection: –")
        controls.addWidget(self.sel_info)

        self.preview_btn = QPushButton()
        set_button_icon(self.preview_btn, 'preview', 'Preview')
        self.preview_btn.setToolTip("Process the selected region with current threshold and color settings")
        self.preview_btn.clicked.connect(self.on_preview)
        
        self.export_btn = QPushButton()
        set_button_icon(self.export_btn, 'export', 'Export...')
        self.export_btn.setToolTip("Export with advanced options (background, trim, format)")
        self.export_btn.clicked.connect(self.on_export)
        self.export_btn.setEnabled(False)
        
        self.save_to_library_btn = QPushButton()
        set_button_icon(self.save_to_library_btn, 'save', 'Save to Library')
        self.save_to_library_btn.setToolTip("Quick save as PNG to local library")
        self.save_to_library_btn.clicked.connect(self.on_save_to_library)
        self.save_to_library_btn.setEnabled(False)
        
        controls.addWidget(self.preview_btn)
        controls.addWidget(self.export_btn)
        controls.addWidget(self.save_to_library_btn)

        # Library list
        controls.addWidget(QLabel("My Signatures"))
        self.library_list = QListWidget()
        self.library_list.itemClicked.connect(self.on_library_item_clicked)
        self.library_list.setMinimumHeight(120)
        controls.addWidget(self.library_list)
        controls.addStretch(1)

        # Right image views
        images = QVBoxLayout()
        images.addWidget(QLabel("Source"))
        self.src_view = ImageView(self)
        images.addWidget(self.src_view, 3)  # Give source view more space
        
        # Selection preview (cropped region only) - initially hidden
        self.crop_preview_label = QLabel("Crop preview")
        self.crop_preview_label.setVisible(False)
        self.crop_preview = QLabel()
        self.crop_preview.setMinimumHeight(100)
        self.crop_preview.setMaximumHeight(150)
        self.crop_preview.setAlignment(Qt.AlignCenter)
        self.crop_preview.setStyleSheet("background-color: white; border: 1px solid #ccc;")
        self.crop_preview.setVisible(False)
        images.addWidget(self.crop_preview_label)
        images.addWidget(self.crop_preview, 1)

        self.result_label = QLabel("Result")
        self.result_label.setVisible(False)
        self.res_view = ImageView(self)
        self.res_view.setMinimumHeight(100)
        self.res_view.setMaximumHeight(200)
        # Set white background for result view for better visibility
        self.res_view.setStyleSheet("background-color: white;")
        self.res_view.setVisible(False)
        images.addWidget(self.result_label)
        images.addWidget(self.res_view, 1)

        root.addLayout(controls, 0)
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
        self._last_result_png = None
        self._last_local_path = None

        # Live preview timer
        self._preview_timer = QTimer(self)
        self._preview_timer.setSingleShot(True)
        self._preview_timer.timeout.connect(self.on_preview)

        # React to selection and slider changes
        self.src_view.selectionChanged.connect(self.on_selection_changed)
        self.threshold.valueChanged.connect(self.on_adjustment_changed)

        # Menu minimal action

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
            
            self.status_bar.showMessage("Uploading image...", 0)
            payload = self.api_client.upload_image(file_path)
            
            # Load image with EXIF orientation correction
            image = self._load_image_with_exif(file_path)
            if image.isNull():
                raise RuntimeError("Could not load selected image into viewer")
            self.src_view.set_image(image)
            
            # Update session ID in status bar (no popup)
            session_id = payload.get('id')
            self.session.session_id = session_id
            self.session_id_label.setText(f"Session: {session_id[:8]}...")
            self.session_id_label.setToolTip(f"Full session ID: {session_id}")
            self.status_bar.showMessage("Image uploaded successfully", 3000)
            
            # Clear previous outputs
            self.crop_preview.clear()
            self.res_view.scene().clear()
            self.export_btn.setEnabled(False)
            self.save_to_library_btn.setEnabled(False)
            # Hide preview/result panes until selection is made
            self.crop_preview_label.setVisible(False)
            self.crop_preview.setVisible(False)
            self.result_label.setVisible(False)
            self.res_view.setVisible(False)
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
            self.color_label.setText(f"Color: {self._color_hex}")
            self.schedule_preview()

    def on_preview(self):
        """Process the selected region and show the result."""
        if not self.session.session_id:
            QMessageBox.warning(self, "No image uploaded", "Please open & upload an image first")
            return
        # Selection
        x1, y1, x2, y2 = self.src_view.selected_rect_image_coords()
        if x1 == x2 or y1 == y2:
            QMessageBox.warning(self, "No region selected", "Drag on the source image to select a region")
            return
        
        self.status_bar.showMessage("Processing...", 0)
        try:
            png_bytes = self.api_client.process_image(
                session_id=self.session.session_id,
                x1=x1, y1=y1, x2=x2, y2=y2,
                color=self._color_hex,
                threshold=int(self.threshold.value()),
            )
            self._last_result_png = png_bytes
            self.res_view.load_image_bytes(png_bytes)
            self.export_btn.setEnabled(True)
            self.save_to_library_btn.setEnabled(True)
            self.status_bar.showMessage("Preview ready", 2000)
        except Exception as e:
            QMessageBox.critical(self, "Process failed", str(e))
            self.status_bar.showMessage("Processing failed", 3000)

    def on_clear_selection(self):
        self.src_view.clear_selection()
        self.sel_info.setText("Selection: –")
        self.crop_preview.clear()
        self.export_btn.setEnabled(False)
        self.save_to_library_btn.setEnabled(False)
        # Hide preview/result panes
        self.crop_preview_label.setVisible(False)
        self.crop_preview.setVisible(False)
        self.result_label.setVisible(False)
        self.res_view.setVisible(False)

    def on_selection_changed(self, _rect):
        # Update selection info and crop preview
        x1, y1, x2, y2 = self.src_view.selected_rect_image_coords()
        w, h = max(0, x2 - x1), max(0, y2 - y1)
        if w > 0 and h > 0:
            self.sel_info.setText(f"Selection: {w}×{h} at ({x1},{y1})")
            # Show preview/result panes now that we have a selection
            self.crop_preview_label.setVisible(True)
            self.crop_preview.setVisible(True)
            self.result_label.setVisible(True)
            self.res_view.setVisible(True)
            
            cropped = self.src_view.crop_selection()
            if cropped and not cropped.isNull():
                # Scale preview to fit label
                pm = QPixmap.fromImage(cropped)
                pm = pm.scaled(self.crop_preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.crop_preview.setPixmap(pm)
            self.schedule_preview()
        else:
            self.sel_info.setText("Selection: –")
            self.crop_preview.clear()
            self.save_btn.setEnabled(False)
            # Hide preview/result panes
            self.crop_preview_label.setVisible(False)
            self.crop_preview.setVisible(False)
            self.result_label.setVisible(False)
            self.res_view.setVisible(False)

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

    def on_toggle_mode(self):
        """Toggle between selection mode and pan mode."""
        current_mode = self.src_view._selection_mode
        new_mode = not current_mode
        self.src_view.toggle_selection_mode(new_mode)
        if new_mode:
            set_button_icon(self.toggle_mode_btn, 'select', 'Mode: Select')
        else:
            # Use different emoji for pan mode (hand)
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
    
    def on_save_to_library(self):
        """Quick save to library with default PNG format."""
        if not self._last_result_png:
            return
        
        # TODO: Implement library directory and auto-naming
        # For now, use a simple save dialog with PNG default
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"signature_{timestamp}.png"
        
        self.status_bar.showMessage("Saving to library...", 0)
        out_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save to Library", 
            default_name,
            "PNG Image (*.png)"
        )
        if not out_path:
            self.status_bar.showMessage("Save cancelled", 2000)
            return
        
        try:
            with open(out_path, "wb") as f:
                f.write(self._last_result_png)
            self.status_bar.showMessage(f"Saved: {out_path}", 4000)
            # TODO: Add to library list widget
        except Exception as e:
            QMessageBox.critical(self, "Save failed", str(e))
            self.status_bar.showMessage("Save failed", 3000)
    
    def on_library_item_clicked(self, item):
        """Load a signature from the library."""
        # TODO: Implement library item loading
        pass

    def _apply_theme(self):
        """Apply subtle blue accent color theme for personality."""
        # Accent color: #007AFF (iOS blue)
        style = """
            QWidget {
                background-color: #f7f7f7;
                color: #222222;
            }
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 13px;
                color: #222222;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border-color: #007AFF;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
            QPushButton:disabled {
                background-color: #f8f8f8;
                color: #888888;
            }
            QLabel {
                font-size: 13px;
                color: #222222;
            }
            QSlider::groove:horizontal {
                border: 1px solid #d0d0d0;
                height: 6px;
                background: #f0f0f0;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #007AFF;
                border: 1px solid #0051d5;
                width: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #0051d5;
            }
        """
        self.setStyleSheet(style)
