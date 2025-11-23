import logging
import json
from datetime import datetime
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
    QPushButton, QFileDialog, QSizePolicy
)
from PySide6.QtCore import Qt, QMimeData, QSize
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QPixmap, QImage

from desktop_app.resources.icons import get_icon, set_button_icon
from desktop_app.processing.watermark import WatermarkEngine

LOG = logging.getLogger(__name__)

class VerifyDialog(QDialog):
    """Dialog to verify the invisible watermark in a signature image."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Verify Signature Authenticity")
        self.resize(500, 400)
        self.watermarker = WatermarkEngine()
        
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Header
        header = QLabel("Forensic Verification")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: palette(text);")
        layout.addWidget(header)
        
        desc = QLabel("Drop a signature image here to verify its origin and integrity.")
        desc.setStyleSheet("color: palette(text); opacity: 0.7;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Drop Zone
        self.drop_zone = QLabel()
        self.drop_zone.setFixedSize(450, 200)
        self.drop_zone.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_zone.setStyleSheet("""
            QLabel {
                border: 2px dashed #555;
                border-radius: 12px;
                background-color: rgba(0, 0, 0, 0.1);
                color: #888;
                font-size: 14px;
            }
            QLabel:hover {
                border-color: #007aff;
                background-color: rgba(0, 122, 255, 0.05);
                color: #007aff;
            }
        """)
        self.drop_zone.setText("Drop PNG here\nor click to browse")
        self.drop_zone.setAcceptDrops(True)
        # Override events
        self.drop_zone.dragEnterEvent = self._drag_enter_event
        self.drop_zone.dropEvent = self._drop_event
        self.drop_zone.mousePressEvent = self._browse_file
        layout.addWidget(self.drop_zone)
        
        # Result Area
        self.result_frame = QFrame()
        self.result_frame.setVisible(False)
        self.result_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 8px; padding: 12px;")
        res_layout = QVBoxLayout(self.result_frame)
        
        self.status_label = QLabel()
        self.status_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        res_layout.addWidget(self.status_label)
        
        self.details_label = QLabel()
        self.details_label.setStyleSheet("font-family: monospace; color: #ccc;")
        res_layout.addWidget(self.details_label)
        
        layout.addWidget(self.result_frame)
        layout.addStretch()
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        close_btn.setFixedWidth(100)
        layout.addWidget(close_btn, 0, Qt.AlignmentFlag.AlignRight)
        
    def _drag_enter_event(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def _drop_event(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            self._verify_file(path)
            
    def _browse_file(self, event):
        path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "PNG Images (*.png)")
        if path:
            self._verify_file(path)
            
    def _verify_file(self, path: str):
        try:
            with open(path, "rb") as f:
                data = f.read()
                
            meta = self.watermarker.verify_watermark(data)
            
            self.result_frame.setVisible(True)
            if meta:
                self.status_label.setText("✅ Authenticated by SignKit")
                self.status_label.setStyleSheet("color: #00cc00; font-weight: bold; font-size: 14px;")
                
                # Format details
                ts = meta.get('timestamp', 0)
                date_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                
                details = (
                    f"App: {meta.get('app', 'Unknown')}\n"
                    f"Version: {meta.get('version', 'Unknown')}\n"
                    f"Date: {date_str}\n"
                    f"Mode: {meta.get('mode', 'Unknown')}\n"
                    f"Source Hash: {meta.get('source_hash', 'Unknown')[:8]}..."
                )
                self.details_label.setText(details)
            else:
                self.status_label.setText("❌ No Watermark Found")
                self.status_label.setStyleSheet("color: #ff3b30; font-weight: bold; font-size: 14px;")
                self.details_label.setText("This image does not contain a valid SignKit forensic watermark.")
                
        except Exception as e:
            LOG.error(f"Verification error: {e}")
            self.result_frame.setVisible(True)
            self.status_label.setText("⚠️ Error")
            self.details_label.setText(f"Could not process file: {e}")
