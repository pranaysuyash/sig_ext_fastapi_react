from __future__ import annotations

import io
from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QImage, QColor
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QLabel, QSlider, QColorDialog, QMessageBox
)

from desktop_app.widgets.image_view import ImageView


class MainWindow(QMainWindow):
    def __init__(self, api_client, session_state, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.session = session_state

        self.setWindowTitle("Signature Extractor (Desktop)")

        # Central UI
        central = QWidget(self)
        self.setCentralWidget(central)
        root = QHBoxLayout(central)

        # Left controls
        controls = QVBoxLayout()
        self.open_btn = QPushButton("Open & Upload Image")
        self.open_btn.clicked.connect(self.on_open)
        controls.addWidget(self.open_btn)

        controls.addWidget(QLabel("Threshold"))
        self.threshold = QSlider(Qt.Horizontal)
        self.threshold.setRange(0, 255)
        self.threshold.setValue(200)
        controls.addWidget(self.threshold)

        self.color_label = QLabel("Color: #000000")
        self.pick_color_btn = QPushButton("Pick Color")
        self.pick_color_btn.clicked.connect(self.on_pick_color)
        controls.addWidget(self.color_label)
        controls.addWidget(self.pick_color_btn)

        self.preview_btn = QPushButton("Preview")
        self.preview_btn.clicked.connect(self.on_preview)
        self.save_btn = QPushButton("Save Result")
        self.save_btn.clicked.connect(self.on_save)
        self.save_btn.setEnabled(False)
        controls.addWidget(self.preview_btn)
        controls.addWidget(self.save_btn)
        controls.addStretch(1)

        # Right image views
        images = QVBoxLayout()
        images.addWidget(QLabel("Source"))
        self.src_view = ImageView(self)
        images.addWidget(self.src_view)
        images.addWidget(QLabel("Result"))
        self.res_view = ImageView(self)
        images.addWidget(self.res_view)

        root.addLayout(controls, 0)
        root.addLayout(images, 1)

        # State
        self._color_hex = "#000000"
        self._last_result_png: Optional[bytes] = None
        self._last_local_path: Optional[str] = None

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
        file_path, _ = QFileDialog.getOpenFileName(self, "Select image", filter="Images (*.png *.jpg *.jpeg)")
        if not file_path:
            return
        self._last_local_path = file_path
        try:
            payload = self.api_client.upload_image(file_path)
            # Show local image as source
            image = QImage(file_path)
            if image.isNull():
                raise RuntimeError("Could not load selected image into viewer")
            self.src_view.set_image(image)
            QMessageBox.information(self, "Uploaded", f"Session ID: {payload.get('id')}")
        except Exception as e:
            QMessageBox.critical(self, "Upload failed", str(e))

    def on_pick_color(self):
        color = QColorDialog.getColor(QColor("black"), self, "Pick color")
        if color.isValid():
            self._color_hex = color.name()  # #RRGGBB
            self.color_label.setText(f"Color: {self._color_hex}")

    def on_preview(self):
        if not self.session.session_id:
            QMessageBox.warning(self, "No image uploaded", "Please open & upload an image first")
            return
        # Selection
        x1, y1, x2, y2 = self.src_view.selected_rect_image_coords()
        if x1 == x2 or y1 == y2:
            QMessageBox.warning(self, "No region selected", "Drag on the source image to select a region")
            return
        try:
            png_bytes = self.api_client.process_image(
                session_id=self.session.session_id,
                x1=x1, y1=y1, x2=x2, y2=y2,
                color=self._color_hex,
                threshold=int(self.threshold.value()),
            )
            self._last_result_png = png_bytes
            self.res_view.load_image_bytes(png_bytes)
            self.save_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Process failed", str(e))

    def on_save(self):
        if not self._last_result_png:
            return
        out_path, _ = QFileDialog.getSaveFileName(self, "Save result", filter="PNG Image (*.png)")
        if not out_path:
            return
        try:
            with open(out_path, "wb") as f:
                f.write(self._last_result_png)
            QMessageBox.information(self, "Saved", f"Saved to {out_path}")
        except Exception as e:
            QMessageBox.critical(self, "Save failed", str(e))
