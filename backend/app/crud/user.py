import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.schemas.user import UserCreate
from backend.app.utils.auth import get_password_hash, verify_password

logger = logging.getLogger(__name__)


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Return a user by email, or None when no match exists."""
    normalized_email = _normalize_email(email)
    return db.query(User).filter(User.email == normalized_email).first()


def create_user(db: Session, user: UserCreate) -> User | None:
    """Create a user or return None if the email is already registered."""
    normalized_email = _normalize_email(user.email)

    if get_user_by_email(db, normalized_email):
        logger.warning("Create user rejected: duplicate email")
        return None

    db_user = User(
        email=normalized_email,
        hashed_password=get_password_hash(user.password),
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info("Created user %s", db_user.id)
        return db_user
    except IntegrityError:
        db.rollback()
        logger.warning("Create user rejected: duplicate email")
        return None
    except Exception:
        db.rollback()
        logger.exception("Error creating user")
        raise


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Validate credentials and return the matching user when successful."""
    user = get_user_by_email(db, email)
    if not user:
        logger.warning("Authentication failed")
        return None

    if not verify_password(password, user.hashed_password):
        logger.warning("Authentication failed")
        return None

    logger.info("User authenticated successfully: %s", user.id)
    return user
