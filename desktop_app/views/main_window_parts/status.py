from __future__ import annotations

import math
import sys
from PySide6.QtCore import QEvent, QObject, QTimer
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QLabel, QStatusBar


class PaneClickEventFilter(QObject):
    """Event filter to intercept mouse press events and track pane activation."""

    def __init__(self, pane_name: str, callback):
        super().__init__()
        self.pane_name = pane_name
        self.callback = callback

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            self.callback(self.pane_name)
        return super().eventFilter(obj, event)


class PaneStatusMixin:
    """Status bar, pane focus, and coordinate display helpers."""

    def _init_status_bar(self) -> None:
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready", 2000)
        if sys.platform == "darwin":
            self.status_bar.setStyleSheet(
                "QStatusBar { background-color: rgba(255, 255, 255, 235);"
                " border-top: 1px solid rgba(0, 0, 0, 20); }"
            )

        self.backend_status_label = QLabel("Backend: checking…")
        self.backend_status_label.setStyleSheet("color: #a37f00; padding: 2px 8px;")
        self.status_bar.addPermanentWidget(self.backend_status_label)

        mono_style = (
            "color: #666; padding: 2px 8px; font-family: 'Menlo', 'Roboto Mono',"
            " 'Fira Code', 'Courier New', monospace; font-size: 11px;"
        )
        self.viewport_size_label = QLabel("Viewport: –")
        self.viewport_size_label.setStyleSheet(mono_style)
        self.viewport_size_label.setToolTip("Viewport widget size (can change on window resize)")
        self.status_bar.addPermanentWidget(self.viewport_size_label)

        self.image_size_label = QLabel("Image: –")
        self.image_size_label.setStyleSheet(mono_style)
        self.image_size_label.setToolTip("Image resolution for the active pane")
        self.status_bar.addPermanentWidget(self.image_size_label)

        self.view_coords_label = QLabel("Visible: –")
        self.view_coords_label.setStyleSheet(mono_style)
        self.view_coords_label.setToolTip("Visible image coordinates in pixel space")
        self.status_bar.addPermanentWidget(self.view_coords_label)

        self.selection_coords_label = QLabel("Selection: –")
        self.selection_coords_label.setStyleSheet(mono_style)
        self.selection_coords_label.setToolTip("Selected area coordinates in image pixel space")
        self.status_bar.addPermanentWidget(self.selection_coords_label)

        self.zoom_label = QLabel("Zoom: –")
        self.zoom_label.setStyleSheet(mono_style)
        self.zoom_label.setToolTip("Current zoom level of active pane")
        self.status_bar.addPermanentWidget(self.zoom_label)

        self.rotation_label = QLabel("Rotation: –")
        self.rotation_label.setStyleSheet(mono_style)
        self.rotation_label.setToolTip("Rotation applied to the active pane view")
        self.status_bar.addPermanentWidget(self.rotation_label)

        self.session_id_label = QLabel("No session")
        self.session_id_label.setStyleSheet("color: #666; padding: 2px 8px;")
        self.status_bar.addPermanentWidget(self.session_id_label)

    def _install_pane_click_filter(self, view, pane_name):
        """Install event filter to track pane activation on mouse press."""
        event_filter = PaneClickEventFilter(pane_name, self._on_pane_clicked)
        view.installEventFilter(event_filter)
        # Store the filter to prevent garbage collection
        if not hasattr(self, '_pane_event_filters'):
            self._pane_event_filters = []
        self._pane_event_filters.append(event_filter)

    def _get_active_view(self):
        return {
            "source": getattr(self, "src_view", None),
            "preview": getattr(self, "preview_view", None),
            "result": getattr(self, "res_view", None),
        }.get(getattr(self, "_active_pane", "source"))

    def _on_pane_clicked(self, pane: str) -> None:
        if getattr(self, "_active_pane", None) != pane:
            self._active_pane = pane
            self._update_pane_borders()
            self._update_view_actions_enabled()
            self._update_coordinate_display()
            if hasattr(self, "status_bar"):
                self.status_bar.showMessage(f"Active pane: {pane.capitalize()}", 2000)

    def _update_coordinate_display(self) -> None:
        active_view = self._get_active_view()

        if not active_view or not active_view.has_image():
            self.viewport_size_label.setText("Viewport: –")
            self.image_size_label.setText("Image: –")
            self.view_coords_label.setText("Visible: –")
            self.zoom_label.setText("Zoom: –")
            self.rotation_label.setText("Rotation: –")
            self._set_zoom_combo_display("—")
            if getattr(self, "_active_pane", "source") != "source" or not getattr(self, "src_view", None) or not self.src_view.has_image():
                self.selection_coords_label.setText("Selection: –")
            return

        viewport_rect = active_view.viewport().rect()
        viewport_w = viewport_rect.width()
        viewport_h = viewport_rect.height()
        self.viewport_size_label.setText(f"Viewport: {viewport_w}×{viewport_h}")

        if active_view._pixmap_item:
            pix = active_view._pixmap_item.pixmap()
            self.image_size_label.setText(f"Image: {pix.width()}×{pix.height()}")
        else:
            self.image_size_label.setText("Image: –")

        tl_scene = active_view.mapToScene(viewport_rect.topLeft())
        br_scene = active_view.mapToScene(viewport_rect.bottomRight())

        if active_view._pixmap_item:
            img_rect = active_view._pixmap_item.pixmap().rect()
            img_tl_viewport = active_view.mapFromScene(0, 0)
            img_br_viewport = active_view.mapFromScene(img_rect.width(), img_rect.height())

            view_x1 = max(0, min(int(tl_scene.x()), img_rect.width()))
            view_y1 = max(0, min(int(tl_scene.y()), img_rect.height()))
            view_x2 = max(0, min(int(br_scene.x()), img_rect.width()))
            view_y2 = max(0, min(int(br_scene.y()), img_rect.height()))

            self.view_coords_label.setText(
                f"Visible: @({int(img_tl_viewport.x())},{int(img_tl_viewport.y())})→"
                f"({int(img_br_viewport.x())},{int(img_br_viewport.y())}) "
                f"shows ({view_x1},{view_y1})→({view_x2},{view_y2})"
            )
        else:
            self.view_coords_label.setText("Visible: –")

        zoom_value = active_view._zoom * 100.0
        zoom_text = f"{int(round(zoom_value))}%" if math.isclose(zoom_value, round(zoom_value), abs_tol=0.1) else f"{zoom_value:.1f}%"
        self.zoom_label.setText(f"Zoom: {zoom_text}")
        self._set_zoom_combo_display(zoom_text)

        rotation_deg = getattr(active_view, "_rotation", 0.0)
        self.rotation_label.setText(f"Rotation: {rotation_deg:.1f}°")

        source_view = getattr(self, "src_view", None)
        if getattr(self, "_active_pane", "source") == "source":
            self._update_selection_label_from_source(source_view)
        else:
            if source_view and source_view.has_image():
                self._update_selection_label_from_source(source_view)
            else:
                self.selection_coords_label.setText("Selection: –")

    def _update_selection_label_from_source(self, source_view) -> None:
        if not source_view:
            self.selection_coords_label.setText("Selection: –")
            return
        x1, y1, x2, y2 = source_view.selected_rect_image_coords()
        if x1 == 0 and y1 == 0 and x2 == 0 and y2 == 0:
            self.selection_coords_label.setText("Selection: –")
            return
        w, h = x2 - x1, y2 - y1
        self.selection_coords_label.setText(f"Selection: ({x1},{y1})→({x2},{y2}) [{w}×{h}]")

    def _set_zoom_combo_display(self, text: str) -> None:
        zoom_combo = getattr(self, "zoom_combo", None)
        if not zoom_combo:
            return
        self._updating_zoom_combo = True
        try:
            zoom_combo.setEditText(text)
        finally:
            self._updating_zoom_combo = False

    def _update_pane_borders(self) -> None:
        palette = self.palette()
        accent = palette.color(QPalette.ColorRole.Highlight).name()
        base_bg = palette.color(QPalette.ColorRole.Base).name()
        border_muted = palette.color(QPalette.ColorRole.Mid).name()
        inactive_text = palette.color(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText).name()

        active_label_style = f"font-weight: 600; color: {accent}; padding: 4px;"
        inactive_label_style = f"font-weight: normal; color: {inactive_text}; padding: 4px;"
        # IMPORTANT: No background-color or border-radius on QGraphicsView - causes crashes
        active_view_style = f"border: 2px solid {accent};"
        inactive_view_style = f"border: 1px solid {border_muted};"

        if getattr(self, "_active_pane", "source") == "source":
            self.src_view.setStyleSheet(active_view_style)
            self.source_label.setStyleSheet(active_label_style)
        else:
            self.src_view.setStyleSheet(inactive_view_style)
            self.source_label.setStyleSheet(inactive_label_style)

        if getattr(self, "_active_pane", "source") == "preview":
            self.preview_view.setStyleSheet(active_view_style)
            self.preview_label.setStyleSheet(active_label_style)
        else:
            self.preview_view.setStyleSheet(inactive_view_style)
            self.preview_label.setStyleSheet(inactive_label_style)

        # IMPORTANT: No background-color or border-radius on QGraphicsView - causes crashes
        res_active_style = f"border: 2px solid {accent};"
        res_inactive_style = f"border: 1px solid {border_muted};"

        if getattr(self, "_active_pane", "source") == "result":
            self.res_view.setStyleSheet(res_active_style)
            self.result_label.setStyleSheet(active_label_style)
        else:
            self.res_view.setStyleSheet(res_inactive_style)
            self.result_label.setStyleSheet(inactive_label_style)

    def defer_coordinate_update(self) -> None:
        """Trigger coordinate update after the event loop settles."""
        QTimer.singleShot(0, self._update_coordinate_display)


__all__ = ["PaneStatusMixin"]
