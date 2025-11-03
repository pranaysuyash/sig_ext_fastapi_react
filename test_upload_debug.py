#!/usr/bin/env python3
"""
Debug script to test if upload is working.
Run this to verify backend connectivity and upload functionality.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from desktop_app.api.client import ApiClient
from desktop_app.state.session import SessionState

def main():
    print("=== Upload Debug Test ===\n")

    # Create session and client
    session = SessionState()
    client = ApiClient("http://localhost:8001", session)

    print(f"1. Testing backend health...")
    try:
        health = client.health_check()
        print(f"   ✓ Backend is healthy: {health}")
    except Exception as e:
        print(f"   ✗ Backend health check failed: {e}")
        return

    # Find a test image
    test_image = None
    for path in ["uploads/images/*.png", "test.html"]:
        import glob
        files = glob.glob(path)
        if files:
            # Look for actual image files
            for f in files:
                if f.endswith(('.png', '.jpg', '.jpeg')):
                    test_image = f
                    break
            if test_image:
                break

    if not test_image:
        print(f"\n   ✗ No test image found. Please provide a .png or .jpg file path.")
        return

    print(f"\n2. Testing upload with image: {test_image}")
    try:
        result = client.upload_image(test_image)
        print(f"   ✓ Upload successful!")
        print(f"   Response: {result}")
        print(f"   Session ID from response: {result.get('id')}")
        print(f"   Session ID in session object: {session.session_id}")
    except Exception as e:
        print(f"   ✗ Upload failed: {e}")
        import traceback
        traceback.print_exc()
        return

    print(f"\n3. Summary:")
    print(f"   - Backend: Online ✓")
    print(f"   - Upload: Working ✓")
    print(f"   - Session ID: {session.session_id} ✓")
    print(f"\n   The backend and upload are working correctly.")
    print(f"   The issue must be in the desktop app's AsyncRunner or signal connections.")

if __name__ == "__main__":
    main()
