from __future__ import annotations

import math

from PySide6.QtCore import Qt, QRect, QRectF, QPoint, QPointF, QSize, Signal
from PySide6.QtGui import QImage, QPixmap, QWheelEvent, QTransform, QDragEnterEvent, QDragMoveEvent, QDropEvent
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QLabel, QRubberBand, QToolTip


class ImageView(QGraphicsView):
    """Image viewer with rubber-band rectangle selection and zoom/pan."""

    # Emitted when a selection rectangle is finalized (mouse release)
    selectionChanged = Signal(QRect)
    # Emitted when zoom level changes
    zoomChanged = Signal()
    # Emitted when the viewport geometry or visible scene region changes
    viewChanged = Signal()
    fileDropped = Signal(str)

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
        self._auto_fit_mode = True  # True = auto-fit on resize, False = manual zoom
        # Coordinate tooltip state
        self._coord_tooltips_enabled = True
        self._last_hover_coords = (-1, -1)
        self._last_tooltip_text = ""
        self.setAcceptDrops(True)

        # Selection hint overlay
        self._hint_label = QLabel("Drag to select area", self)
        self._hint_label.setAlignment(Qt.AlignCenter)
        self._hint_label.setStyleSheet(
            "QLabel { "
            "  background-color: rgba(0, 0, 0, 120); "
            "  color: white; "
            "  padding: 12px 24px; "
            "  border-radius: 8px; "
            "  font-size: 14px; "
            "}"
        )
        self._hint_label.hide()
        self._hint_dismissed = False

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
        # Enable auto-fit for new images
        self._auto_fit_mode = True
        self.fit()
        # Show hint for new image
        self._show_selection_hint()

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
            # Hide hint on first interaction
            if not self._hint_dismissed:
                self._hint_dismissed = True
                self._hint_label.hide()
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
            # Update live coordinate tooltip while dragging a selection
            self._maybe_show_coord_tooltip(event, dragging=True)
            event.accept()
        else:
            # Update live coordinate tooltip on hover
            self._maybe_show_coord_tooltip(event, dragging=False)
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

    def mouseDoubleClickEvent(self, event) -> None:
        """Double-click toggles between fit and 100% zoom."""
        if event.button() == Qt.LeftButton and self._pixmap_item:
            current_zoom = self.get_zoom_percent()
            if abs(current_zoom - 100.0) < 5.0:  # Close to 100%
                # Switch to fit mode
                self._auto_fit_mode = True
                self.fit()
            else:
                # Switch to 100%
                self._auto_fit_mode = False
                self.set_zoom_percent(100.0)
            event.accept()
        else:
            super().mouseDoubleClickEvent(event)

    # -------- Drag & drop helpers --------
    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    path = url.toLocalFile()
                    if path:
                        self.fileDropped.emit(path)
                        event.acceptProposedAction()
                        return
        event.ignore()

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

        # Ensure minimum 2px extent to prevent collapsed selections due to rounding
        if x2 - x1 < 2:
            x2 = min(img_rect.width(), x1 + 2)
        if y2 - y1 < 2:
            y2 = min(img_rect.height(), y1 + 2)

        # Ensure the resulting rectangle has valid dimensions.
        if x2 <= x1 or y2 <= y1:
            self._last_reported_coords = (0, 0, 0, 0)
            return (0, 0, 0, 0)

        coords = (x1, y1, x2, y2)
        if coords != self._last_reported_coords:
            print(f"[ImageView] Selection -> ({x1},{y1})→({x2},{y2}) [{x2 - x1}×{y2 - y1}] (scene bounds: {bounds.left():.1f},{bounds.top():.1f}→{bounds.right():.1f},{bounds.bottom():.1f})")
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

    # -------- Coordinate tooltip helpers --------
    def enable_coordinate_tooltips(self, enabled: bool) -> None:
        self._coord_tooltips_enabled = bool(enabled)

    def _maybe_show_coord_tooltip(self, event, dragging: bool) -> None:
        if not self._coord_tooltips_enabled or not self._pixmap_item:
            return
        # Map cursor to scene/image coordinates
        scene_pt = self.mapToScene(event.pos())
        img_rect = self._pixmap_item.pixmap().rect()
        x = max(0, min(img_rect.width(), int(math.floor(scene_pt.x()))))
        y = max(0, min(img_rect.height(), int(math.floor(scene_pt.y()))))

        # Build tooltip text with HTML for guaranteed visibility
        coords = f"{x}, {y}"
        if dragging and self._selection_mode:
            origin_scene = self.mapToScene(self._origin)
            x1 = max(0, min(img_rect.width(), int(math.floor(min(origin_scene.x(), scene_pt.x())))))
            y1 = max(0, min(img_rect.height(), int(math.floor(min(origin_scene.y(), scene_pt.y())))))
            x2 = max(0, min(img_rect.width(), int(math.ceil(max(origin_scene.x(), scene_pt.x())))))
            y2 = max(0, min(img_rect.height(), int(math.ceil(max(origin_scene.y(), scene_pt.y())))))
            w = max(0, x2 - x1)
            h = max(0, y2 - y1)
            coords = f"{x}, {y}  •  Sel: ({x1}, {y1}) → ({x2}, {y2})  [{w}×{h}]"

        # Use HTML with explicit black text on yellow background
        text = f'<span style="background-color: #ffffcc; color: #000000; padding: 4px; border: 1px solid #888;">{coords}</span>'

        # Avoid spamming identical tooltips
        if text == self._last_tooltip_text and (x, y) == self._last_hover_coords:
            return
        self._last_tooltip_text = text
        self._last_hover_coords = (x, y)

        # Show tooltip near the cursor
        global_pos = self.mapToGlobal(event.pos())
        QToolTip.showText(global_pos, text, self)

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
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
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
        # Manual zoom disables auto-fit
        self._auto_fit_mode = False
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

    def fit(self, margin_percent: float = 5.0):
        """Fit image to view with optional margin.

        Args:
            margin_percent: Percentage of viewport to leave as margin (0-20).
        """
        if not self.scene() or self.sceneRect().isNull():
            return
        self.reset_zoom()
        try:
            if self._pixmap_item is not None:
                # Get the image bounds
                item_rect = self._pixmap_item.boundingRect()
                # Get viewport size
                viewport_rect = self.viewport().rect()

                # Calculate margins
                margin = max(0, min(20, margin_percent)) / 100.0
                effective_width = viewport_rect.width() * (1 - 2 * margin)
                effective_height = viewport_rect.height() * (1 - 2 * margin)

                # Calculate scale to fit within effective area
                scale_x = effective_width / item_rect.width()
                scale_y = effective_height / item_rect.height()
                scale = min(scale_x, scale_y)

                # Apply scale and center
                self.scale(scale, scale)
                self.centerOn(self._pixmap_item)
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
        # Only auto-fit on resize if auto-fit mode is enabled
        if self._auto_fit_mode and self._pixmap_item:
            self.fit()
        # Reposition hint overlay
        if not self._hint_dismissed and self._hint_label.isVisible():
            self._show_selection_hint()
        self.viewChanged.emit()

    def get_zoom_percent(self) -> float:
        """Get current zoom level as a percentage relative to image pixel size."""
        return self._zoom * 100.0

    def set_zoom_percent(self, percent: float):
        """Set zoom to an explicit percentage relative to image pixel size."""
        if not self._pixmap_item:
            return
        # Manual zoom disables auto-fit
        self._auto_fit_mode = False
        target_scale = max(0.01, percent / 100.0)
        if math.isclose(self._zoom, target_scale, rel_tol=1e-4, abs_tol=1e-4):
            return
        current_scale = self._zoom if self._zoom > 0 else 1.0
        factor = target_scale / current_scale
        self._apply_zoom(factor)

    def is_auto_fit_mode(self) -> bool:
        """Check if auto-fit mode is enabled."""
        return self._auto_fit_mode

    def set_auto_fit_mode(self, enabled: bool) -> None:
        """Enable or disable auto-fit mode."""
        self._auto_fit_mode = enabled
        if enabled and self._pixmap_item:
            self.fit()

    def _show_selection_hint(self) -> None:
        """Show the selection hint overlay if not dismissed and in selection mode."""
        if not self._hint_dismissed and self._selection_mode and self._pixmap_item:
            self._hint_label.adjustSize()
            # Center the hint in the viewport
            viewport_rect = self.viewport().rect()
            hint_width = self._hint_label.width()
            hint_height = self._hint_label.height()
            x = (viewport_rect.width() - hint_width) // 2
            y = (viewport_rect.height() - hint_height) // 2
            self._hint_label.move(x, y)
            self._hint_label.show()
            self._hint_label.raise_()
        else:
            self._hint_label.hide()
