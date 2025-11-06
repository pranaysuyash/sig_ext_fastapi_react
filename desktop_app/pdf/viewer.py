"""PDF viewer widget with page navigation and zoom."""

from typing import Optional, List, Dict, Any
from pathlib import Path
import sys

from PySide6.QtCore import Qt, Signal, QRectF, QPointF, QPoint
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QScrollArea, QComboBox, QMessageBox, QMenu, QToolTip
)

from desktop_app.pdf.renderer import PDFRenderer
from desktop_app.widgets.modern_mac_button import ModernMacButton


def _create_button(
    text: str = "",
    parent: Optional[QWidget] = None,
    *,
    use_modern_mac: Optional[bool] = None,
    primary: bool = False,
    color: str = 'blue',
    compact: bool = False  # Dialog buttons are typically not compact
) -> QPushButton:
    """Create a button, using ModernMacButton on macOS if available and requested.

    Args:
        text: Button text
        parent: Parent widget
        use_modern_mac: Force modern button (default: auto-detect macOS)
        primary: True for primary action buttons (colored)
        color: One of 'blue', 'purple', 'pink', 'red', 'orange', 'yellow', 'green', 'teal'
        compact: True for smaller buttons (sidebar/toolbar), False for larger (dialogs)
    """
    if use_modern_mac is None:
        use_modern_mac = sys.platform == "darwin"

    if use_modern_mac:
        try:
            btn = ModernMacButton(
                text, parent,
                primary=primary,
                color=color,
                glass=True,
                compact=compact
            )
            return btn
        except (NameError, TypeError):
            # Fallback if ModernMacButton not available or doesn't support compact
            pass

    # Default to standard QPushButton
    return QPushButton(text, parent)


class PDFPageView(QWidget):
    """Widget to display a single PDF page with signature overlays."""
    
    signature_clicked = Signal(int)  # Emits signature index
    page_clicked = Signal(QPointF)   # Emits click position
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap: Optional[QPixmap] = None
        self.signatures: List[Dict[str, Any]] = []  # [{"x": 100, "y": 200, "width": 150, "height": 50, "pixmap": QPixmap, "sig_path": ""}, ...]
        self.setMinimumSize(400, 500)
        
        # Drag/move state
        self.dragging_signature: Optional[int] = None
        self.drag_start_pos: Optional[QPointF] = None
        self.drag_offset_x: float = 0
        self.drag_offset_y: float = 0
        
        # Resize state
        self.resizing_signature: Optional[int] = None
        self.resize_handle: Optional[str] = None  # "nw", "ne", "sw", "se", "n", "s", "e", "w"
        self.resize_start_pos: Optional[QPointF] = None
        self.resize_orig_rect: Optional[Dict[str, float]] = None
        self.resize_aspect_ratio: Optional[float] = None
        self.selected_signature: Optional[int] = None  # Currently selected signature
        
        # Placement preview state
        self.preview_pixmap: Optional[QPixmap] = None
        self.preview_pos: Optional[QPointF] = None
        self.setMouseTracking(True)  # Enable mouse tracking for preview
        
        # Coordinate tooltip state
        self._coord_tooltips_enabled = False  # Off by default in PDF viewer
        self._last_tooltip_text = ""
    
    def set_page(self, pixmap: Optional[QPixmap]) -> None:
        """Set the PDF page to display."""
        self.pixmap = pixmap
        if pixmap:
            self.setFixedSize(pixmap.size())
        self.update()
    
    def set_preview_signature(self, sig_pixmap: Optional[QPixmap]) -> None:
        """Set signature for placement preview."""
        self.preview_pixmap = sig_pixmap
        self.update()
    
    def add_signature_overlay(self, x: int, y: int, width: int, height: int, 
                             sig_pixmap: QPixmap, sig_path: str = "") -> int:
        """
        Add a signature overlay at specified position.
        
        Args:
            sig_path: Path to signature image file (needed for PDF signing)
        
        Returns:
            Index of added signature
        """
        self.signatures.append({
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "pixmap": sig_pixmap,
            "sig_path": sig_path  # Store path with each signature
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
        for i, sig in enumerate(self.signatures):
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
            
            # Draw resize handles if this signature is selected
            if i == self.selected_signature:
                self._draw_resize_handles(painter, sig)
        
        # Draw placement preview if active
        if self.preview_pixmap and self.preview_pos:
            width, height = 150, 50
            x = int(self.preview_pos.x() - width / 2)
            y = int(self.preview_pos.y() - height / 2)
            
            # Draw semi-transparent preview
            painter.setOpacity(0.6)
            scaled_preview = self.preview_pixmap.scaled(
                width, height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            painter.drawPixmap(x, y, scaled_preview)
            
            # Draw preview border
            painter.setOpacity(1.0)
            painter.setPen(QPen(QColor(0, 200, 0), 2, Qt.PenStyle.DashLine))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(x, y, width, height)
    
    def mousePressEvent(self, event):
        """Handle mouse click (for signature selection or placement)."""
        pos = event.position()
        pos_point = pos.toPoint()
        
        # Check if clicked on existing signature
        for i, sig in enumerate(self.signatures):
            rect = QRectF(sig["x"], sig["y"], sig["width"], sig["height"])
            if rect.contains(pos_point):
                # Select this signature
                self.selected_signature = i
                self.update()
                
                # Right-click: show context menu
                if event.button() == Qt.MouseButton.RightButton:
                    self._show_signature_context_menu(i, event.globalPosition().toPoint())
                    return
                
                # Left-click: check if on resize handle first
                if event.button() == Qt.MouseButton.LeftButton:
                    handle = self._get_resize_handle_at(pos, sig)
                    if handle:
                        # Start resizing
                        self.resizing_signature = i
                        self.resize_handle = handle
                        self.resize_start_pos = pos
                        self.resize_orig_rect = {
                            "x": sig["x"],
                            "y": sig["y"],
                            "width": sig["width"],
                            "height": sig["height"]
                        }
                        self.resize_aspect_ratio = sig["width"] / sig["height"]
                        self.setCursor(self._get_cursor_for_handle(handle))
                        return
                    else:
                        # Start dragging
                        self.dragging_signature = i
                        self.drag_start_pos = pos
                        self.drag_offset_x = pos.x() - sig["x"]
                        self.drag_offset_y = pos.y() - sig["y"]
                        self.setCursor(Qt.CursorShape.ClosedHandCursor)
                return
        
        # Clicked on empty area - deselect
        self.selected_signature = None
        self.update()
        
        # Otherwise, emit page click for new signature placement
        if event.button() == Qt.MouseButton.LeftButton:
            self.page_clicked.emit(pos)
    
    def _show_signature_context_menu(self, index: int, global_pos: QPoint) -> None:
        """Show context menu for signature."""
        menu = QMenu(self)
        remove_action = menu.addAction("🗑️ Remove Signature")
        
        action = menu.exec(global_pos)
        if action == remove_action:
            self.remove_signature(index)
    
    def _draw_resize_handles(self, painter: QPainter, sig: Dict[str, Any]) -> None:
        """Draw resize handles on selected signature."""
        handle_size = 8
        x, y, w, h = sig["x"], sig["y"], sig["width"], sig["height"]
        
        # Handle positions: corners and edges
        handles = {
            "nw": (x, y),
            "ne": (x + w, y),
            "sw": (x, y + h),
            "se": (x + w, y + h),
            "n": (x + w/2, y),
            "s": (x + w/2, y + h),
            "e": (x + w, y + h/2),
            "w": (x, y + h/2)
        }
        
        painter.setPen(QPen(QColor(0, 120, 215), 1))
        painter.setBrush(QColor(255, 255, 255))
        
        for handle_pos in handles.values():
            hx, hy = handle_pos
            painter.drawRect(
                int(hx - handle_size/2),
                int(hy - handle_size/2),
                handle_size,
                handle_size
            )
    
    def _get_resize_handle_at(self, pos: QPointF, sig: Dict[str, Any]) -> Optional[str]:
        """Check if position is over a resize handle. Returns handle name or None."""
        handle_size = 8
        tolerance = handle_size / 2 + 2
        
        x, y, w, h = sig["x"], sig["y"], sig["width"], sig["height"]
        px, py = pos.x(), pos.y()
        
        # Check each handle
        handles = {
            "nw": (x, y),
            "ne": (x + w, y),
            "sw": (x, y + h),
            "se": (x + w, y + h),
            "n": (x + w/2, y),
            "s": (x + w/2, y + h),
            "e": (x + w, y + h/2),
            "w": (x, y + h/2)
        }
        
        for handle_name, (hx, hy) in handles.items():
            if abs(px - hx) <= tolerance and abs(py - hy) <= tolerance:
                return handle_name
        
        return None
    
    def _get_cursor_for_handle(self, handle: str) -> Qt.CursorShape:
        """Get cursor shape for resize handle."""
        cursors = {
            "nw": Qt.CursorShape.SizeFDiagCursor,
            "se": Qt.CursorShape.SizeFDiagCursor,
            "ne": Qt.CursorShape.SizeBDiagCursor,
            "sw": Qt.CursorShape.SizeBDiagCursor,
            "n": Qt.CursorShape.SizeVerCursor,
            "s": Qt.CursorShape.SizeVerCursor,
            "e": Qt.CursorShape.SizeHorCursor,
            "w": Qt.CursorShape.SizeHorCursor
        }
        return cursors.get(handle, Qt.CursorShape.ArrowCursor)
    
    def enable_coordinate_tooltips(self, enabled: bool) -> None:
        """Enable or disable coordinate tooltips for this page view."""
        self._coord_tooltips_enabled = bool(enabled)
    
    def _show_coordinate_tooltip(self, event) -> None:
        """Show coordinate tooltip at mouse position if enabled."""
        if not self._coord_tooltips_enabled or not self.pixmap:
            return
        
        pos = event.position()
        x = int(pos.x())
        y = int(pos.y())
        
        # Build tooltip text with PDF page coordinates
        coords = f"PDF: {x}, {y}"
        
        # Add signature info if hovering over one
        for i, sig in enumerate(self.signatures):
            rect = QRectF(sig["x"], sig["y"], sig["width"], sig["height"])
            if rect.contains(pos.toPoint()):
                coords += f"  •  Sig#{i+1}: {sig['width']}×{sig['height']}"
                if i == self.selected_signature:
                    coords += " [selected]"
                break
        
        # Show during resize/drag operations
        if self.resizing_signature is not None:
            sig = self.signatures[self.resizing_signature]
            coords += f"  •  Resizing: {sig['width']}×{sig['height']}"
        elif self.dragging_signature is not None:
            sig = self.signatures[self.dragging_signature]
            coords += f"  •  Moving: ({sig['x']}, {sig['y']})"
        elif self.preview_pixmap:
            coords += f"  •  Preview: {self.preview_pixmap.width()}×{self.preview_pixmap.height()}"
        
        # Use HTML with explicit black text on yellow background
        text = f'<span style="background-color: #ffffcc; color: #000000; padding: 4px; border: 1px solid #888;">{coords}</span>'
        
        # Avoid spamming identical tooltips
        if text == self._last_tooltip_text:
            return
        self._last_tooltip_text = text
        
        # Show tooltip near cursor
        global_pos = self.mapToGlobal(event.position().toPoint())
        QToolTip.showText(global_pos, text, self)
    
    def mouseMoveEvent(self, event):
        """Handle mouse move (for dragging/resizing signatures or preview)."""
        pos = event.position()
        
        # Always update coordinate tooltip if enabled
        self._show_coordinate_tooltip(event)
        
        if self.resizing_signature is not None:
            # Resizing an existing signature
            sig = self.signatures[self.resizing_signature]
            orig = self.resize_orig_rect
            handle = self.resize_handle
            
            dx = pos.x() - self.resize_start_pos.x()
            dy = pos.y() - self.resize_start_pos.y()
            
            # Update dimensions based on handle
            new_x, new_y = orig["x"], orig["y"]
            new_width, new_height = orig["width"], orig["height"]
            
            if "w" in handle:  # West handles (left side)
                new_x = orig["x"] + dx
                new_width = orig["width"] - dx
            if "e" in handle:  # East handles (right side)
                new_width = orig["width"] + dx
            if "n" in handle:  # North handles (top side)
                new_y = orig["y"] + dy
                new_height = orig["height"] - dy
            if "s" in handle:  # South handles (bottom side)
                new_height = orig["height"] + dy
            
            # Preserve aspect ratio for corner handles
            if handle in ["nw", "ne", "sw", "se"]:
                # Use width as primary dimension
                new_height = new_width / self.resize_aspect_ratio
                if "n" in handle:
                    new_y = orig["y"] + orig["height"] - new_height
            
            # Enforce minimum size
            min_size = 20
            if new_width >= min_size and new_height >= min_size:
                sig["x"] = int(new_x)
                sig["y"] = int(new_y)
                sig["width"] = int(new_width)
                sig["height"] = int(new_height)
                
                # Constrain to page bounds
                if self.pixmap:
                    if sig["x"] < 0:
                        sig["width"] += sig["x"]
                        sig["x"] = 0
                    if sig["y"] < 0:
                        sig["height"] += sig["y"]
                        sig["y"] = 0
                    if sig["x"] + sig["width"] > self.pixmap.width():
                        sig["width"] = self.pixmap.width() - sig["x"]
                    if sig["y"] + sig["height"] > self.pixmap.height():
                        sig["height"] = self.pixmap.height() - sig["y"]
            
            self.update()
            
        elif self.dragging_signature is not None:
            # Dragging an existing signature
            sig = self.signatures[self.dragging_signature]
            
            # Update signature position
            sig["x"] = int(pos.x() - self.drag_offset_x)
            sig["y"] = int(pos.y() - self.drag_offset_y)
            
            # Constrain to page bounds
            if self.pixmap:
                sig["x"] = max(0, min(sig["x"], self.pixmap.width() - sig["width"]))
                sig["y"] = max(0, min(sig["y"], self.pixmap.height() - sig["height"]))
            
            self.update()
            
        elif self.preview_pixmap:
            # Show placement preview
            self.preview_pos = pos
            self.update()
            
        else:
            # Update cursor to show if hovering over a signature or resize handle
            pos_point = pos.toPoint()
            cursor_set = False
            
            for i, sig in enumerate(self.signatures):
                rect = QRectF(sig["x"], sig["y"], sig["width"], sig["height"])
                if rect.contains(pos_point):
                    # Check if over a resize handle (for selected signature)
                    if i == self.selected_signature:
                        handle = self._get_resize_handle_at(pos, sig)
                        if handle:
                            self.setCursor(self._get_cursor_for_handle(handle))
                            cursor_set = True
                            break
                    
                    # Otherwise show move cursor
                    if not cursor_set:
                        self.setCursor(Qt.CursorShape.OpenHandCursor)
                        cursor_set = True
                    break
            
            if not cursor_set:
                self.setCursor(Qt.CursorShape.ArrowCursor)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release (end dragging/resizing)."""
        if self.resizing_signature is not None:
            self.resizing_signature = None
            self.resize_handle = None
            self.resize_start_pos = None
            self.resize_orig_rect = None
            self.resize_aspect_ratio = None
            self.setCursor(Qt.CursorShape.ArrowCursor)
        elif self.dragging_signature is not None:
            self.dragging_signature = None
            self.drag_start_pos = None
            self.setCursor(Qt.CursorShape.ArrowCursor)


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
        self.pending_signature_path: str = ""  # Track signature file path
        # Base DPI used for rendering; must be kept in sync with PDFRenderer.render_page default
        self.base_dpi: int = 150
        # Track all signatures across all pages: {page_num: [sig_dict, ...]}
        self.all_signatures: Dict[int, List[Dict[str, Any]]] = {}
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Initialize UI components."""
        layout = QVBoxLayout(self)
        
        # Top toolbar
        toolbar = QHBoxLayout()
        
        self.prev_btn = _create_button("◀ Previous", self)
        self.prev_btn.clicked.connect(self.previous_page)
        toolbar.addWidget(self.prev_btn)
        
        self.page_label = QLabel("Page 0 of 0")
        toolbar.addWidget(self.page_label)
        
        self.next_btn = _create_button("Next ▶", self)
        self.next_btn.clicked.connect(self.next_page)
        toolbar.addWidget(self.next_btn)
        
        toolbar.addStretch()
        
        # Zoom control
        toolbar.addWidget(QLabel("Zoom:"))
        self.zoom_combo = QComboBox()
        # Provide document-style options and common percentages
        self.zoom_combo.addItems(["Whole Page", "Page Width", "50%", "75%", "100%", "125%", "150%", "200%"])
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
    
    def enable_coordinate_tooltips(self, enabled: bool) -> None:
        """Enable or disable coordinate tooltips in the PDF page view."""
        if self.page_view:
            self.page_view.enable_coordinate_tooltips(enabled)
    
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
            
            # Default to showing the whole page on open
            self.zoom_combo.setCurrentText("Whole Page")
            
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
        self.all_signatures.clear()  # Clear all tracked signatures
        self._update_controls()
    
    def _render_current_page(self) -> None:
        """Render the current page."""
        if not self.renderer:
            return
        
        pixmap = self.renderer.render_page(self.current_page, scale=self.zoom_level, dpi=self.base_dpi)
        self.page_view.set_page(pixmap)
        
        # Restore signatures for this page
        self._load_page_signatures()
        
        self.page_changed.emit(self.current_page)
    
    def _save_page_signatures(self) -> None:
        """Save current page's signatures before switching pages."""
        if self.current_page not in self.all_signatures:
            self.all_signatures[self.current_page] = []
        else:
            self.all_signatures[self.current_page].clear()
        
        # Copy signatures from page_view
        for sig in self.page_view.signatures:
            self.all_signatures[self.current_page].append(sig.copy())
    
    def _load_page_signatures(self) -> None:
        """Load signatures for current page from storage."""
        self.page_view.clear_signatures()
        
        if self.current_page in self.all_signatures:
            for sig in self.all_signatures[self.current_page]:
                self.page_view.signatures.append(sig.copy())
            self.page_view.update()
    
    def previous_page(self) -> None:
        """Go to previous page."""
        if not self.renderer:
            return
        
        if self.current_page > 0:
            self._save_page_signatures()  # Save before switching
            self.current_page -= 1
            self._render_current_page()
            self._update_controls()
    
    def next_page(self) -> None:
        """Go to next page."""
        if not self.renderer:
            return
        
        if self.current_page < self.renderer.page_count() - 1:
            self._save_page_signatures()  # Save before switching
            self.current_page += 1
            self._render_current_page()
            self._update_controls()
    
    def goto_page(self, page_num: int) -> None:
        """Go to specific page."""
        if not self.renderer:
            return
        
        if 0 <= page_num < self.renderer.page_count():
            self._save_page_signatures()  # Save before switching
            self.current_page = page_num
            self._render_current_page()
            self._update_controls()
    
    def _on_zoom_changed(self, text: str) -> None:
        """Handle zoom level change."""
        if text in ("Whole Page", "Fit to Screen"):
            # Backward compatible: treat "Fit to Screen" as "Whole Page"
            self._fit_to_page()
            return
        if text == "Page Width":
            self._fit_to_width()
            return
        try:
            zoom_pct = int(text.rstrip('%'))
            self.zoom_level = zoom_pct / 100.0
            self._render_current_page()
        except ValueError:
            pass
    
    def _fit_to_page(self) -> None:
        """Fit the entire page within the viewport (like Word's "Whole Page")."""
        if not self.renderer:
            return

        page_width_pt, page_height_pt = self.renderer.get_page_size(self.current_page)
        if page_width_pt <= 0 or page_height_pt <= 0:
            return

        # Available area in pixels
        avail_w_px = max(1, self.scroll_area.viewport().width() - 20)
        avail_h_px = max(1, self.scroll_area.viewport().height() - 20)

        # Convert page size (points) to pixels at scale=1 using base DPI
        page_w_px_at_100 = page_width_pt * self.base_dpi / 72.0
        page_h_px_at_100 = page_height_pt * self.base_dpi / 72.0

        # Required scale so the rendered bitmap fits both dimensions
        s_w = avail_w_px / page_w_px_at_100
        s_h = avail_h_px / page_h_px_at_100
        self.zoom_level = max(0.1, min(min(s_w, s_h), 3.0))

        self._render_current_page()

        # Reflect custom mode in dropdown
        self._set_zoom_combo_mode("Whole Page")

    def _fit_to_width(self) -> None:
        """Fit page width to viewport (like Word's "Page Width")."""
        if not self.renderer:
            return

        page_width_pt, page_height_pt = self.renderer.get_page_size(self.current_page)
        if page_width_pt <= 0 or page_height_pt <= 0:
            return

        avail_w_px = max(1, self.scroll_area.viewport().width() - 20)
        page_w_px_at_100 = page_width_pt * self.base_dpi / 72.0
        s_w = avail_w_px / page_w_px_at_100
        self.zoom_level = max(0.1, min(s_w, 3.0))

        self._render_current_page()

        self._set_zoom_combo_mode("Page Width")

    def _set_zoom_combo_mode(self, label: str) -> None:
        """Helper to set the zoom combo without triggering handlers."""
        self.zoom_combo.blockSignals(True)
        idx = self.zoom_combo.findText(label)
        if idx >= 0:
            self.zoom_combo.setCurrentIndex(idx)
        else:
            # Fallback: set closest percentage text
            pct = int(self.zoom_level * 100)
            for i in range(self.zoom_combo.count()):
                t = self.zoom_combo.itemText(i)
                if t.endswith('%') and t.rstrip('%').isdigit() and int(t.rstrip('%')) == pct:
                    self.zoom_combo.setCurrentIndex(i)
                    break
        self.zoom_combo.blockSignals(False)
    
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
    
    def set_signature_for_placement(self, sig_pixmap: QPixmap, sig_path: str = "") -> None:
        """
        Set a signature for placement (user will click on PDF to place).
        
        Args:
            sig_pixmap: Signature image to place
            sig_path: Path to signature image file (for PDF embedding)
        """
        self.pending_signature_pixmap = sig_pixmap
        self.pending_signature_path = sig_path
        self.page_view.set_preview_signature(sig_pixmap)  # Enable preview
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
        
        # Add signature overlay to current page with path
        self.page_view.add_signature_overlay(
            x, y, width, height, 
            self.pending_signature_pixmap,
            self.pending_signature_path
        )
        
        # Emit signal for tracking
        self.signature_placed.emit(self.current_page, x, y, width, height)
        
        # Clear pending signature and preview
        self.pending_signature_pixmap = None
        self.pending_signature_path = ""
        self.page_view.set_preview_signature(None)  # Disable preview
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
    
    def _on_signature_clicked(self, index: int) -> None:
        """Handle click on existing signature (for removal/editing)."""
        # This is now handled in PDFPageView's mousePressEvent for dragging
        # Only called for actual removal requests
        pass
    
    def get_placed_signatures(self) -> List[Dict[str, Any]]:
        """
        Get all placed signatures across all pages.
        
        Returns:
            List of signature dicts with page, position, size, and image path
        """
        # Save current page signatures first
        self._save_page_signatures()
        
        # Collect all signatures from all pages
        all_sigs = []
        for page_num, sigs in self.all_signatures.items():
            for sig in sigs:
                all_sigs.append({
                    "page": page_num,
                    "x": sig["x"],
                    "y": sig["y"],
                    "width": sig["width"],
                    "height": sig["height"],
                    "sig_path": sig.get("sig_path", ""),
                    # Provide metadata so signer can convert from pixels to points
                    "units": "px",
                    "dpi": self.base_dpi,
                    "scale": self.zoom_level,
                })
        
        return all_sigs
