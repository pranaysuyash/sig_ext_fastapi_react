
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from backend.app.config import settings
import logging

logger = logging.getLogger(__name__)

# Resolve database URL with optional SQLite fallback for desktop/local use
import os
ENV_DB_URL = os.getenv("DATABASE_URL")
if ENV_DB_URL:
    SQLALCHEMY_DATABASE_URL = ENV_DB_URL
else:
    # Default to Postgres via settings; users can flip to SQLite by setting DATABASE_URL
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}"
        f"@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
    )

# Ensure directory exists for SQLite file URLs like sqlite:///backend/data/app.db
connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    try:
        path = SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "", 1)
        if path:
            os.makedirs(os.path.dirname(path), exist_ok=True)
    except Exception as _e:
        logger.warning(f"Could not ensure SQLite directory: {_e}")
    connect_args = {"check_same_thread": False}

# Create engine (add pooling only when not using SQLite)
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False, connect_args=connect_args)
else:
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
