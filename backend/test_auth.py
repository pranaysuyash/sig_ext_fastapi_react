import json
import logging

import pytest

pytestmark = pytest.mark.skip(reason="Requires running API service and database instance.")

pytest.importorskip("requests")
pytest.importorskip("psycopg2")

import requests
import psycopg2
from psycopg2.extras import RealDictCursor

from app.utils.auth import get_password_hash
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://127.0.0.1:8001"
TEST_USER = {
    "email": "test@example.com",
    "password": "test123456"
}

def update_test_user_password():
    """Update test user's password in database."""
    try:
        # Connect to database
        conn = psycopg2.connect(
            dbname=settings.DATABASE_NAME,
            user=settings.DATABASE_USERNAME,
            password=settings.DATABASE_PASSWORD,
            host=settings.DATABASE_HOSTNAME,
            port=settings.DATABASE_PORT,
            cursor_factory=RealDictCursor
        )
        
        # Create cursor
        with conn.cursor() as cur:
            # Generate new password hash
            hashed_password = get_password_hash(TEST_USER["password"])
            
            # Update user's password
            cur.execute(
                """
                UPDATE users 
                SET hashed_password = %s 
                WHERE email = %s 
                RETURNING id, email
                """,
                (hashed_password, TEST_USER["email"])
            )
            
            updated_user = cur.fetchone()
            if updated_user:
                logger.info(f"Updated password for user: {updated_user['email']}")
            else:
                logger.warning("No user found to update")
            
            conn.commit()
            
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def get_test_token():
    """Get authentication token for test user."""
    try:
        # First update the password
        update_test_user_password()
        
        # Attempt login
        login_data = {
            "username": TEST_USER["email"],
            "password": TEST_USER["password"]
        }
        
        logger.info(f"Attempting login for user: {TEST_USER['email']}")
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data=login_data
        )
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("access_token")
            
            if token:
                logger.info("Login successful!")
                logger.info(f"Access token: {token[:20]}...")
                
                # Save token to file
                with open("test_token.txt", "w") as f:
                    json.dump({"access_token": token}, f)
                logger.info("Token saved to test_token.txt")
                
                return token
            else:
                logger.error("No token in response")
                return None
        else:
            logger.error(f"Login failed: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Error getting test token: {str(e)}")
        return None

if __name__ == "__main__":
    get_test_token()
