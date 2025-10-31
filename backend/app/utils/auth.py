import logging
import base64
import binascii
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

from backend.app.config import settings

try:
    from passlib.context import CryptContext
except ImportError:  # pragma: no cover - exercised when passlib unavailable
    CryptContext = None  # type: ignore[attr-defined]

logger = logging.getLogger(__name__)

_FALLBACK_ALGORITHM = "pbkdf2_sha256"
_FALLBACK_ITERATIONS = 390000
_FALLBACK_SALT_BYTES = 16


def _encode_bytes(raw: bytes) -> str:
    """URL-safe base64 without padding; easier to persist in text fields."""
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _decode_bytes(data: str) -> bytes:
    """Decode padding-less base64 segment."""
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _pbkdf2_hash(password: str, salt: bytes, iterations: int) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") if CryptContext else None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    if pwd_context:
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:  # pragma: no cover - handled gracefully below
            logger.exception("Passlib verification failed; falling back to PBKDF2.")

    try:
        algorithm, iter_str, salt_b64, digest_b64 = hashed_password.split("$", 3)
        if algorithm != _FALLBACK_ALGORITHM:
            return False
        iterations = int(iter_str)
        salt = _decode_bytes(salt_b64)
        expected_digest = _decode_bytes(digest_b64)
    except (ValueError, binascii.Error):
        return False

    candidate_digest = _pbkdf2_hash(plain_password, salt, iterations)
    return hmac.compare_digest(candidate_digest, expected_digest)

def get_password_hash(password: str) -> str:
    """Generate password hash."""
    if pwd_context:
        return pwd_context.hash(password)

    salt = secrets.token_bytes(_FALLBACK_SALT_BYTES)
    digest = _pbkdf2_hash(password, salt, _FALLBACK_ITERATIONS)
    return "$".join(
        (
            _FALLBACK_ALGORITHM,
            str(_FALLBACK_ITERATIONS),
            _encode_bytes(salt),
            _encode_bytes(digest),
        )
    )

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT token."""
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.JWT_SECRET, 
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error(f"Token creation failed: {str(e)}")
        raise
