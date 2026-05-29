"""Video conversion module.

Handles: mp4→mp3, mov→mp4, mkv→mp4, webm→mp4
All require ffmpeg binary — desktop only.
"""

import tempfile
from pathlib import Path


def mp4_to_mp3(data: bytes) -> bytes:
    """Extract audio from MP4 as MP3."""
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.mp4"
        dst = Path(tmp) / "output.mp3"
        src.write_bytes(data)
        import ffmpeg
        (
            ffmpeg
            .input(str(src))
            .output(str(dst), acodec="libmp3lame", q_a=2)
            .overwrite_output()
            .run(quiet=True)
        )
        return dst.read_bytes()


def mov_to_mp4(data: bytes) -> bytes:
    """Convert MOV to MP4."""
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
            .run(quiet=True)
        )
        return dst.read_bytes()


def mkv_to_mp4(data: bytes) -> bytes:
    """Convert MKV to MP4."""
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
            .run(quiet=True)
        )
        return dst.read_bytes()


def webm_to_mp4(data: bytes) -> bytes:
    """Convert WebM to MP4."""
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
            .run(quiet=True)
        )
        return dst.read_bytes()
