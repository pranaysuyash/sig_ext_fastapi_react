"""Standalone utility functions and helpers for the extraction tab.

This module contains code that has no dependency on ``self`` or any mixin
state.  Everything here is importable from any module without circular
import risk.
"""

from __future__ import annotations

import sys
from typing import Optional

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPushButton, QSizePolicy, QWidget

# ---------------------------------------------------------------------------
# Async helpers
# ---------------------------------------------------------------------------

class AsyncRunner(QObject):
    """Run a callable in the global thread pool and emit its result."""

    finished = Signal(object)
    error = Signal(Exception)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(e)


def run_async(func, *args, **kwargs):
    """Run *func* in the thread pool and return a future-like object."""

    runner = AsyncRunner(func, *args, **kwargs)

    class Future:
        def __init__(self, runner):
            self.runner = runner
            self._result = None
            self._error = None
            self._finished = False
            runner.finished.connect(self._on_finished)
            runner.error.connect(self._on_error)

        def _on_finished(self, result):
            self._result = result
            self._finished = True

        def _on_error(self, error):
            self._error = error
            self._finished = True

        def result(self):
            if self._error:
                raise self._error
            return self._result

        def isFinished(self):
            return self._finished

    future = Future(runner)

    thread_pool = QThreadPool.globalInstance()
    runnable = QRunnable.create(lambda: runner.run())
    runnable.setAutoDelete(True)
    thread_pool.start(runnable)

    return future


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def _rgba(color: QColor) -> str:
    """Return a Qt stylesheet-friendly RGBA string for *color*."""
    return f"rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()})"


# ---------------------------------------------------------------------------
# Button factory
# ---------------------------------------------------------------------------

def _create_button(
    text: str = "",
    parent: QWidget = None,
    *,
    use_modern_mac: bool = None,
    primary: bool = False,
    destructive: bool = False,
    color: str = 'blue',
    compact: bool = False,
) -> QPushButton:
    """Create a platform-appropriate button.

    On macOS the function tries to use ``ModernMacButton`` (glassmorphism).
    Falls back to a standard ``QPushButton`` on other platforms or if the
    custom widget is unavailable.
    """
    if use_modern_mac is None:
        use_modern_mac = sys.platform == "darwin"

    resolved_color = 'red' if destructive and color == 'blue' else color

    if use_modern_mac:
        try:
            from desktop_app.widgets.modern_mac_button import ModernMacButton
            btn = ModernMacButton(
                text, parent,
                primary=primary,
                color=resolved_color,
                glass=True,
                compact=compact,
            )
            if destructive:
                btn.setProperty("destructive", True)
            return btn
        except (NameError, TypeError):
            pass

    btn = QPushButton(text, parent)
    if primary:
        btn.setProperty("primary", True)
    if destructive:
        btn.setProperty("destructive", True)
    if compact:
        btn.setProperty("compact", True)
    return btn


# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------

def _clear_layout(layout) -> None:
    """Remove and delete all items from *layout*."""
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()
        else:
            sub = item.layout()
            if sub:
                _clear_layout(sub)
