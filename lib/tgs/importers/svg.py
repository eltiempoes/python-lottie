from .base import importer
from ..parsers.baseporter import ExtraOption ## fff
from ..parsers.svg import parse_svg_file


@importer("SVG", ["svg"], [
    ExtraOption("layer_frames", type=int, default=0,
        help="If greater than 0, treats every layer in the SVG as a different animation frame, "
        "greater values increase the time each frames lasts for."),
    ExtraOption("n_frames", type=int, default=60),
    ExtraOption("framerate", type=int, default=60),
])
def import_svg(file, *a, **kw):
    return parse_svg_file(file, *a, **kw)
