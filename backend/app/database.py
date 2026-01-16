
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from backend.app.config import settings
import logging

logger = logging.getLogger(__name__)

import os
ENV_DB_URL = os.getenv("DATABASE_URL")
if ENV_DB_URL:
    SQLALCHEMY_DATABASE_URL = ENV_DB_URL
else:
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

if not SQLALCHEMY_DATABASE_URL.startswith("postgresql://") and not SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    raise ValueError(
        "Unsupported DATABASE_URL scheme. This backend requires PostgreSQL. "
        "Set DATABASE_URL to a postgresql://... URL."
    )

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
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
        db.execute(text("SELECT 1"))
        logger.info("Database connection verified successfully")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False
    finally:
        db.close()
