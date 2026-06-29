import logging
import base64
import binascii
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping, Optional

import bcrypt
from jose import jwt

from backend.app.config import settings

logger = logging.getLogger(__name__)

_FALLBACK_ALGORITHM = "pbkdf2_sha256"
_FALLBACK_ITERATIONS = 390000
_FALLBACK_MIN_ITERATIONS = 100000
_FALLBACK_MAX_ITERATIONS = 1000000
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


def _hash_with_bcrypt(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _verify_with_bcrypt(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except Exception:
        logger.exception("bcrypt verification failed.")
        return False


def _is_fallback_hash(hashed_password: str) -> bool:
    return hashed_password.startswith(f"{_FALLBACK_ALGORITHM}$")


def _verify_fallback_password(plain_password: str, hashed_password: str) -> bool:
    try:
        algorithm, iter_str, salt_b64, digest_b64 = hashed_password.split("$", 3)
        if algorithm != _FALLBACK_ALGORITHM:
            return False
        iterations = int(iter_str)
        if iterations < _FALLBACK_MIN_ITERATIONS or iterations > _FALLBACK_MAX_ITERATIONS:
            return False
        salt = _decode_bytes(salt_b64)
        expected_digest = _decode_bytes(digest_b64)
    except (ValueError, binascii.Error):
        return False

    candidate_digest = _pbkdf2_hash(plain_password, salt, iterations)
    return hmac.compare_digest(candidate_digest, expected_digest)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    if _is_fallback_hash(hashed_password):
        return _verify_fallback_password(plain_password, hashed_password)

    if hashed_password.startswith("$2"):
        return _verify_with_bcrypt(plain_password, hashed_password)

    return False

def get_password_hash(password: str) -> str:
    """Generate password hash."""
    try:
        return _hash_with_bcrypt(password)
    except Exception:
        logger.exception("bcrypt hashing failed; falling back to PBKDF2.")

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

def create_access_token(data: Mapping[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT token."""
    try:
        to_encode = dict(data)
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode["exp"] = expire
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt
    except Exception:
        logger.exception("Token creation failed")
        raise
