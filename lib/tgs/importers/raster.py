from .base import importer
from ..parsers.baseporter import ExtraOption
from ..parsers.pixel import pixel_to_animation_paths, pixel_to_animation
from ..parsers.svg.importer import parse_color

try:
    from ..parsers.raster import raster_to_animation
    raster = True
except ImportError:
    raster = False


@importer("Raster image", ["bmp", "png", "gif"], [
    ExtraOption("n_colors", type=int, default=1, help="Number of colors to quantize"),
    ExtraOption("palette", type=parse_color, default=[], nargs="+", help="Custom palette"),
    ExtraOption(
        "mode",
        default="pixel",
        choices=["pixel", "polygon"] + (["bezier"] if raster else []),
        help="Vectorization mode"
    ),
    ExtraOption("frame_delay", type=int, default=4, help="Number of frames to skip between images"),
    ExtraOption("framerate", type=int, default=60, help="Frames per second"),
    # TODO QuanzationMode for raster
])
def import_raster(filenames, n_colors, palette, mode, frame_delay=1, framerate=60):
    if mode == "bezier":
        return raster_to_animation(
            filenames, n_colors, frame_delay,
            framerate=framerate,
            palette=palette
        )
    elif mode == "polygon":
        return pixel_to_animation_paths(filenames, frame_delay, framerate)
    else:
        return pixel_to_animation(filenames, frame_delay, framerate)

