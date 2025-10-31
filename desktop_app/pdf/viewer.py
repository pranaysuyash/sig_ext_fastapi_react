"""PDF viewer widget with page navigation and zoom."""

from typing import Optional, List, Dict, Any
from pathlib import Path

from PySide6.QtCore import Qt, Signal, QRectF, QPointF
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QScrollArea, QComboBox, QMessageBox
)

from desktop_app.pdf.renderer import PDFRenderer


class PDFPageView(QWidget):
    """Widget to display a single PDF page with signature overlays."""
    
    signature_clicked = Signal(int)  # Emits signature index
    page_clicked = Signal(QPointF)   # Emits click position
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap: Optional[QPixmap] = None
        self.signatures: List[Dict[str, Any]] = []  # [{"x": 100, "y": 200, "width": 150, "height": 50, "pixmap": QPixmap}, ...]
        self.setMinimumSize(400, 500)
    
    def set_page(self, pixmap: Optional[QPixmap]) -> None:
        """Set the PDF page to display."""
        self.pixmap = pixmap
        if pixmap:
            self.setFixedSize(pixmap.size())
        self.update()
    
    def add_signature_overlay(self, x: int, y: int, width: int, height: int, 
                             sig_pixmap: QPixmap) -> int:
        """
        Add a signature overlay at specified position.
        
        Returns:
            Index of added signature
        """
        self.signatures.append({
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "pixmap": sig_pixmap
        })
        self.update()
        return len(self.signatures) - 1
    
    def remove_signature(self, index: int) -> None:
        """Remove signature overlay by index."""
        if 0 <= index < len(self.signatures):
            self.signatures.pop(index)
            self.update()
    
    def clear_signatures(self) -> None:
        """Remove all signature overlays."""
        self.signatures.clear()
        self.update()
    
    def paintEvent(self, event):
        """Draw PDF page and signature overlays."""
        painter = QPainter(self)
        
        # Draw PDF page
        if self.pixmap:
            painter.drawPixmap(0, 0, self.pixmap)
        
        # Draw signature overlays
        for sig in self.signatures:
            # Draw signature image
            scaled_sig = sig["pixmap"].scaled(
                sig["width"], sig["height"],
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            painter.drawPixmap(sig["x"], sig["y"], scaled_sig)
            
            # Draw selection border
            painter.setPen(QPen(QColor(0, 120, 215), 2, Qt.PenStyle.DashLine))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(sig["x"], sig["y"], sig["width"], sig["height"])
    
    def mousePressEvent(self, event):
        """Handle mouse click (for signature selection or placement)."""
        pos = event.position().toPoint()
        
        # Check if clicked on existing signature
        for i, sig in enumerate(self.signatures):
            rect = QRectF(sig["x"], sig["y"], sig["width"], sig["height"])
            if rect.contains(pos):
                self.signature_clicked.emit(i)
                return
        
        # Otherwise, emit page click for new signature placement
        self.page_clicked.emit(event.position())


class PDFViewer(QWidget):
    """PDF viewer with navigation controls."""
    
    # Signals
    page_changed = Signal(int)  # Current page number
    signature_placed = Signal(int, int, int, int, int)  # page, x, y, width, height
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.renderer: Optional[PDFRenderer] = None
        self.current_page = 0
        self.zoom_level = 1.0
        self.pending_signature_pixmap: Optional[QPixmap] = None
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Initialize UI components."""
        layout = QVBoxLayout(self)
        
        # Top toolbar
        toolbar = QHBoxLayout()
        
        self.prev_btn = QPushButton("◀ Previous")
        self.prev_btn.clicked.connect(self.previous_page)
        toolbar.addWidget(self.prev_btn)
        
        self.page_label = QLabel("Page 0 of 0")
        toolbar.addWidget(self.page_label)
        
        self.next_btn = QPushButton("Next ▶")
        self.next_btn.clicked.connect(self.next_page)
        toolbar.addWidget(self.next_btn)
        
        toolbar.addStretch()
        
        # Zoom control
        toolbar.addWidget(QLabel("Zoom:"))
        self.zoom_combo = QComboBox()
        self.zoom_combo.addItems(["50%", "75%", "100%", "125%", "150%", "200%"])
        self.zoom_combo.setCurrentText("100%")
        self.zoom_combo.currentTextChanged.connect(self._on_zoom_changed)
        toolbar.addWidget(self.zoom_combo)
        
        layout.addLayout(toolbar)
        
        # Scroll area with page view
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.page_view = PDFPageView()
        self.page_view.page_clicked.connect(self._on_page_clicked)
        self.page_view.signature_clicked.connect(self._on_signature_clicked)
        
        self.scroll_area.setWidget(self.page_view)
        layout.addWidget(self.scroll_area)
        
        self._update_controls()
    
    def open_pdf(self, pdf_path: str) -> bool:
        """
        Open a PDF file for viewing.
        
        Returns:
            True if opened successfully
        """
        try:
            # Close existing PDF
            if self.renderer:
                self.renderer.close()
            
            # Open new PDF
            self.renderer = PDFRenderer(pdf_path)
            self.current_page = 0
            
            # Render first page
            self._render_current_page()
            self._update_controls()
            
            return True
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open PDF:\n{e}")
            return False
    
    def close_pdf(self) -> None:
        """Close the current PDF."""
        if self.renderer:
            self.renderer.close()
            self.renderer = None
        self.page_view.set_page(None)
        self.page_view.clear_signatures()
        self._update_controls()
    
    def _render_current_page(self) -> None:
        """Render the current page."""
        if not self.renderer:
            return
        
        pixmap = self.renderer.render_page(self.current_page, scale=self.zoom_level)
        self.page_view.set_page(pixmap)
        self.page_changed.emit(self.current_page)
    
    def previous_page(self) -> None:
        """Go to previous page."""
        if not self.renderer:
            return
        
        if self.current_page > 0:
            self.current_page -= 1
            self._render_current_page()
            self._update_controls()
    
    def next_page(self) -> None:
        """Go to next page."""
        if not self.renderer:
            return
        
        if self.current_page < self.renderer.page_count() - 1:
            self.current_page += 1
            self._render_current_page()
            self._update_controls()
    
    def goto_page(self, page_num: int) -> None:
        """Go to specific page."""
        if not self.renderer:
            return
        
        if 0 <= page_num < self.renderer.page_count():
            self.current_page = page_num
            self._render_current_page()
            self._update_controls()
    
    def _on_zoom_changed(self, text: str) -> None:
        """Handle zoom level change."""
        try:
            zoom_pct = int(text.rstrip('%'))
            self.zoom_level = zoom_pct / 100.0
            self._render_current_page()
        except ValueError:
            pass
    
    def _update_controls(self) -> None:
        """Update navigation controls state."""
        if not self.renderer:
            self.page_label.setText("No PDF loaded")
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
            return
        
        total = self.renderer.page_count()
        self.page_label.setText(f"Page {self.current_page + 1} of {total}")
        self.prev_btn.setEnabled(self.current_page > 0)
        self.next_btn.setEnabled(self.current_page < total - 1)
    
    def set_signature_for_placement(self, sig_pixmap: QPixmap) -> None:
        """
        Set a signature for placement (user will click on PDF to place).
        
        Args:
            sig_pixmap: Signature image to place
        """
        self.pending_signature_pixmap = sig_pixmap
        self.setCursor(QCursor(Qt.CursorShape.CrossCursor))
    
    def _on_page_clicked(self, pos: QPointF) -> None:
        """Handle click on PDF page."""
        if not self.pending_signature_pixmap:
            return
        
        # Place signature at clicked position
        # Default size: 150x50 pixels (typical signature size)
        width, height = 150, 50
        x = int(pos.x() - width / 2)  # Center on click
        y = int(pos.y() - height / 2)
        
        # Add signature overlay to current page
        self.page_view.add_signature_overlay(x, y, width, height, self.pending_signature_pixmap)
        
        # Emit signal for tracking
        self.signature_placed.emit(self.current_page, x, y, width, height)
        
        # Clear pending signature
        self.pending_signature_pixmap = None
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
    
    def _on_signature_clicked(self, index: int) -> None:
        """Handle click on existing signature (for removal/editing)."""
        reply = QMessageBox.question(
            self, "Remove Signature",
            "Do you want to remove this signature?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.page_view.remove_signature(index)
    
    def get_placed_signatures(self) -> List[Dict[str, Any]]:
        """
        Get all placed signatures on current page.
        
        Returns:
            List of signature dicts with position and size
        """
        return [
            {
                "page": self.current_page,
                "x": sig["x"],
                "y": sig["y"],
                "width": sig["width"],
                "height": sig["height"]
            }
            for sig in self.page_view.signatures
        ]
