"""Cross-platform screen recording helper using ffmpeg.

Usage:
    from tools.record import start_recording, stop_recording
    proc = start_recording("out.mp4", fps=30)
    # ... drive your flow ...
    stop_recording(proc)
"""

from __future__ import annotations

import os
import shlex
import subprocess
import sys
from typing import Optional, Tuple, List


def _mac_command(output: str, fps: int, screen: Optional[int], region: Optional[Tuple[int, int, int, int]]) -> List[str]:
    # Device listing: ffmpeg -f avfoundation -list_devices true -i ""
    index = 1 if screen is None else int(screen)
    base = [
        "ffmpeg",
        "-y",
        "-f",
        "avfoundation",
        "-framerate",
        str(fps),
        "-i",
        f"{index}:",
    ]
    if region:
        x, y, w, h = region
        base += ["-filter:v", f"crop={w}:{h}:{x}:{y}"]
    base += ["-pix_fmt", "yuv420p", output]
    return base


def _linux_command(output: str, fps: int, display: Optional[str], region: Optional[Tuple[int, int, int, int]]) -> List[str]:
    # Default to :0.0 if not set
    disp = display or os.environ.get("DISPLAY", ":0.0")
    if region:
        x, y, w, h = region
        return [
            "ffmpeg",
            "-y",
            "-f",
            "x11grab",
            "-framerate",
            str(fps),
            "-video_size",
            f"{w}x{h}",
            "-i",
            f"{disp}+{x},{y}",
            "-pix_fmt",
            "yuv420p",
            output,
        ]
    return [
        "ffmpeg",
        "-y",
        "-f",
        "x11grab",
        "-framerate",
        str(fps),
        "-i",
        disp,
        "-pix_fmt",
        "yuv420p",
        output,
    ]


def _windows_command(output: str, fps: int, region: Optional[Tuple[int, int, int, int]]) -> List[str]:
    base = [
        "ffmpeg",
        "-y",
        "-f",
        "gdigrab",
        "-framerate",
        str(fps),
        "-i",
        "desktop",
    ]
    if region:
        x, y, w, h = region
        base = [
            "ffmpeg",
            "-y",
            "-f",
            "gdigrab",
            "-framerate",
            str(fps),
            "-offset_x",
            str(x),
            "-offset_y",
            str(y),
            "-video_size",
            f"{w}x{h}",
            "-i",
            "desktop",
        ]
    base += ["-pix_fmt", "yuv420p", output]
    return base


def start_recording(
    output_path: str,
    *,
    fps: int = 30,
    screen: Optional[int] = None,
    region: Optional[Tuple[int, int, int, int]] = None,
    linux_display: Optional[str] = None,
) -> subprocess.Popen:
    """Start an ffmpeg recording process.

    - macOS: set `screen` index if needed
    - Linux: set `linux_display` or rely on $DISPLAY
    - Windows: ignore `screen`; use `region` to crop
    - `region` is (x, y, width, height)
    """
    if sys.platform == "darwin":
        cmd = _mac_command(output_path, fps, screen, region)
    elif sys.platform.startswith("linux"):
        cmd = _linux_command(output_path, fps, linux_display, region)
    elif sys.platform.startswith("win"):
        cmd = _windows_command(output_path, fps, region)
    else:
        raise RuntimeError(f"Unsupported platform: {sys.platform}")

    # Use creationflags to avoid opening a new window on Windows
    creationflags = 0x08000000 if sys.platform.startswith("win") else 0
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=creationflags)


def stop_recording(proc: subprocess.Popen) -> None:
    try:
        if proc and proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=5)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass

