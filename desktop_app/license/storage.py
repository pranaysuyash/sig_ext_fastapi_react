import json
import os
from dataclasses import dataclass
from typing import Optional


APP_DIR_NAME = ".signature_extractor"
LICENSE_FILE = "license.json"


def _config_dir() -> str:
    """Return the per-user config directory (e.g., ~/.signature_extractor)."""
    home = os.path.expanduser("~")
    path = os.path.join(home, APP_DIR_NAME)
    os.makedirs(path, exist_ok=True)
    return path


def _license_path() -> str:
    return os.path.join(_config_dir(), LICENSE_FILE)


@dataclass
class LicenseInfo:
    key: str
    email: Optional[str] = None


def load_license() -> Optional[LicenseInfo]:
    """Load license info from disk, if present."""
    path = _license_path()
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        key = data.get("key", "").strip()
        email = data.get("email")
        if key:
            return LicenseInfo(key=key, email=email)
    except Exception:
        # Ignore malformed file
        return None
    return None


def save_license(key: str, email: Optional[str] = None) -> None:
    """Persist license info to disk."""
    data = {"key": key.strip()}
    if email:
        data["email"] = email.strip()
    with open(_license_path(), "w", encoding="utf-8") as f:
        json.dump(data, f)


def is_licensed() -> bool:
    """Very lightweight local check for MVP: consider any non-empty key as licensed.

    Later, integrate an online verification or signature check if desired.
    """
    info = load_license()
    return bool(info and info.key and len(info.key) >= 6)
