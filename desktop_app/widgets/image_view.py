from __future__ import annotations

from PySide6.QtCore import Qt, QRect, QPoint, QSize
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QRubberBand


class ImageView(QGraphicsView):
    """Simple image viewer with rubber-band rectangle selection."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self._pixmap_item = None
        self._rubber = QRubberBand(QRubberBand.Rectangle, self)
        self._origin = QPoint()
        self._last_rect = QRect()
        self.setMouseTracking(True)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def load_image_bytes(self, data: bytes) -> None:
        image = QImage.fromData(data)
        self.set_image(image)

    def set_image(self, image: QImage) -> None:
        self.scene().clear()
        pix = QPixmap.fromImage(image)
        self._pixmap_item = self.scene().addPixmap(pix)
        self.setSceneRect(pix.rect())
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._origin = event.pos()
            self._rubber.setGeometry(QRect(self._origin, QSize(1, 1)))
            self._rubber.show()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._rubber.isVisible():
            rect = QRect(self._origin, event.pos()).normalized()
            self._rubber.setGeometry(rect)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self._rubber.isVisible():
            self._last_rect = self._rubber.geometry()
            self._rubber.hide()
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
