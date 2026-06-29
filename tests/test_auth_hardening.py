from __future__ import annotations

import atexit
import asyncio
import os
import tempfile
import time
from datetime import timedelta
from uuid import UUID, uuid4

os.environ.setdefault("JWT_SECRET", "a" * 32)
_db_fd, _db_path = tempfile.mkstemp(prefix="signkit-auth-tests-", suffix=".sqlite3")
os.close(_db_fd)
os.environ["DATABASE_URL"] = f"sqlite:///{_db_path}"
atexit.register(lambda: os.path.exists(_db_path) and os.unlink(_db_path))

import pytest
import bcrypt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import sessionmaker

from backend.app.config import settings
from backend.app.database import Base, engine
from backend.app.models.user import User
from backend.app.routers.auth import login, register, router as auth_router
from backend.app.schemas.user import UserCreate
from backend.app.utils.auth import (
    _FALLBACK_ALGORITHM,
    _FALLBACK_ITERATIONS,
    _FALLBACK_MAX_ITERATIONS,
    _FALLBACK_SALT_BYTES,
    _encode_bytes,
    _pbkdf2_hash,
    create_access_token,
    get_password_hash,
    verify_password,
)
from backend.app.utils.dependencies import get_current_user

Base.metadata.create_all(bind=engine)


@pytest.fixture()
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection, autoflush=False, autocommit=False)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


def test_password_hash_round_trip():
    password = "correct horse battery staple"
    hashed = get_password_hash(password)

    assert hashed.startswith("$2")
    assert verify_password(password, hashed) is True
    assert verify_password("wrong-password", hashed) is False


def test_user_create_password_max_length_enforced():
    with pytest.raises(ValidationError):
        UserCreate(email="user@example.com", password="x" * 73)


def test_bcrypt_hash_format_verifies():
    password = "correct horse battery staple"
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    assert hashed.startswith("$2")
    assert verify_password(password, hashed) is True
    assert verify_password("wrong-password", hashed) is False


def test_get_password_hash_falls_back_to_pbkdf2(monkeypatch):
    def _raise(*args, **kwargs):
        raise ValueError("bcrypt unavailable")

    monkeypatch.setattr("backend.app.utils.auth.bcrypt.hashpw", _raise)
    password = "correct horse battery staple"
    hashed = get_password_hash(password)

    assert hashed.startswith("pbkdf2_sha256$")
    assert verify_password(password, hashed) is True


def test_fallback_pbkdf2_round_trip():
    password = "correct horse battery staple"
    salt = b"0" * _FALLBACK_SALT_BYTES
    digest = _pbkdf2_hash(password, salt, _FALLBACK_ITERATIONS)
    hashed = "$".join(
        (
            _FALLBACK_ALGORITHM,
            str(_FALLBACK_ITERATIONS),
            _encode_bytes(salt),
            _encode_bytes(digest),
        )
    )

    assert verify_password(password, hashed) is True
    assert verify_password("wrong-password", hashed) is False


def test_fallback_pbkdf2_rejects_malformed_and_excessive_iterations():
    password = "correct horse battery staple"
    salt = b"1" * _FALLBACK_SALT_BYTES
    digest = _pbkdf2_hash(password, salt, _FALLBACK_ITERATIONS)

    malformed_hash = f"{_FALLBACK_ALGORITHM}$not-a-number$bad$hash"
    excessive_hash = "$".join(
        (
            _FALLBACK_ALGORITHM,
            str(_FALLBACK_MAX_ITERATIONS + 1),
            _encode_bytes(salt),
            _encode_bytes(digest),
        )
    )

    assert verify_password(password, malformed_hash) is False
    assert verify_password(password, excessive_hash) is False


def test_create_access_token_contains_only_sub_and_exp():
    subject = str(uuid4())
    token = create_access_token({"sub": subject}, expires_delta=timedelta(minutes=5))
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

    assert sorted(payload.keys()) == ["exp", "sub"]
    assert payload["sub"] == subject
    assert isinstance(payload["exp"], int)


def test_register_route_returns_created_status():
    route = next(route for route in auth_router.routes if getattr(route, "path", None) == "/register")
    assert route.status_code == 201


def test_register_function_normalizes_email_and_returns_user(db_session):
    user = asyncio.run(
        register(
            UserCreate(email="  New.User@Example.com ", password="supersecret"),
            db_session,
        )
    )

    assert user.email == "new.user@example.com"
    assert hasattr(user, "hashed_password")
    assert user.subscription_plan.value == "Free"


def test_login_function_returns_token_and_generic_log(db_session, caplog):
    caplog.set_level("INFO")
    user_id = uuid4()
    db_session.add(
        User(
            id=user_id,
            email="login@example.com",
            hashed_password=get_password_hash("supersecret"),
        )
    )
    db_session.commit()

    form = OAuth2PasswordRequestForm(
        username="login@example.com",
        password="supersecret",
    )
    response = asyncio.run(login(form, db_session))

    assert set(response.keys()) == {"access_token", "token_type"}

    payload = jwt.decode(
        response["access_token"],
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM],
    )
    assert sorted(payload.keys()) == ["exp", "sub"]
    assert payload["sub"] == str(user_id)
    assert any(record.message == "User login succeeded" for record in caplog.records)


def test_get_current_user_valid_token_resolves_user(db_session):
    user_id = UUID("12345678-1234-5678-1234-567812345678")
    db_session.add(
        User(
            id=user_id,
            email="user@example.com",
            hashed_password=get_password_hash("supersecret"),
        )
    )
    db_session.commit()

    token = create_access_token({"sub": str(user_id)})
    user = asyncio.run(get_current_user(token=token, db=db_session))

    assert user.id == user_id


def test_get_current_user_rejects_missing_sub(db_session):
    token = create_access_token({})

    with pytest.raises(HTTPException):
        asyncio.run(get_current_user(token=token, db=db_session))


def test_get_current_user_rejects_invalid_uuid_sub(db_session):
    token = create_access_token({"sub": "not-a-uuid"})

    with pytest.raises(HTTPException):
        asyncio.run(get_current_user(token=token, db=db_session))


def test_get_current_user_rejects_missing_or_malformed_exp(db_session):
    missing_exp_token = jwt.encode(
        {"sub": str(uuid4())},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    malformed_exp_token = jwt.encode(
        {"sub": str(uuid4()), "exp": "not-a-number"},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )

    with pytest.raises(HTTPException):
        asyncio.run(get_current_user(token=missing_exp_token, db=db_session))

    with pytest.raises(HTTPException):
        asyncio.run(get_current_user(token=malformed_exp_token, db=db_session))


def test_get_current_user_rejects_expired_token(db_session):
    expired_token = jwt.encode(
        {"sub": str(uuid4()), "exp": int(time.time()) - 60},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )

    with pytest.raises(HTTPException):
        asyncio.run(get_current_user(token=expired_token, db=db_session))


def test_get_current_user_rejects_missing_user(db_session):
    token = create_access_token({"sub": str(uuid4())})

    with pytest.raises(HTTPException):
        asyncio.run(get_current_user(token=token, db=db_session))
