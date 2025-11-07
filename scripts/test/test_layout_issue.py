#!/usr/bin/env python3
"""
Test to identify the exact layout issue with result pane
"""
import sys
import os
sys.path.insert(0, 'desktop_app')

from PySide6.QtCore import Qt, QBuffer, QIODevice
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from desktop_app.widgets.image_view import ImageView

def test_result_layout():
    """Test the exact layout structure used in the app"""
    print("=== Testing Result Layout Structure ===")
    
    app = QApplication([])
    
    # Create main window
    window = QMainWindow()
    central = QWidget()
    layout = QVBoxLayout(central)
    
    # Create result_container (like in the app)
    result_container = QWidget()
    result_layout = QVBoxLayout(result_container)
    result_layout.setContentsMargins(0, 0, 0, 0)
    
    # Create result_label
    result_label = QLabel("Result")
    result_layout.addWidget(result_label)
    
    # Create res_view
    res_view = ImageView()
    res_view.setObjectName("resultImageView")
    res_view.setSizePolicy(Qt.SizePolicy.Expanding, Qt.SizePolicy.Expanding)
    res_view.toggle_selection_mode(False)
    res_view.setVisible(False)
    result_layout.addWidget(res_view)
    
    # Create result_empty (ADDED AFTER res_view - this is the key!)
    result_empty = QLabel("Process a selection to see the result")
    result_empty.setAlignment(Qt.AlignCenter)
    result_empty.setStyleSheet("opacity:0.7; font-size:12px; padding:24px;")
    result_empty.setVisible(True)
    result_layout.addWidget(result_empty)  # This is added AFTER res_view!
    
    # Add to main layout
    layout.addWidget(result_container, 1)
    window.setCentralWidget(central)
    
    print("Layout structure created:")
    print("  - result_container")
    print("  - result_label")
    print("  - res_view (added first)")
    print("  - result_empty (added after res_view)")
    
    print(f"\nInitial state:")
    print(f"  - res_view visible: {res_view.isVisible()}")
    print(f"  - result_empty visible: {result_empty.isVisible()}")
    print(f"  - res_view z-order index: {result_layout.indexOf(res_view)}")
    print(f"  - result_empty z-order index: {result_layout.indexOf(result_empty)}")
    
    # Test image loading
    img = QImage(50, 50, QImage.Format.Format_ARGB32)
    img.fill(Qt.GlobalColor.blue)
    
    buffer = QBuffer()
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    img.save(buffer, 'PNG')
    png_bytes = buffer.data().data()
    buffer.close()
    
    print(f"\nLoading image ({len(png_bytes)} bytes)...")
    res_view.load_image_bytes(png_bytes)
    
    print(f"After loading image:")
    print(f"  - res_view has image: {res_view.has_image()}")
    print(f"  - res_view visible: {res_view.isVisible()}")
    
    # Now simulate the result display logic
    print(f"\nApplying visibility changes...")
    result_empty.setVisible(False)
    res_view.setVisible(True)
    
    print(f"After visibility changes:")
    print(f"  - res_view visible: {res_view.isVisible()}")
    print(f"  - result_empty visible: {result_empty.isVisible()}")
    
    # Check geometry
    print(f"\nGeometry information:")
    print(f"  - res_view geometry: {res_view.geometry()}")
    print(f"  - result_empty geometry: {result_empty.geometry()}")
    print(f"  - result_container geometry: {result_container.geometry()}")
    
    # Check if they overlap
    res_geo = res_view.geometry()
    empty_geo = result_empty.geometry()
    
    if res_geo.intersects(empty_geo):
        print(f"\n⚠️  OVERLAP DETECTED: res_view and result_empty geometries overlap!")
        print(f"   This means result_empty is visible ON TOP of res_view")
        print(f"   Even though result_empty.setVisible(False) was called, the layout might not be updating properly")
    else:
        print(f"\n✓ No overlap detected")
    
    print(f"\n=== KEY FINDING ===")
    print(f"The issue is that result_empty is added to the layout AFTER res_view,")
    print(f"so it appears on TOP of res_view in the z-order.")
    print(f"When both widgets are visible, result_empty covers res_view completely!")
    print(f"")
    print(f"Even when we call result_empty.setVisible(False), there might be")
    print(f"layout/drawing issues that prevent res_view from showing properly.")

if __name__ == "__main__":
    test_result_layout()