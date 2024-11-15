# # # backend/app/database.py
# # from sqlalchemy import create_engine
# # from sqlalchemy.ext.declarative import declarative_base
# # from sqlalchemy.orm import sessionmaker
# # from app.config import settings
# # from typing import Generator
# # from sqlalchemy.orm import Session

# # SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# # engine = create_engine(SQLALCHEMY_DATABASE_URL)
# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# # Base = declarative_base()

# # def get_db() -> Generator[Session, None, None]:
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()



# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from app.config import settings

# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

# Create engine with logging and connection pooling
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # Log all SQL statements
    pool_pre_ping=True,  # Enable connection health checks
    pool_size=5,
    max_overflow=10
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def safe_commit(db):
    """Safely commit database changes with error handling."""
    try:
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database commit failed: {str(e)}")
        logger.error("Rolling back transaction")
        return False
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error during commit: {str(e)}")
        logger.error("Rolling back transaction")
        return False

def verify_db_connection():
    """Verify database connection is working."""
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        logger.info("Database connection verified successfully")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False
    finally:
        db.close()