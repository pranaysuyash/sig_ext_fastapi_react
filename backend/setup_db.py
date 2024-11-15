import logging
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine, Base
from app.models.user import User
from app.models.image import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    try:
        logger.info("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        
        logger.info("Creating all tables...")
        Base.metadata.create_all(bind=engine)
        
        logger.info("Database setup completed successfully!")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database error during setup: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during setup: {str(e)}")
        return False

if __name__ == "__main__":
    setup_database()