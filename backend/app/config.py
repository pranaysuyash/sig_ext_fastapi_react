from __future__ import annotations

import logging
from pathlib import Path

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application configuration loaded from environment variables or .env."""

    model_config = SettingsConfigDict(
        env_file=str((Path(__file__).resolve().parents[1] / ".env")),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Database settings
    DATABASE_HOSTNAME: str = "localhost"
    DATABASE_PORT: str = "5432"
    DATABASE_PASSWORD: str = "pranay"
    DATABASE_NAME: str = "signature_extractor"
    DATABASE_USERNAME: str = "pranay"

    # JWT settings
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Optional third-party integrations
    RAZORPAY_KEY_ID: str | None = None
    RAZORPAY_KEY_SECRET: str | None = None

    @property
    def DATABASE_URL(self) -> str:
        """Construct a SQLAlchemy-compatible database URL."""
        return (
            f"postgresql://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOSTNAME}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info("Settings initialized successfully")
        logger.debug("Database URL: %s", self.DATABASE_URL)
        logger.debug("JWT Algorithm: %s", self.JWT_ALGORITHM)
        logger.debug(
            "JWT Expiry: %s minutes", self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )


try:
    settings = Settings()
except ValidationError as exc:
    logger.error("Settings validation error: %s", exc)
    raise
except Exception as exc:
    logger.error("Unexpected error loading settings: %s", exc)
    raise
