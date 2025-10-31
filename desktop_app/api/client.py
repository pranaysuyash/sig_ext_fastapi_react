from __future__ import annotations

import os
from typing import Optional, Dict, Any, Tuple
import requests

from desktop_app.state.session import SessionState


class ApiClient:
    def __init__(self, base_url: str, session: SessionState) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = session

    def _headers(self, extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers: Dict[str, str] = {"Accept": "application/json"}
        # Only add auth header if present (login is optional)
        if hasattr(self.session, 'auth_header'):
            headers.update(self.session.auth_header())
        if extra:
            headers.update(extra)
        return headers

    # Login is optional; method retained for future use
    def login(self, username: str, password: str) -> Dict[str, Any]:
        url = f"{self.base_url}/auth/login"
        data = {"username": username, "password": password}
        resp = requests.post(url, data=data, headers={"Accept": "application/json"}, timeout=30)
        resp.raise_for_status()
        payload = resp.json()
        token = payload.get("access_token")
        if not token:
            raise RuntimeError("No access_token in login response")
        self.session.access_token = token
        self.session.user_email = username
        return payload

    def upload_image(self, filepath: str) -> Dict[str, Any]:
        url = f"{self.base_url}/extraction/upload"
        if not os.path.exists(filepath):
            raise FileNotFoundError(filepath)
        with open(filepath, "rb") as f:
            files = {"file": (os.path.basename(filepath), f, "application/octet-stream")}
            resp = requests.post(url, files=files, headers=self._headers(), timeout=120)
        resp.raise_for_status()
        payload = resp.json()
        self.session.session_id = payload.get("id")
        return payload

    def process_image(self, *, session_id: str, x1: int, y1: int, x2: int, y2: int, color: str, threshold: int) -> bytes:
        url = f"{self.base_url}/extraction/process_image/"
        data = {
            "session_id": session_id,
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "color": color,
            "threshold": threshold,
        }
        self.session.last_request = data.copy()
        resp = requests.post(url, data=data, headers=self._headers(), timeout=120)
        if resp.status_code == 404:
            raise FileNotFoundError("Image file not found on server for session_id")
        resp.raise_for_status()
        return resp.content  # PNG bytes

    def health_check(self, timeout: float = 3.0) -> Tuple[bool, Dict[str, Any]]:
        """Ping backend /health. Returns (ok, payload_or_error).

        - ok=True and payload dict when reachable and healthy
        - ok=False and payload containing {"error": str} when unreachable or unhealthy
        """
        url = f"{self.base_url}/health"
        try:
            resp = requests.get(url, headers={"Accept": "application/json"}, timeout=timeout)
            resp.raise_for_status()
            payload = resp.json()
            # Consider presence of status=="healthy" as OK when provided
            ok = True
            if isinstance(payload, dict) and payload.get("status"):
                ok = str(payload.get("status")).lower() in {"ok", "healthy", "up"}
            return ok, payload if isinstance(payload, dict) else {"raw": payload}
        except requests.exceptions.RequestException as e:
            return False, {"error": str(e)}
