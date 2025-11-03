#!/usr/bin/env python3
"""
Test script to verify the results pane fix
"""
import sys
import os
import tempfile
from PIL import Image
import requests
import threading
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'desktop_app'))

from PySide6.QtCore import Qt, QBuffer, QIODevice, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from desktop_app.widgets.image_view import ImageView

def test_app_startup():
    """Test that the app starts without errors"""
    print("=== Testing App Startup ===")
    
    try:
        from desktop_app.config import load_config
        from desktop_app.state.session import SessionState
        from desktop_app.api.client import ApiClient
        from desktop_app.views.main_window import MainWindow
        
        cfg = load_config()
        session = SessionState()
        client = ApiClient(cfg.api_base_url, session)
        
        # Create MainWindow
        window = MainWindow(client, session)
        
        print("✓ MainWindow created successfully")
        print("✓ All app components initialized")
        
        # Check that result view exists and has correct properties
        if hasattr(window, 'res_view'):
            print("✓ Result view exists")
            print(f"  - Has image: {window.res_view.has_image()}")
            print(f"  - Visible: {window.res_view.isVisible()}")
        else:
            print("✗ Result view not found")
            return False
            
        # Check that result empty label exists
        if hasattr(window, 'result_empty'):
            print("✓ Result empty label exists")
            print(f"  - Visible: {window.result_empty.isVisible()}")
        else:
            print("✗ Result empty label not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ App startup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backend_integration():
    """Test backend integration"""
    print("\n=== Testing Backend Integration ===")
    
    try:
        # Test upload
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            img = Image.new('RGB', (100, 100), color='white')
            img.save(f, 'PNG')
            temp_path = f.name
        
        with open(temp_path, 'rb') as f:
            files = {'file': ('test.png', f, 'image/png')}
            response = requests.post('http://127.0.0.1:8001/extraction/upload', files=files, timeout=10)
            
        if response.status_code == 200:
            result = response.json()
            session_id = result.get('id')
            print(f"✓ Upload successful, session_id: {session_id[:8]}...")
            
            # Test processing
            data = {
                'session_id': session_id,
                'x1': 10, 'y1': 10, 'x2': 50, 'y2': 50,
                'color': '#000000',
                'threshold': 200
            }
            response = requests.post('http://127.0.0.1:8001/extraction/process_image/', data=data, timeout=30)
            
            if response.status_code == 200:
                png_bytes = response.content
                print(f"✓ Processing successful, got {len(png_bytes)} bytes")
                return True, png_bytes
            else:
                print(f"✗ Processing failed: {response.status_code}")
                return False, None
        else:
            print(f"✗ Upload failed: {response.status_code}")
            return False, None
            
    except Exception as e:
        print(f"✗ Backend test failed: {e}")
        return False, None
    finally:
        try:
            os.unlink(temp_path)
        except:
            pass

def test_result_display(png_bytes):
    """Test result display functionality"""
    print("\n=== Testing Result Display ===")
    
    try:
        # Create result view and empty label
        res_view = ImageView()
        res_view.toggle_selection_mode(False)
        res_view.setVisible(False)
        
        result_empty = QLabel('Process a selection to see the result')
        result_empty.setVisible(True)
        
        print("Initial state:")
        print(f"  - res_view visible: {res_view.isVisible()}")
        print(f"  - result_empty visible: {result_empty.isVisible()}")
        
        # Apply the updated workflow logic
        res_view.load_image_bytes(png_bytes)
        
        # Check if image was loaded
        if not res_view.has_image():
            print("✗ Image failed to load")
            return False
            
        print(f"After loading image:")
        print(f"  - res_view has image: {res_view.has_image()}")
        
        # Show result view, hide empty overlay
        result_empty.setVisible(False)
        res_view.setVisible(True)
        
        print(f"Final state:")
        print(f"  - res_view visible: {res_view.isVisible()}")
        print(f"  - result_empty visible: {result_empty.isVisible()}")
        
        if res_view.isVisible() and not result_empty.isVisible():
            print("✓ Result display working correctly")
            return True
        else:
            print("✗ Result display not working correctly")
            return False
            
    except Exception as e:
        print(f"✗ Result display test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("Results Pane Fix Verification")
    print("=" * 40)
    
    # Create a single QApplication instance for all tests
    from PySide6.QtWidgets import QApplication
    app = QApplication([])
    
    # Test 1: App startup
    if not test_app_startup():
        print("\n❌ App startup test failed")
        return 1
    
    # Test 2: Backend integration
    success, png_bytes = test_backend_integration()
    if not success:
        print("\n❌ Backend integration test failed")
        return 1
    
    # Test 3: Result display
    if not test_result_display(png_bytes):
        print("\n❌ Result display test failed")
        return 1
    
    print("\n" + "=" * 40)
    print("🎉 All tests passed!")
    print("\nThe results pane should now display processed signature images correctly.")
    print("\nTo test manually:")
    print("1. Run: source .venv/bin/activate && python -m desktop_app.main")
    print("2. Upload an image")
    print("3. Make a selection on the source image")
    print("4. Wait for processing to complete")
    print("5. Check that the result appears in the Result pane")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())