import logging
import os
from typing import Optional, List, Dict, Any
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFileDialog, QFrame, QSizePolicy, QMessageBox,
    QToolBar, QSpinBox
)
from PySide6.QtCore import Qt, QMimeData, QPoint, QSize, QByteArray, QBuffer, QIODevice
from PySide6.QtGui import QPixmap, QImage, QDrag, QPainter, QAction, QIcon, QMouseEvent, QResizeEvent

from desktop_app.processing.pdf_engine import PdfEngine
from desktop_app.resources.icons import get_icon, set_button_icon

LOG = logging.getLogger(__name__)

class DraggableSignature(QLabel):
    """A draggable, resizable signature overlay widget."""
    
    def __init__(self, pixmap: QPixmap, parent: QWidget):
        super().__init__(parent)
        self.setPixmap(pixmap)
        self.setScaledContents(True)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.show()
        
        self.original_pixmap = pixmap
        self.is_dragging = False
        self.drag_start_pos = QPoint()
        
        # Resize handle
        self.setMouseTracking(True)
        self.resize_margin = 10
        self.is_resizing = False
        
        # Initial size
        self.resize(200, 100) # Default size
        
        # Style
        self.setStyleSheet("border: 1px dashed #007bff; background-color: transparent;")

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self._is_on_resize_handle(event.pos()):
                self.is_resizing = True
            else:
                self.is_dragging = True
            self.drag_start_pos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        # Cursor update
        if self._is_on_resize_handle(event.pos()):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.SizeAllCursor)
            
        if self.is_dragging:
            # Move widget
            delta = event.pos() - self.drag_start_pos
            self.move(self.pos() + delta)
        elif self.is_resizing:
            # Resize widget
            delta = event.pos() - self.drag_start_pos
            new_size = self.size() + QSize(delta.x(), delta.y())
            if new_size.width() > 20 and new_size.height() > 20:
                self.resize(new_size)
                self.drag_start_pos = event.pos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.is_dragging = False
        self.is_resizing = False

    def _is_on_resize_handle(self, pos: QPoint) -> bool:
        return (pos.x() > self.width() - self.resize_margin and 
                pos.y() > self.height() - self.resize_margin)
                
    def get_image_bytes(self) -> bytes:
        """Return the original image bytes (PNG)."""
        ba = QByteArray()
        buff = QBuffer(ba)
        buff.open(QIODevice.OpenModeFlag.WriteOnly)
        self.original_pixmap.save(buff, "PNG")
        return ba.data()

class PdfTab(QWidget):
    """Tab for viewing and signing PDFs."""
    
    def __init__(self):
        super().__init__()
        self.engine = PdfEngine()
        self.current_page_idx = 0
        self.total_pages = 0
        self.scale = 1.0
        self.signatures: List[DraggableSignature] = []
        
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # --- Toolbar ---
        toolbar = QFrame()
        toolbar.setStyleSheet("background-color: palette(window); border-bottom: 1px solid palette(mid);")
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(8, 4, 8, 4)
        
        self.open_btn = QPushButton("Open PDF")
        set_button_icon(self.open_btn, "folder_open", "Open", use_emoji=False)
        self.open_btn.clicked.connect(self.open_pdf)
        tb_layout.addWidget(self.open_btn)
        
        self.save_btn = QPushButton("Save Signed PDF")
        set_button_icon(self.save_btn, "save", "Save", use_emoji=False)
        self.save_btn.clicked.connect(self.save_pdf)
        self.save_btn.setEnabled(False)
        tb_layout.addWidget(self.save_btn)
        
        tb_layout.addStretch()
        
        # Page Navigation
        self.prev_btn = QPushButton("◀")
        self.prev_btn.setFixedSize(30, 30)
        self.prev_btn.clicked.connect(self.prev_page)
        self.prev_btn.setEnabled(False)
        tb_layout.addWidget(self.prev_btn)
        
        self.page_label = QLabel("Page 0/0")
        tb_layout.addWidget(self.page_label)
        
        self.next_btn = QPushButton("▶")
        self.next_btn.setFixedSize(30, 30)
        self.next_btn.clicked.connect(self.next_page)
        self.next_btn.setEnabled(False)
        tb_layout.addWidget(self.next_btn)
        
        layout.addWidget(toolbar)
        
        # --- PDF Viewer Area ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setStyleSheet("background-color: #555;") # Dark background for document contrast
        
        # Container for the page image + overlays
        self.page_container = QLabel()
        self.page_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_container.setAcceptDrops(True)
        # We need to override dragEnter/drop events on the container
        self.page_container.dragEnterEvent = self._drag_enter_event
        self.page_container.dropEvent = self._drop_event
        
        self.scroll_area.setWidget(self.page_container)
        layout.addWidget(self.scroll_area)
        
    def open_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if path:
            try:
                self.total_pages = self.engine.load_pdf(path)
                self.current_page_idx = 0
                self._update_page_display()
                self.save_btn.setEnabled(True)
                self._update_nav_buttons()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open PDF: {e}")

    def _update_page_display(self):
        if self.total_pages == 0:
            return
            
        try:
            # Clear existing signatures on page change (in a real app, we'd store them per page)
            # For MVP, we warn or just clear. Let's clear for now.
            for sig in self.signatures:
                sig.close()
            self.signatures.clear()
            
            pil_image = self.engine.render_page(self.current_page_idx, scale=1.5) # Render at 1.5x for quality
            
            # Convert PIL to QPixmap
            im_data = pil_image.convert("RGBA").tobytes("raw", "RGBA")
            qim = QImage(im_data, pil_image.width, pil_image.height, QImage.Format.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qim)
            
            self.page_container.setPixmap(pixmap)
            self.page_container.setFixedSize(pixmap.size())
            
            self.page_label.setText(f"Page {self.current_page_idx + 1}/{self.total_pages}")
            
        except Exception as e:
            LOG.error(f"Page render error: {e}")

    def _update_nav_buttons(self):
        self.prev_btn.setEnabled(self.current_page_idx > 0)
        self.next_btn.setEnabled(self.current_page_idx < self.total_pages - 1)

    def prev_page(self):
        if self.current_page_idx > 0:
            self.current_page_idx -= 1
            self._update_page_display()
            self._update_nav_buttons()

    def next_page(self):
        if self.current_page_idx < self.total_pages - 1:
            self.current_page_idx += 1
            self._update_page_display()
            self._update_nav_buttons()

    # --- Drag & Drop Support ---
    def _drag_enter_event(self, event):
        if event.mimeData().hasImage() or event.mimeData().hasUrls():
            event.acceptProposedAction()

    def _drop_event(self, event):
        pos = event.pos()
        
        pixmap = None
        if event.mimeData().hasImage():
            img = QImage(event.mimeData().imageData())
            pixmap = QPixmap.fromImage(img)
        elif event.mimeData().hasUrls():
            # Handle file drop (if it's an image)
            url = event.mimeData().urls()[0]
            if url.isLocalFile():
                pixmap = QPixmap(url.toLocalFile())
                
        if pixmap and not pixmap.isNull():
            sig_widget = DraggableSignature(pixmap, self.page_container)
            # Center on drop pos
            sig_widget.move(pos - QPoint(sig_widget.width() // 2, sig_widget.height() // 2))
            sig_widget.show()
            self.signatures.append(sig_widget)
            event.acceptProposedAction()

    def save_pdf(self):
        if not self.engine.pdf_path:
            return
            
        out_path, _ = QFileDialog.getSaveFileName(self, "Save Signed PDF", "", "PDF Files (*.pdf)")
        if not out_path:
            return
            
        try:
            # Collect signatures
            sig_data = []
            page_height = self.page_container.height()
            
            # We rendered at 1.5x scale (see _update_page_display)
            # We need to convert UI coordinates back to PDF points (1/72 inch)
            # pypdfium2 default render is 72 DPI * scale.
            # So UI pixels = PDF points * 1.5
            scale_factor = 1.5
            
            for sig in self.signatures:
                # Get geometry relative to page container
                x_ui = sig.x()
                y_ui = sig.y()
                w_ui = sig.width()
                h_ui = sig.height()
                
                # Convert to PDF points
                x_pdf = x_ui / scale_factor
                y_pdf = y_ui / scale_factor
                w_pdf = w_ui / scale_factor
                h_pdf = h_ui / scale_factor
                
                sig_data.append({
                    "page_index": self.current_page_idx,
                    "x": x_pdf,
                    "y": y_pdf,
                    "width": w_pdf,
                    "height": h_pdf,
                    "image_bytes": sig.get_image_bytes()
                })
                
            self.engine.save_signed_pdf(out_path, sig_data)
            QMessageBox.information(self, "Success", f"Signed PDF saved to:\n{out_path}")
            
        except Exception as e:
            LOG.error(f"Save error: {e}")
            QMessageBox.critical(self, "Save Error", f"Failed to save PDF: {e}")
