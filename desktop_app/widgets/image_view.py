import logging
from typing import Optional, Tuple
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFrame
from PySide6.QtCore import Qt, Signal, QPointF, QRectF, QByteArray, QBuffer, QIODevice
from PySide6.QtGui import QPixmap, QImage, QPainter, QPen, QColor, QWheelEvent, QMouseEvent

LOG = logging.getLogger(__name__)

class ImageView(QGraphicsView):
    """A widget for displaying and interacting with images (zoom, pan, select)."""
    
    selectionChanged = Signal(tuple) # (x1, y1, x2, y2)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.pixmap_item: Optional[QGraphicsPixmapItem] = None
        self.selection_rect_item = None
        
        # State
        self._is_panning = False
        self._pan_start = QPointF()
        self._is_selecting = False
        self._selection_start = QPointF()
        self._selection_end = QPointF()
        self._zoom_level = 1.0
        self._selection_mode = True # True = Select, False = Pan
        self._drag_source_enabled = False
        
        # UI Setup
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setBackgroundBrush(QColor("#1e1e1e")) # Dark background
        
    def load_image(self, path: str):
        """Load image from file path."""
        pixmap = QPixmap(path)
        self._set_pixmap(pixmap)
        
    def load_image_bytes(self, data: bytes):
        """Load image from bytes."""
        img = QImage.fromData(data)
        pixmap = QPixmap.fromImage(img)
        self._set_pixmap(pixmap)
        
    def _set_pixmap(self, pixmap: QPixmap):
        self.scene.clear()
        self.pixmap_item = self.scene.addPixmap(pixmap)
        self.setSceneRect(self.pixmap_item.boundingRect())
        self.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        self.selection_rect_item = None
        
    def clear_image(self):
        self.scene.clear()
        self.pixmap_item = None
        self.selection_rect_item = None
        
    def set_selection_mode(self, enabled: bool):
        self._selection_mode = enabled
        if enabled:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.setCursor(Qt.CursorShape.CrossCursor)
        else:
            if not self._drag_source_enabled:
                self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
                self.setCursor(Qt.CursorShape.OpenHandCursor)
            else:
                self.setDragMode(QGraphicsView.DragMode.NoDrag)
                self.setCursor(Qt.CursorShape.PointingHandCursor)
            
    def set_drag_source(self, enabled: bool):
        """Enable dragging the image out of the view."""
        self._drag_source_enabled = enabled
        # Refresh cursor/mode
        self.set_selection_mode(self._selection_mode)

    def get_selection(self) -> Optional[Tuple[int, int, int, int]]:
        """Get selection coordinates (x1, y1, x2, y2) relative to image."""
        if not self.selection_rect_item or not self.pixmap_item:
            return None
            
        rect = self.selection_rect_item.rect()
        # Ensure coordinates are within image bounds
        img_rect = self.pixmap_item.boundingRect()
        x1 = max(0, int(rect.left()))
        y1 = max(0, int(rect.top()))
        x2 = min(int(img_rect.width()), int(rect.right()))
        y2 = min(int(img_rect.height()), int(rect.bottom()))
        
        if x2 <= x1 or y2 <= y1:
            return None
            
        return (x1, y1, x2, y2)
        
    def rotate(self, angle: float):
        """Rotate the view."""
        self.rotate(angle)

    # --- Events ---
    
    def wheelEvent(self, event: QWheelEvent):
        zoom_in = event.angleDelta().y() > 0
        factor = 1.1 if zoom_in else 0.9
        self.scale(factor, factor)
        
    def mousePressEvent(self, event: QMouseEvent):
        if self._selection_mode and event.button() == Qt.MouseButton.LeftButton:
            self._is_selecting = True
            pos = self.mapToScene(event.pos())
            self._selection_start = pos
            self._selection_end = pos
            self._update_selection_rect()
        elif self._drag_source_enabled and event.button() == Qt.MouseButton.LeftButton:
            # Prepare for drag
            self._pan_start = event.pos()
        else:
            super().mousePressEvent(event)
            
    def mouseMoveEvent(self, event: QMouseEvent):
        if self._is_selecting:
            self._selection_end = self.mapToScene(event.pos())
            self._update_selection_rect()
        elif self._drag_source_enabled and event.buttons() & Qt.MouseButton.LeftButton:
            # Check drag threshold
            if (event.pos() - self._pan_start).manhattanLength() > 10:
                self._start_drag()
        else:
            super().mouseMoveEvent(event)
            
    def _start_drag(self):
        if not self.pixmap_item:
            return
            
        drag = QDrag(self)
        mime_data = QMimeData()
        
        # Get current image data
        pixmap = self.pixmap_item.pixmap()
        mime_data.setImageData(pixmap.toImage())
        
        drag.setMimeData(mime_data)
        drag.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        drag.setHotSpot(QPointF(50, 50).toPoint())
        
        drag.exec(Qt.DropAction.CopyAction)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self._is_selecting:
            self._is_selecting = False
            self._selection_end = self.mapToScene(event.pos())
            self._update_selection_rect()
            
            sel = self.get_selection()
            if sel:
                self.selectionChanged.emit(sel)
        else:
            super().mouseReleaseEvent(event)
            
    def _update_selection_rect(self):
        if not self.pixmap_item:
            return
            
        if not self.selection_rect_item:
            self.selection_rect_item = self.scene.addRect(QRectF(), QPen(QColor("#00ff00"), 2), QColor(0, 255, 0, 50))
            self.selection_rect_item.setZValue(10)
            
        rect = QRectF(self._selection_start, self._selection_end).normalized()
        self.selection_rect_item.setRect(rect)
