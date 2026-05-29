"""Audio conversion module.

Handles: wav→mp3, m4a→mp3
Both require ffmpeg/pydub — desktop only.
"""

import tempfile
from pathlib import Path
from .validator import validate


def wav_to_mp3(data: bytes, is_web: bool = False) -> bytes:
    """Convert WAV to MP3."""
    validate(data, "wav", is_web=is_web)
    if is_web:
        raise ValueError("Audio conversions are desktop-only due to Vercel compute limitations.")
        
    from pydub import AudioSegment
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.wav"
        dst = Path(tmp) / "output.mp3"
        src.write_bytes(data)
        audio = AudioSegment.from_wav(str(src))
        audio.export(str(dst), format="mp3", bitrate="192k")
        return dst.read_bytes()


def m4a_to_mp3(data: bytes, is_web: bool = False) -> bytes:
    """Convert M4A to MP3."""
    validate(data, "m4a", is_web=is_web)
    if is_web:
        raise ValueError("Audio conversions are desktop-only due to Vercel compute limitations.")
        
    from pydub import AudioSegment
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.m4a"
        dst = Path(tmp) / "output.mp3"
        src.write_bytes(data)
        audio = AudioSegment.from_file(str(src), format="m4a")
        audio.export(str(dst), format="mp3", bitrate="192k")
        return dst.read_bytes()
