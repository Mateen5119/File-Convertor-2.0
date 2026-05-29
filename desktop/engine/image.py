"""Image conversion module.

Handles: heic→jpg, webp→png, webp→jpg, png→jpg, svg→png, tiff→jpg, tiff→pdf, gif→mp4
"""

import io
import tempfile
from pathlib import Path
from .validator import validate


def heic_to_jpg(data: bytes) -> bytes:
    validate(data, "heic")
    from pillow_heif import register_heif_opener
    register_heif_opener()
    from PIL import Image
    img = Image.open(io.BytesIO(data)).convert("RGB")
    out = io.BytesIO()
    img.save(out, "JPEG", quality=90)
    return out.getvalue()


def webp_to_png(data: bytes) -> bytes:
    validate(data, "webp")
    from PIL import Image
    img = Image.open(io.BytesIO(data)).convert("RGBA")
    out = io.BytesIO()
    img.save(out, "PNG")
    return out.getvalue()


def webp_to_jpg(data: bytes) -> bytes:
    validate(data, "webp")
    from PIL import Image
    img = Image.open(io.BytesIO(data)).convert("RGB")
    out = io.BytesIO()
    img.save(out, "JPEG", quality=90)
    return out.getvalue()


def png_to_jpg(data: bytes, quality: int = 90) -> bytes:
    validate(data, "png")
    from PIL import Image
    img = Image.open(io.BytesIO(data)).convert("RGB")
    out = io.BytesIO()
    img.save(out, "JPEG", quality=quality)
    return out.getvalue()


def svg_to_png(data: bytes) -> bytes:
    import cairosvg
    return cairosvg.svg2png(bytestring=data)


def tiff_to_jpg(data: bytes) -> bytes:
    from PIL import Image
    img = Image.open(io.BytesIO(data)).convert("RGB")
    out = io.BytesIO()
    img.save(out, "JPEG", quality=90)
    return out.getvalue()


def tiff_to_pdf(data: bytes) -> bytes:
    from PIL import Image
    img = Image.open(io.BytesIO(data))
    frames = []
    try:
        while True:
            frames.append(img.copy().convert("RGB"))
            img.seek(img.tell() + 1)
    except EOFError:
        pass
    out = io.BytesIO()
    if len(frames) == 1:
        frames[0].save(out, "PDF")
    else:
        frames[0].save(out, "PDF", save_all=True, append_images=frames[1:])
    return out.getvalue()


def gif_to_mp4(data: bytes) -> bytes:
    """Requires ffmpeg binary — desktop only."""
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "input.gif"
        dst = Path(tmp) / "output.mp4"
        src.write_bytes(data)
        import ffmpeg
        (
            ffmpeg
            .input(str(src))
            .output(str(dst), vcodec="libx264", pix_fmt="yuv420p", movflags="faststart")
            .overwrite_output()
            .run(quiet=True)
        )
        return dst.read_bytes()
