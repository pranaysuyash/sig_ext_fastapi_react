import requests
import logging
import json
import os
from PIL import Image
import io

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8001")

def create_test_image():
    """Create a test image if none exists."""
    if not os.path.exists("test_image.jpg"):
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        img.save("test_image.jpg")
        logger.info("Created test image: test_image.jpg")

def test_upload(image_path="test_image.jpg"):
    try:
        # Create test image if needed
        create_test_image()
        
        # Load token
        try:
            with open("test_token.txt", "r") as f:
                token_data = json.load(f)
                token = token_data.get("access_token")
        except FileNotFoundError:
            logger.error("No token found. Please run test_auth.py first")
            return False

        # Check if image exists
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            return False

        # Prepare request
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        files = {
            'file': (
                'test_image.jpg',
                open(image_path, 'rb'),
                'image/jpeg'
            )
        }

        # Log request details
        logger.info("Sending upload request...")
        logger.info(f"URL: {BASE_URL}/extraction/upload")
        logger.info(f"File: {image_path}")
        logger.info("Headers:")
        logger.info(json.dumps({k: v for k, v in headers.items() if k != 'Authorization'}, indent=2))

        # Make request
        response = requests.post(
            f"{BASE_URL}/extraction/upload",
            headers=headers,
            files=files
        )

        # Log response
        logger.info(f"\nStatus Code: {response.status_code}")
        logger.info("Response Headers:")
        logger.info(json.dumps(dict(response.headers), indent=2))
        logger.info("\nResponse Body:")
        try:
            logger.info(json.dumps(response.json(), indent=2))
        except:
            logger.info(response.text)

        return response.status_code == 200

    except Exception as e:
        logger.error(f"Error during upload test: {str(e)}")
        return False
    finally:
        # Clean up
        if 'files' in locals():
            files['file'][1].close()

if __name__ == "__main__":
    test_upload()