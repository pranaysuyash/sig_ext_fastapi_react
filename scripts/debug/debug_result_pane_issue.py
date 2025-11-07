#!/usr/bin/env python3
"""
Debug script to trace the result pane visibility issue
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

def simulate_selection_changed():
    """Simulate the selection changed event"""
    print("=== Simulating Selection Changed Event ===")
    
    app = QApplication([])
    
    # Create result view and empty label like in the app
    res_view = ImageView()
    res_view.toggle_selection_mode(False)
    res_view.setVisible(False)
    
    from PySide6.QtWidgets import QLabel
    result_empty = QLabel('Process a selection to see the result')
    result_empty.setAlignment(Qt.AlignCenter)
    result_empty.setStyleSheet("opacity:0.7; font-size:12px; padding:24px;")
    result_empty.setVisible(True)
    
    print(f"After clear_selection (initial state):")
    print(f"  - res_view visible: {res_view.isVisible()}")
    print(f"  - result_empty visible: {result_empty.isVisible()}")
    print(f"  - res_view has image: {res_view.has_image()}")
    
    return res_view, result_empty

def simulate_processing(res_view, result_empty):
    """Simulate the processing workflow"""
    print("\n=== Simulating Processing Workflow ===")
    
    # Test backend
    try:
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            img = Image.new('RGB', (100, 100), color='white')
            img.save(f, 'PNG')
            temp_path = f.name
        
        print("1. Uploading image...")
        with open(temp_path, 'rb') as f:
            files = {'file': ('test.png', f, 'image/png')}
            response = requests.post('http://127.0.0.1:8001/extraction/upload', files=files, timeout=10)
            
        if response.status_code == 200:
            result = response.json()
            session_id = result.get('id')
            print(f"   ✓ Upload successful, session_id: {session_id[:8]}...")
            
            print("2. Processing image...")
            data = {
                'session_id': session_id,
                'x1': 10, 'y1': 10, 'x2': 90, 'y2': 90,
                'color': '#000000',
                'threshold': 200
            }
            response = requests.post('http://127.0.0.1:8001/extraction/process_image/', data=data, timeout=30)
            
            if response.status_code == 200:
                png_bytes = response.content
                print(f"   ✓ Processing successful, got {len(png_bytes)} bytes")
                
                # Simulate _on_process_finished
                print("\n3. Simulating _on_process_finished...")
                _last_result_png = png_bytes
                
                # Ensure preview panel is visible first
                preview_result_panel_visible = True
                result_label_visible = True
                
                # Load image
                print(f"   - Before load_image_bytes: res_view has_image = {res_view.has_image()}")
                res_view.load_image_bytes(png_bytes)
                print(f"   - After load_image_bytes: res_view has_image = {res_view.has_image()}")
                
                # Show result view, hide empty overlay
                print(f"   - Before visibility updates: res_view visible = {res_view.isVisible()}, result_empty visible = {result_empty.isVisible()}")
                
                result_empty.setVisible(False)
                res_view.setVisible(True)
                
                print(f"   - After visibility updates: res_view visible = {res_view.isVisible()}, result_empty visible = {result_empty.isVisible()}")
                
                # Force UI refresh
                res_view.update()
                res_view.viewport().update()
                
                # Fit the result to view
                try:
                    res_view.fit()
                    print("   - Fit operation completed")
                except Exception as e:
                    print(f"   - Fit operation failed: {e}")
                
                print("\n4. Final state check:")
                print(f"   - res_view visible: {res_view.isVisible()}")
                print(f"   - result_empty visible: {result_empty.isVisible()}")
                print(f"   - res_view has image: {res_view.has_image()}")
                
                if res_view.isVisible() and res_view.has_image() and not result_empty.isVisible():
                    print("   ✅ SUCCESS: Result should be visible!")
                else:
                    print("   ❌ FAILED: Result is not properly visible")
                    print("   This explains why you're seeing 'Process a selection' instead of results")
                
                return True
            else:
                print(f"   ✗ Processing failed: {response.status_code}")
                return False
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

def main():
    print("Debugging Result Pane Visibility Issue")
    print("=" * 50)
    
    # Step 1: Simulate initial state (after clear)
    res_view, result_empty = simulate_selection_changed()
    
    # Step 2: Simulate processing
    success = simulate_processing(res_view, result_empty)
    
    print("\n" + "=" * 50)
    if success:
        print("Test completed - check the results above")
    else:
        print("Test failed - backend issues detected")
    
    print("\nIf the result view is visible and has an image but you're still seeing")
    print("the 'Process a selection' message, the issue might be:")
    print("1. Layout/geometry issues in the main window")
    print("2. Z-index or layering problems")
    print("3. The result_empty widget is being shown on top of the result view")
    print("4. The preview_result_panel is not properly sized")
    
    return 0 if success else 1

if __name__ == "__main__":
    main()