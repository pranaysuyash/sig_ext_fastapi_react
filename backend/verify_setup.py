import logging
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models.user import User
from backend.app.models.image import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_setup():
    db = SessionLocal()
    try:
        # Check users table
        users = db.query(User).all()
        logger.info(f"Found {len(users)} users")
        for user in users:
            logger.info(f"User: {user.email}, Plan: {user.subscription_plan}")

        # Check images table structure
        logger.info("\nVerifying images table structure...")
        image_columns = Image.__table__.columns
        for column in image_columns:
            logger.info(f"Column: {column.name}, Type: {column.type}")

        # Check database constraints
        logger.info("\nVerifying foreign key constraints...")
        for fk in Image.__table__.foreign_keys:
            logger.info(f"Foreign Key: {fk}")

        return True
    except Exception as e:
        logger.error(f"Verification failed: {str(e)}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    verify_setup()