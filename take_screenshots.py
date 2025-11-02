#!/usr/bin/env python3
"""Take screenshots of the app at different window sizes."""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

os.environ.setdefault("QT_MAC_APPLICATION_NAME", "Signature Extractor")
os.environ.setdefault("QT_MAC_WANTS_LAYER", "1")

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QScreen

from desktop_app.config import load_config
from desktop_app.state.session import SessionState
from desktop_app.api.client import ApiClient
from desktop_app.views.main_window import MainWindow


def take_screenshot(window, name: str, screenshots_dir: Path):
    """Take a screenshot of the window."""
    # Give Qt time to render
    QApplication.processEvents()
    time.sleep(0.5)

    # Grab the window
    pixmap = window.grab()

    # Save screenshot
    filepath = screenshots_dir / f"{name}.png"
    pixmap.save(str(filepath))
    print(f"Screenshot saved: {filepath}")


def main():
    app = QApplication(sys.argv)

    if sys.platform == "darwin":
        try:
            app.setStyle("macOS")
        except Exception:
            pass

    cfg = load_config()
    session = SessionState()
    client = ApiClient(cfg.api_base_url, session)

    win = MainWindow(client, session)
    win.show()

    # Create screenshots directory
    screenshots_dir = Path("screenshots_debug")
    screenshots_dir.mkdir(exist_ok=True)

    # Get screen geometry
    screen = app.primaryScreen()
    if screen:
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        print(f"Screen size: {screen_width}x{screen_height}")
    else:
        screen_width, screen_height = 1920, 1080

    def take_all_screenshots():
        """Take screenshots at different sizes."""
        # 1. Minimum size (1000x700)
        print("\n1. Testing minimum size (1000x700)")
        win.resize(1000, 700)
        take_screenshot(win, "01_minimum_1000x700", screenshots_dir)

        # 2. Small size (1200x800) - default
        print("\n2. Testing small size (1200x800)")
        win.resize(1200, 800)
        take_screenshot(win, "02_small_1200x800", screenshots_dir)

        # 3. Medium size (1400x900)
        print("\n3. Testing medium size (1400x900)")
        win.resize(1400, 900)
        take_screenshot(win, "03_medium_1400x900", screenshots_dir)

        # 4. Large size (1600x1000)
        print("\n4. Testing large size (1600x1000)")
        win.resize(1600, 1000)
        take_screenshot(win, "04_large_1600x1000", screenshots_dir)

        # 5. Full screen (or close to it)
        print(f"\n5. Testing full screen ({screen_width-100}x{screen_height-100})")
        win.resize(screen_width - 100, screen_height - 100)
        take_screenshot(win, "05_fullscreen", screenshots_dir)

        print(f"\n✅ All screenshots saved to {screenshots_dir}/")

        # Quit after screenshots
        QTimer.singleShot(500, app.quit)

    # Delay to let window fully initialize
    QTimer.singleShot(1000, take_all_screenshots)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
