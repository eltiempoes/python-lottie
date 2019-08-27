import io
from PIL import Image

from .cairo import export_png
from .base import exporter, ExtraOption


def _png_gif_prepare(image):
    if image.mode not in ["RGBA", "RGBa"]:
        image = image.convert("RGBA")
    alpha = image.getchannel("A")
    image = image.convert('P', palette=Image.ADAPTIVE, colors=255)
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    image.paste(255, mask)
    return image


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
        file = io.BytesIO()
        export_png(animation, file, i, dpi)
        file.seek(0)
        frames.append(_png_gif_prepare(Image.open(file)))

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
