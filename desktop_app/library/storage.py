import os
import json
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
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


def save_png_to_library(png_bytes: bytes, metadata: Optional[Dict[str, Any]] = None) -> str:
    """Save PNG to library with optional metadata sidecar file.
    
    Args:
        png_bytes: PNG image data
        metadata: Optional dict with extraction metadata (selection coords, color, threshold)
    
    Returns:
        Path to saved PNG file
    """
    ensure_library_dir()
    fname = auto_filename()
    path = os.path.join(LIB_DIR, fname)
    with open(path, "wb") as f:
        f.write(png_bytes)
    
    # Save metadata as JSON sidecar if provided
    if metadata:
        json_path = path.rsplit(".", 1)[0] + ".json"
        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)
        except Exception:
            pass  # Non-critical, continue even if metadata save fails
    
    return path


@dataclass
class LibraryItem:
    path: str
    modified: float  # epoch seconds
    metadata: Optional[Dict[str, Any]] = None

    @property
    def display_name(self) -> str:
        return os.path.basename(self.path)

    @property
    def pretty_time(self) -> str:
        try:
            return datetime.fromtimestamp(self.modified).strftime("%Y-%m-%d %H:%M")
        except Exception:
            return ""
    
    @property
    def tooltip_text(self) -> str:
        """Generate tooltip text with coordinate info and image dimensions."""
        lines = [
            f"File: {self.display_name}",
            f"Modified: {self.pretty_time}"
        ]
        
        # Always try to load image dimensions
        try:
            from PIL import Image
            with Image.open(self.path) as img:
                lines.append(f"Image Size: {img.width} × {img.height} px")
                lines.append(f"Mode: {img.mode}")
        except Exception:
            pass
        
        # Add file size
        try:
            file_size = os.path.getsize(self.path)
            if file_size < 1024:
                size_str = f"{file_size} B"
            elif file_size < 1024 * 1024:
                size_str = f"{file_size / 1024:.1f} KB"
            else:
                size_str = f"{file_size / (1024 * 1024):.1f} MB"
            lines.append(f"File Size: {size_str}")
        except Exception:
            pass
        
        # Add extraction metadata if available
        if self.metadata:
            lines.append("")  # Blank line separator
            lines.append("Extraction Info:")
            
            # Add selection coordinates if available
            if "selection" in self.metadata:
                sel = self.metadata["selection"]
                x1, y1 = sel.get("x1", 0), sel.get("y1", 0)
                x2, y2 = sel.get("x2", 0), sel.get("y2", 0)
                width, height = x2 - x1, y2 - y1
                lines.append(f"  Selection: ({x1}, {y1}) → ({x2}, {y2})")
                lines.append(f"  Selection Size: {width} × {height} px")
            
            # Add source image size if available
            if "image_size" in self.metadata:
                img_size = self.metadata["image_size"]
                w, h = img_size.get("width", 0), img_size.get("height", 0)
                if w and h:
                    lines.append(f"  Source Image: {w} × {h} px")
            
            # Add color info if available
            if "color" in self.metadata:
                lines.append(f"  Color: {self.metadata['color']}")
            
            # Add threshold if available
            if "threshold" in self.metadata:
                lines.append(f"  Threshold: {self.metadata['threshold']}")
            
            # Add session ID if available
            if "session_id" in self.metadata and self.metadata["session_id"]:
                session_id = self.metadata["session_id"]
                # Truncate long session IDs
                if len(session_id) > 20:
                    session_id = session_id[:17] + "..."
                lines.append(f"  Session: {session_id}")
        
        return "\n".join(lines)


def list_items(limit: int = 50) -> List[LibraryItem]:
    """List library items with optional metadata from sidecar JSON files."""
    ensure_library_dir()
    items: List[LibraryItem] = []
    for name in os.listdir(LIB_DIR):
        if not name.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        p = os.path.join(LIB_DIR, name)
        try:
            mtime = os.path.getmtime(p)
            
            # Try to load metadata from sidecar JSON
            metadata = None
            json_path = p.rsplit(".", 1)[0] + ".json"
            if os.path.exists(json_path):
                try:
                    with open(json_path, "r", encoding="utf-8") as f:
                        metadata = json.load(f)
                except Exception:
                    pass  # Ignore metadata read errors
            
            items.append(LibraryItem(path=p, modified=mtime, metadata=metadata))
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
