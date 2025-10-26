from __future__ import annotations

from PySide6.QtCore import Qt, QRect, QPoint, QSize, Signal
from PySide6.QtGui import QImage, QPixmap, QWheelEvent, QTransform
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QRubberBand


class ImageView(QGraphicsView):
    """Image viewer with rubber-band rectangle selection and zoom/pan."""

    # Emitted when a selection rectangle is finalized (mouse release)
    selectionChanged = Signal(QRect)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self._pixmap_item = None
        self._image = None
        self._rubber = QRubberBand(QRubberBand.Rectangle, self)
        self._origin = QPoint()
        self._last_rect = QRect()
        self.setMouseTracking(True)
        self.setDragMode(QGraphicsView.NoDrag)  # Disable hand drag by default
        self._zoom = 1.0
        self._selection_mode = True  # True = select, False = pan

    def load_image_bytes(self, data: bytes) -> None:
        image = QImage.fromData(data)
        self.set_image(image)

    def set_image(self, image: QImage) -> None:
        self.scene().clear()
        self._image = image
        pix = QPixmap.fromImage(image)
        self._pixmap_item = self.scene().addPixmap(pix)
        self.setSceneRect(pix.rect())
        self.fit()
        self._last_rect = QRect()

    def image(self) -> QImage | None:
        return self._image

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self._selection_mode:
            # Selection mode: start rubber band
            self._origin = event.pos()
            self._rubber.setGeometry(QRect(self._origin, QSize(1, 1)))
            self._rubber.show()
            event.accept()
        elif event.button() == Qt.MiddleButton or (event.button() == Qt.LeftButton and not self._selection_mode):
            # Pan mode: enable hand drag temporarily
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            super().mousePressEvent(event)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._rubber.isVisible() and self._selection_mode:
            rect = QRect(self._origin, event.pos()).normalized()
            self._rubber.setGeometry(rect)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self._rubber.isVisible() and self._selection_mode:
            self._last_rect = self._rubber.geometry()
            self._rubber.hide()
            self.selectionChanged.emit(self._last_rect)
            event.accept()
        elif event.button() == Qt.MiddleButton or (event.button() == Qt.LeftButton and not self._selection_mode):
            # Reset drag mode
            self.setDragMode(QGraphicsView.NoDrag)
            super().mouseReleaseEvent(event)
        else:
            super().mouseReleaseEvent(event)

    def selected_rect_image_coords(self) -> tuple[int, int, int, int]:
        """Return selection in image coordinates (x1,y1,x2,y2)."""
        if not self._pixmap_item or self._last_rect.isNull():
            return (0, 0, 0, 0)

        # Map from view coords to scene coords, then to image pixel coords
        top_left = self.mapToScene(self._last_rect.topLeft())
        bottom_right = self.mapToScene(self._last_rect.bottomRight())
        x1, y1 = int(top_left.x()), int(top_left.y())
        x2, y2 = int(bottom_right.x()), int(bottom_right.y())
        # Clamp to image bounds
        rect = self._pixmap_item.pixmap().rect()
        x1 = max(0, min(x1, rect.width()))
        x2 = max(0, min(x2, rect.width()))
        y1 = max(0, min(y1, rect.height()))
        y2 = max(0, min(y2, rect.height()))
        return (x1, y1, x2, y2)

    def selected_rect(self) -> QRect:
        return QRect(self._last_rect)

    def clear_selection(self) -> None:
        self._last_rect = QRect()
        self._rubber.hide()
        self.selectionChanged.emit(QRect())

    def crop_selection(self) -> QImage | None:
        """Return a QImage cropped to the selected rect (no processing)."""
        if not self._image or self._last_rect.isNull():
            return None
        # Map to image coordinates
        x1, y1, x2, y2 = self.selected_rect_image_coords()
        if x2 <= x1 or y2 <= y1:
            return None
        return self._image.copy(QRect(x1, y1, x2 - x1, y2 - y1))

    # Zoom/pan helpers
    def wheelEvent(self, event: QWheelEvent) -> None:
        # Ctrl+wheel or trackpad gesture to zoom
        if event.modifiers() & Qt.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()
        else:
            super().wheelEvent(event)

    def zoom_in(self):
        self._apply_zoom(1.25)

    def zoom_out(self):
        self._apply_zoom(0.8)

    def _apply_zoom(self, factor: float):
        self._zoom *= factor
        self.scale(factor, factor)

    def reset_zoom(self):
        # Reset any transforms then fit
        self.setTransform(QTransform())
        self._zoom = 1.0

    def fit(self):
        if not self.scene() or self.sceneRect().isNull():
            return
        self.reset_zoom()
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def toggle_selection_mode(self, enable: bool):
        """Toggle between selection mode and pan mode."""
        self._selection_mode = enable
        if not enable:
            # Hide rubber band if switching to pan mode
            self._rubber.hide()

