import io
import sys
from PIL import Image
from PIL import features

from .cairo import export_png
from .base import exporter
from ..parsers.baseporter import ExtraOption


def _png_gif_prepare(image):
    if image.mode not in ["RGBA", "RGBa"]:
        image = image.convert("RGBA")
    alpha = image.getchannel("A")
    image = image.convert("RGB").convert('P', palette=Image.ADAPTIVE, colors=255)
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    image.paste(255, mask=mask)
    return image


def _log_frame(fmt, frame_no=None, end=None):
    if frame_no is None:
        sys.stderr.write("\r%s frame rendering completed\n" % (fmt))
    else:
        sys.stderr.write("\r%s rendering frame %s/%s" % (fmt, frame_no, end))
    sys.stderr.flush()


@exporter("GIF", ["gif"], [
    ExtraOption("skip_frames", type=int, default=5, help="Only renderer 1 out of these many frames"),
])
def export_gif(animation, fp, dpi=96, skip_frames=5):
    """
    Gif export

    Note that it's a bit slow.
    """
    start = int(animation.in_point)
    end = int(animation.out_point)
    frames = []
    for i in range(start, end+1, skip_frames):
        _log_frame("GIF", i, end)
        file = io.BytesIO()
        export_png(animation, file, i, dpi)
        file.seek(0)
        frames.append(_png_gif_prepare(Image.open(file)))
    _log_frame("GIF")


    sys.stderr.write("GIF Writing to file...\n")
    duration = 1000 / animation.frame_rate
    frames[0].save(
        fp,
        format='GIF',
        append_images=frames[1:],
        save_all=True,
        duration=duration,
        loop=0,
        transparency=255,
        disposal=2,
    )


@exporter("WebP", ["webp"], [
    ExtraOption("lossless", action="store_true", help="If present, use lossless compression"),
    ExtraOption("quality", type=int, default=80, help="Compression effort between 0 and 100, for lossy 0 gives the smalles size, for lossless 0 gives the largest file"),
    ExtraOption("method", type=int, default=0, help="Quality/speed trade-off (0=fast, 6=slower-better)"),
])
def export_webp(animation, fp, dpi=96, lossless=False, quality=80, method=0):
    """
    Export WebP

    See https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#webp
    """
    if not features.check("webp_anim"):
        raise Exception("WebP animations not supported in this system")

    start = int(animation.in_point)
    end = int(animation.out_point)
    frames = []
    for i in range(start, end+1):
        _log_frame("WebP", i, end)
        file = io.BytesIO()
        export_png(animation, file, i, dpi)
        file.seek(0)
        frames.append(Image.open(file))
    _log_frame("WebP")

    sys.stderr.write("WebP Writing to file...\n")
    duration = int(round(1000 / animation.frame_rate))
    frames[0].save(
        fp,
        format='WebP',
        append_images=frames[1:],
        save_all=True,
        duration=duration,
        loop=0,
        background=(0, 0, 0, 0),
        lossless=lossless,
        quality=quality,
        method=method
    )
