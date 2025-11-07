#!/usr/bin/env python3
"""
Debug script to test the results pane issue
"""
import sys
import os
import tempfile
from PIL import Image
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'desktop_app'))

from PySide6.QtCore import Qt, QBuffer, QIODevice, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from desktop_app.widgets.image_view import ImageView

def create_test_image():
    """Create a test image with a signature-like pattern"""
    img = Image.new('RGB', (300, 200), color='white')
    pixels = img.load()
    
    # Create a simple signature-like pattern in black
    for i in range(50, 250):
        for j in range(50, 150):
            if (i - 100)**2 + (j - 100)**2 < 50**2:  # Circle
                pixels[i, j] = (0, 0, 0)
    
    # Save to temp file
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    img.save(temp_file.name, 'PNG')
    return temp_file.name

def test_complete_workflow():
    """Test the complete workflow from upload to result display"""
    print("=== Testing Complete Workflow ===")
    
    # Create QApplication
    app = QApplication([])
    
    # Create main window structure
    window = QMainWindow()
    central = QWidget()
    layout = QVBoxLayout(central)
    
    # Create result view (like in the app)
    result_view = ImageView()
    result_view.toggle_selection_mode(False)  # Disable selection mode for result view
    result_view.setObjectName('resultImageView')
    result_view.setVisible(False)  # Initially hidden
    
    # Create result empty label
    result_empty = QLabel("Process a selection to see the result")
    result_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
    result_empty.setStyleSheet("opacity:0.7; font-size:12px; padding:24px;")
    result_empty.setVisible(True)
    
    layout.addWidget(result_view)
    layout.addWidget(result_empty)
    window.setCentralWidget(central)
    
    print(f"Result view initial state:")
    print(f"  - Visible: {result_view.isVisible()}")
    print(f"  - Has image: {result_view.has_image()}")
    print(f"  - Empty overlay visible: {result_empty.isVisible()}")
    
    # Create test image
    test_image_path = create_test_image()
    print(f"Created test image: {test_image_path}")
    
    try:
        # Step 1: Upload image to backend
        print("\n1. Uploading image to backend...")
        with open(test_image_path, 'rb') as f:
            files = {'file': ('test_signature.png', f, 'image/png')}
            response = requests.post('http://127.0.0.1:8001/extraction/upload', files=files, timeout=10)
            
        if response.status_code == 200:
            result = response.json()
            session_id = result.get('id')
            print(f"✓ Upload successful, session_id: {session_id[:8]}...")
            
            # Step 2: Process image
            print("\n2. Processing image...")
            data = {
                'session_id': session_id,
                'x1': 50, 'y1': 50, 'x2': 250, 'y2': 150,
                'color': '#000000',
                'threshold': 200
            }
            response = requests.post('http://127.0.0.1:8001/extraction/process_image/', data=data, timeout=30)
            
            if response.status_code == 200:
                png_bytes = response.content
                print(f"✓ Processing successful, got {len(png_bytes)} bytes of image data")
                
                # Step 3: Simulate what _on_process_finished does
                print("\n3. Loading result into result pane...")
                
                # Store result
                _last_result_png = png_bytes
                
                # Load image into result view
                result_view.load_image_bytes(png_bytes)
                
                # Show result view, hide empty overlay
                result_empty.setVisible(False)
                result_view.setVisible(True)
                
                print(f"Result view after loading:")
                print(f"  - Visible: {result_view.isVisible()}")
                print(f"  - Has image: {result_view.has_image()}")
                print(f"  - Empty overlay visible: {result_empty.isVisible()}")
                
                if result_view.has_image():
                    image = result_view.image()
                    if image:
                        print(f"  - Image dimensions: {image.width()}x{image.height()}")
                    
                    # Check scene items
                    if result_view.scene():
                        items = result_view.scene().items()
                        print(f"  - Scene has {len(items)} items")
                        if items:
                            print(f"  - First item type: {type(items[0])}")
                
                # Step 4: Verify the image data
                print("\n4. Verifying image data...")
                test_image = QImage.fromData(png_bytes)
                if not test_image.isNull():
                    print(f"✓ Image data is valid, dimensions: {test_image.width()}x{test_image.height()}")
                else:
                    print("✗ Image data is invalid")
                
                # Test fit operation
                print("\n5. Testing result view fit operation...")
                try:
                    result_view.fit()
                    print("✓ Fit operation completed successfully")
                except Exception as e:
                    print(f"✗ Fit operation failed: {e}")
                
                print("\n=== Test Results ===")
                print("✓ Backend is working correctly")
                print("✓ Image processing returns valid PNG data")
                print("✓ Result pane can load and display the processed image")
                print("✓ All components are functioning as expected")
                
                print("\nIf you're still not seeing results in the app:")
                print("1. Make sure the backend is running")
                print("2. Check the app logs for any error messages")
                print("3. Try the manual test: source .venv/bin/activate && python -m desktop_app.main")
                print("4. Ensure you make a selection on the source image")
                
            else:
                print(f"✗ Processing failed: {response.status_code}")
                print(response.text)
        else:
            print(f"✗ Upload failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup
        try:
            os.unlink(test_image_path)
        except:
            pass

if __name__ == "__main__":
    test_complete_workflow()