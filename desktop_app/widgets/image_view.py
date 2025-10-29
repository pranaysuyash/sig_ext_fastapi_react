from __future__ import annotations

import math

from PySide6.QtCore import Qt, QRect, QRectF, QPoint, QPointF, QSize, Signal
from PySide6.QtGui import QImage, QPixmap, QWheelEvent, QTransform
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QRubberBand


class ImageView(QGraphicsView):
    """Image viewer with rubber-band rectangle selection and zoom/pan."""

    # Emitted when a selection rectangle is finalized (mouse release)
    selectionChanged = Signal(QRect)
    # Emitted when zoom level changes
    zoomChanged = Signal()
    # Emitted when the viewport geometry or visible scene region changes
    viewChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self._pixmap_item = None
        self._image = None
        self._rubber = QRubberBand(QRubberBand.Rectangle, self)
        self._origin = QPoint()
        self._last_rect = QRect()
        self._last_rect_scene_bounds = QRectF()
        self._last_reported_coords = (0, 0, 0, 0)
        self.setMouseTracking(True)
        self.setDragMode(QGraphicsView.NoDrag)  # Disable hand drag by default
        self._zoom = 1.0
        self._selection_mode = True  # True = select, False = pan
        self._rotation = 0.0  # Track view rotation for contextual controls

    def load_image_bytes(self, data: bytes) -> None:
        image = QImage.fromData(data)
        self.set_image(image)

    def set_image(self, image: QImage) -> None:
        self.scene().clear()
        self._image = image
        pix = QPixmap.fromImage(image)
        self._pixmap_item = self.scene().addPixmap(pix)
        self.setSceneRect(pix.rect())
        self._last_rect = QRect()
        self._last_rect_scene_bounds = QRectF()
        self._last_reported_coords = (0, 0, 0, 0)
        self.fit()

    def clear_image(self) -> None:
        """Clear the current image and remove scene items."""
        self.scene().clear()
        self._image = None
        self._pixmap_item = None
        self._last_rect = QRect()
        self._last_rect_scene_bounds = QRectF()
        self.setTransform(QTransform())
        self._zoom = 1.0
        self._rotation = 0.0
        self.viewChanged.emit()

    def image(self) -> QImage | None:
        return self._image

    def has_image(self) -> bool:
        return self._image is not None

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
            if not self._last_rect.isNull():
                # Persist selection bounds in scene coordinates so zoom/fit/rotation stay consistent
                scene_points = [
                    self.mapToScene(self._last_rect.topLeft()),
                    self.mapToScene(self._last_rect.topRight()),
                    self.mapToScene(self._last_rect.bottomLeft()),
                    self.mapToScene(self._last_rect.bottomRight()),
                ]
                xs = [pt.x() for pt in scene_points]
                ys = [pt.y() for pt in scene_points]
                min_point = QPointF(min(xs), min(ys))
                max_point = QPointF(max(xs), max(ys))
                self._last_rect_scene_bounds = QRectF(min_point, max_point).normalized()
            else:
                self._last_rect_scene_bounds = QRectF()
                self._last_reported_coords = (0, 0, 0, 0)
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
        if not self._pixmap_item or self._last_rect_scene_bounds.isNull():
            return (0, 0, 0, 0)

        bounds = self._last_rect_scene_bounds

        # The stored bounds reflect image-space coordinates; map directly to ints.
        x1 = math.floor(bounds.left())
        y1 = math.floor(bounds.top())
        x2 = math.ceil(bounds.right())
        y2 = math.ceil(bounds.bottom())

        # Clamp coordinates to the image's actual boundaries to prevent errors.
        img_rect = self._pixmap_item.pixmap().rect()

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(img_rect.width(), x2)
        y2 = min(img_rect.height(), y2)

        # Ensure the resulting rectangle has valid dimensions.
        if x2 <= x1 or y2 <= y1:
            self._last_reported_coords = (0, 0, 0, 0)
            return (0, 0, 0, 0)

        coords = (x1, y1, x2, y2)
        if coords != self._last_reported_coords:
            print(f"[ImageView] Selection -> ({x1},{y1})→({x2},{y2}) [{x2 - x1}×{y2 - y1}]")
            self._last_reported_coords = coords
        return (x1, y1, x2, y2)

    def selected_rect(self) -> QRect:
        return QRect(self._last_rect)

    def clear_selection(self) -> None:
        self._last_rect = QRect()
        self._last_rect_scene_bounds = QRectF()
        self._last_reported_coords = (0, 0, 0, 0)
        self._rubber.hide()
        self.selectionChanged.emit(QRect())

    def crop_selection(self) -> QImage | None:
        """Return a QImage cropped to the selected rect (no processing)."""
        if not self._image or self._last_rect_scene_bounds.isNull():
            return None
        # Map to image coordinates
        x1, y1, x2, y2 = self.selected_rect_image_coords()
        if x2 <= x1 or y2 <= y1:
            return None
        width = max(1, x2 - x1)
        height = max(1, y2 - y1)
        return self._image.copy(QRect(x1, y1, width, height))

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
        self.zoomChanged.emit()
        self.viewChanged.emit()

    def reset_zoom(self):
        # Reset any transforms then fit
        self.setTransform(QTransform())
        self._zoom = 1.0
        self._rotation = 0.0
        self.zoomChanged.emit()
        self.viewChanged.emit()

    def fit(self):
        if not self.scene() or self.sceneRect().isNull():
            return
        self.reset_zoom()
        try:
            if self._pixmap_item is not None:
                self.fitInView(self._pixmap_item, Qt.KeepAspectRatio)
            else:
                self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)
        except Exception:
            self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)
        # Update zoom level after fit
        transform = self.transform()
        self._zoom = transform.m11()  # Get actual scale factor
        self.zoomChanged.emit()
        self.viewChanged.emit()

    def rotate_view(self, degrees: float):
        """Rotate the view around its center without altering the image data."""
        if not self._pixmap_item:
            return
        self.rotate(degrees)
        self._rotation = (self._rotation + degrees) % 360
        self.viewChanged.emit()

    def toggle_selection_mode(self, enable: bool):
        """Toggle between selection mode and pan mode."""
        self._selection_mode = enable
        if not enable:
            # Hide rubber band if switching to pan mode
            self._rubber.hide()

    def scrollContentsBy(self, dx: int, dy: int) -> None:
        super().scrollContentsBy(dx, dy)
        self.viewChanged.emit()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.viewChanged.emit()

    def set_zoom_percent(self, percent: float):
        """Set zoom to an explicit percentage relative to image pixel size."""
        if not self._pixmap_item:
            return
        target_scale = max(0.01, percent / 100.0)
        if math.isclose(self._zoom, target_scale, rel_tol=1e-4, abs_tol=1e-4):
            return
        current_scale = self._zoom if self._zoom > 0 else 1.0
        factor = target_scale / current_scale
        self._apply_zoom(factor)
