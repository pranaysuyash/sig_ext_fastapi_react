import os
from dataclasses import dataclass
from typing import List
from datetime import datetime


APP_DIR = os.path.join(os.path.expanduser("~"), ".signature_extractor")
LIB_DIR = os.path.join(APP_DIR, "signatures")


def ensure_library_dir() -> str:
    os.makedirs(LIB_DIR, exist_ok=True)
    return LIB_DIR


def library_dir() -> str:
    return ensure_library_dir()


def auto_filename(prefix: str = "signature", ext: str = ".png") -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}{ext}"


def save_png_to_library(png_bytes: bytes) -> str:
    ensure_library_dir()
    fname = auto_filename()
    path = os.path.join(LIB_DIR, fname)
    with open(path, "wb") as f:
        f.write(png_bytes)
    return path


@dataclass
class LibraryItem:
    path: str
    modified: float  # epoch seconds

    @property
    def display_name(self) -> str:
        return os.path.basename(self.path)

    @property
    def pretty_time(self) -> str:
        try:
            return datetime.fromtimestamp(self.modified).strftime("%Y-%m-%d %H:%M")
        except Exception:
            return ""


def list_items(limit: int = 50) -> List[LibraryItem]:
    ensure_library_dir()
    items: List[LibraryItem] = []
    for name in os.listdir(LIB_DIR):
        if not name.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        p = os.path.join(LIB_DIR, name)
        try:
            mtime = os.path.getmtime(p)
            items.append(LibraryItem(path=p, modified=mtime))
        except Exception:
            continue
    items.sort(key=lambda x: x.modified, reverse=True)
    return items[:limit]


def delete_item(path: str) -> bool:
    try:
        if os.path.commonpath([os.path.abspath(path), os.path.abspath(LIB_DIR)]) != os.path.abspath(LIB_DIR):
            return False
    except Exception:
        return False
    try:
        os.remove(path)
        return True
    except Exception:
        return False
