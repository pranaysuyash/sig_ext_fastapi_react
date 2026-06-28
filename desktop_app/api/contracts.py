from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class LoginResponse:
    access_token: str
    payload: Dict[str, Any]


@dataclass(frozen=True)
class UploadResponse:
    session_id: str
    filename: Optional[str]
    file_path: Optional[str]
    payload: Dict[str, Any]


@dataclass(frozen=True)
class ProcessResponse:
    png_bytes: bytes
    content_type: str
    payload: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class RegionSelectionResponse:
    session_id: str
    selection: Optional[Dict[str, Any]]
    image: Optional[Dict[str, Any]]
    message: Optional[str]
    file_path: Optional[str]
    payload: Dict[str, Any]
