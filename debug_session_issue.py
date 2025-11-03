#!/usr/bin/env python3
"""
Debug script to test the session ID issue
"""
import sys
import os
import tempfile
from PIL import Image
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'desktop_app'))

from PySide6.QtCore import Qt, QBuffer, QIODevice
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication
from desktop_app.widgets.image_view import ImageView
from desktop_app.api.client import ApiClient
from desktop_app.state.session import SessionState
from desktop_app.config import load_config

def test_session_workflow():
    """Test the complete session workflow"""
    print("=== Testing Session ID Workflow ===")
    
    # Test 1: Backend upload response
    print("\n1. Testing backend upload response...")
    
    # Create test image
    img = Image.new('RGB', (100, 100), color='white')
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        img.save(f, 'PNG')
        temp_path = f.name
    
    try:
        with open(temp_path, 'rb') as f:
            files = {'file': ('test.png', f, 'image/png')}
            response = requests.post('http://127.0.0.1:8001/extraction/upload', files=files, timeout=10)
            
        if response.status_code == 200:
            payload = response.json()
            print(f"   ✓ Backend response: {payload}")
            
            # Test the exact extraction logic
            session_id = payload.get("id") or payload.get("session_id") or payload.get("image_id")
            print(f"   ✓ Session ID extracted: {session_id}")
        else:
            print(f"   ✗ Upload failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ✗ Test failed: {e}")
        return False
    finally:
        try:
            os.unlink(temp_path)
        except:
            pass
    
    # Test 2: Session state initialization
    print("\n2. Testing session state...")
    
    app = QApplication([])
    
    try:
        cfg = load_config()
        session = SessionState()
        client = ApiClient(cfg.api_base_url, session)
        
        print(f"   Initial session_id: {repr(session.session_id)} (type: {type(session.session_id)})")
        print(f"   bool(session_id): {bool(session.session_id)}")
        
        # Set session ID like the app does
        session.session_id = session_id
        print(f"   After setting: session_id: {repr(session.session_id)}")
        print(f"   bool(session_id): {bool(session.session_id)}")
        
        # Test condition that would block preview
        if not session.session_id:
            print("   ✗ Session ID is falsy - this would block preview!")
        else:
            print("   ✓ Session ID is set - preview should work")
        
    except Exception as e:
        print(f"   ✗ Session test failed: {e}")
        return False
    
    # Test 3: Main window initialization
    print("\n3. Testing MainWindow session label...")
    
    try:
        from desktop_app.views.main_window import MainWindow
        window = MainWindow(client, session)
        
        print(f"   Window has session_id_label: {hasattr(window, 'session_id_label')}")
        if hasattr(window, 'session_id_label'):
            initial_text = window.session_id_label.text()
            print(f"   Initial session_id_label text: '{initial_text}'")
            
            # Update like the app does
            window.session_id_label.setText(f"Session: {session_id[:8]}...")
            updated_text = window.session_id_label.text()
            print(f"   Updated session_id_label text: '{updated_text}'")
        else:
            print("   ✗ session_id_label not found!")
            return False
            
    except Exception as e:
        print(f"   ✗ MainWindow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 50)
    print("✅ Session workflow test completed")
    print("If session ID shows as 'No session' in the app, check:")
    print("1. Backend upload is successful")
    print("2. session_id_label is properly initialized")
    print("3. _on_upload_finished is called correctly")
    print("4. No exceptions are thrown during upload processing")
    
    return True

if __name__ == "__main__":
    success = test_session_workflow()
    sys.exit(0 if success else 1)