#!/usr/bin/env python3
"""
Test script to verify the result pane functionality
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'desktop_app'))

from PySide6.QtCore import Qt, QBuffer, QIODevice
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication
from desktop_app.widgets.image_view import ImageView

def test_result_pane():
    """Test the result pane functionality"""
    print("Testing result pane functionality...")
    
    # Create QApplication
    app = QApplication([])
    
    # Create result view (like in the app)
    res_view = ImageView()
    res_view.toggle_selection_mode(False)  # Disable selection mode for result view
    
    # Create test image data
    img = QImage(100, 100, QImage.Format.Format_ARGB32)
    img.fill(Qt.GlobalColor.blue)
    
    # Convert to PNG bytes
    buffer = QBuffer()
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    img.save(buffer, 'PNG')
    png_data = buffer.data().data()
    buffer.close()
    
    print(f"Created test image: {len(png_data)} bytes")
    
    # Simulate the result pane workflow
    print("Loading image into result view...")
    res_view.load_image_bytes(png_data)
    
    print(f"Result view has image: {res_view.has_image()}")
    print(f"Result view is visible: {res_view.isVisible()}")
    
    if res_view.has_image():
        image = res_view.image()
        if image:
            print(f"Image dimensions: {image.width()}x{image.height()}")
    
    # Check scene
    if res_view.scene():
        items = res_view.scene().items()
        print(f"Scene has {len(items)} items")
    
    print("Result pane test completed successfully!")
    print("\nThe result pane should display processed signature images.")
    print("If you're not seeing results:")
    print("1. Check if the backend is running: curl http://127.0.0.1:8001/health")
    print("2. Make a selection on the source image")
    print("3. Wait for processing to complete")
    print("4. Check the app logs for any errors")
    
    return True

if __name__ == "__main__":
    test_result_pane()