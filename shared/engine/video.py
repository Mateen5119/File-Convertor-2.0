"""Video conversion module.

Handles: mp4→mp3, mov→mp4, mkv→mp4, webm→mp4
All require ffmpeg binary — desktop only.
"""

import tempfile
import subprocess
from pathlib import Path
from .validator import validate


def mp4_to_mp3(data: bytes, is_web: bool = False) -> bytes:
    """Extract audio from MP4 as MP3."""
    validate(data, "mp4", is_web=is_web)
    if is_web:
        raise ValueError("Video conversions are premium desktop-only features.")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.mp4"
        dst = Path(tmp) / "output.mp3"
        src.write_bytes(data)
        
        # ISS-019: Subprocess / ffmpeg execution with timeout parameters to prevent infinite hangs
        import ffmpeg
        (
            ffmpeg
            .input(str(src))
            .output(str(dst), acodec="libmp3lame", q_a=2)
            .overwrite_output()
            .run(quiet=True, timeout=45)
        )
        return dst.read_bytes()


def mov_to_mp4(data: bytes, is_web: bool = False) -> bytes:
    """Convert MOV to MP4."""
    validate(data, "mov", is_web=is_web)
    if is_web:
        raise ValueError("Video conversions are premium desktop-only features.")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.mov"
        dst = Path(tmp) / "output.mp4"
        src.write_bytes(data)
        
        import ffmpeg
        (
            ffmpeg
            .input(str(src))
            .output(str(dst), vcodec="libx264", acodec="aac", movflags="faststart")
            .overwrite_output()
            .run(quiet=True, timeout=60)
        )
        return dst.read_bytes()


def mkv_to_mp4(data: bytes, is_web: bool = False) -> bytes:
    """Convert MKV to MP4."""
    validate(data, "mkv", is_web=is_web)
    if is_web:
        raise ValueError("Video conversions are premium desktop-only features.")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.mkv"
        dst = Path(tmp) / "output.mp4"
        src.write_bytes(data)
        
        import ffmpeg
        (
            ffmpeg
            .input(str(src))
            .output(str(dst), vcodec="libx264", acodec="aac", movflags="faststart")
            .overwrite_output()
            .run(quiet=True, timeout=60)
        )
        return dst.read_bytes()


def webm_to_mp4(data: bytes, is_web: bool = False) -> bytes:
    """Convert WebM to MP4."""
    validate(data, "webm", is_web=is_web)
    if is_web:
        raise ValueError("Video conversions are premium desktop-only features.")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.webm"
        dst = Path(tmp) / "output.mp4"
        src.write_bytes(data)
        
        import ffmpeg
        (
            ffmpeg
            .input(str(src))
            .output(str(dst), vcodec="libx264", acodec="aac", movflags="faststart")
            .overwrite_output()
            .run(quiet=True, timeout=60)
        )
        return dst.read_bytes()
