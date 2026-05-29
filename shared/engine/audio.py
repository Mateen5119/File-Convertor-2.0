"""Audio conversion module.

Handles: wav→mp3, m4a→mp3
Both require ffmpeg/pydub — desktop only.
"""

import tempfile
from pathlib import Path


def wav_to_mp3(data: bytes) -> bytes:
    """Convert WAV to MP3."""
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.wav"
        dst = Path(tmp) / "output.mp3"
        src.write_bytes(data)
        from pydub import AudioSegment
        audio = AudioSegment.from_wav(str(src))
        audio.export(str(dst), format="mp3", bitrate="192k")
        return dst.read_bytes()


def m4a_to_mp3(data: bytes) -> bytes:
    """Convert M4A to MP3."""
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.m4a"
        dst = Path(tmp) / "output.mp3"
        src.write_bytes(data)
        from pydub import AudioSegment
        audio = AudioSegment.from_file(str(src), format="m4a")
        audio.export(str(dst), format="mp3", bitrate="192k")
        return dst.read_bytes()
