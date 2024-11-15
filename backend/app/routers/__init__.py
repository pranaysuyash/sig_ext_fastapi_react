# backend/app/routers/__init__.py
from .auth import router as auth_router
from .extraction import router as extraction_router

__all__ = ["auth_router", "extraction_router"]
