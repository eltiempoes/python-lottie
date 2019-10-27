#!/usr/bin/env python3

import re
import sys
import os
import argparse
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.exporters import exporters
from tgs.exporters.base import ExtraOption, _add_options
from tgs import parsers
from tgs.parsers.svg.importer import parse_color
from tgs.utils.stripper import float_strip, heavy_strip
try:
    import tgs.parsers.pixel
    pixel = True
except ImportError:
    pixel = False


class Importer:
    def __init__(self, name, extensions, callback, extra_options=[], slug=None):
        self.name = name
        self.extensions = extensions
        self.callback = callback
        self.extra_options = extra_options
        self.slug = slug if slug is not None else extensions[0]

    def load(self, stream, extra_options):
        return self.callback(stream, **extra_options)


importers = [
    Importer("SVG", ["svg"], parsers.svg.parse_svg_file, [
        ExtraOption("layer_frames", type=int, default=0,
            help="If greater than 0, treats every layer in the SVG as a different animation frame, "
            "greater values increase the time each frames lasts for."),
        ExtraOption("n_frames", type=int, default=60),
        ExtraOption("framerate", type=int, default=60),
    ]),
    Importer("Lottie JSON / Telegram Sticker", ["json", "tgs"], parsers.tgs.parse_tgs, [], "lottie"),
]
if pixel:
    try:
        import tgs.parsers.raster
        raster = True
    except ImportError:
        raster = False

    def bitmap_to_animation(filenames, n_colors, palette, mode, frame_delay=1, framerate=60):
        if raster and mode == "bezier":
            return tgs.parsers.raster.raster_to_animation(
                filenames, n_colors, frame_delay,
                framerate=framerate,
                palette=palette
            )
        elif mode == "polygon":
            return tgs.parsers.pixel.pixel_to_animation_paths(filenames, frame_delay, framerate)
        else:
            return tgs.parsers.pixel.pixel_to_animation(filenames, frame_delay, framerate)

    mode_option = ExtraOption(
        "mode",
        default="pixel",
        choices=["bezier", "pixel", "polygon"],
        help="Vectorization mode"
    )

    importers.append(
        Importer("Raster image", ["bmp", "png", "gif"], bitmap_to_animation, [
            ExtraOption("n_colors", type=int, default=1, help="Number of colors to quantize"),
            ExtraOption("palette", type=parse_color, default=[], nargs="+", help="Custom palette"),
            mode_option,
            ExtraOption("frame_delay", type=int, default=4, help="Number of frames to skip between images"),
            ExtraOption("framerate", type=int, default=60, help="Frames per second"),
            # TODO QuanzationMode for raster
        ])
    )


desc = """Converts between multiple formats

Supported formats:

- Input:
%s

- Output:
%s
""" % (
    "\n".join("%s- %s" % (" "*2, e.name) for e in importers),
    "\n".join("%s- %s" % (" "*2, e.name) for e in exporters),
)

parser = argparse.ArgumentParser(
    description=desc,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)

group = parser.add_argument_group("Generic input options")
group.add_argument(
    "infile",
    default="-",
    nargs="?",
    help="Input file"
)
group.add_argument(
    "--input-format", "-if",
    default=None,
    choices=[importer.slug for importer in importers],
    help="Explicit output format (if missing implied by the input filename)",
)


group = exporters.set_options(parser)

group.add_argument(
    "outfile",
    default="-",
    nargs="?",
    help="Output file"
)
group.add_argument(
    "--output-format", "-of",
    default=None,
    choices=[exporter.slug for exporter in exporters],
    help="Explicit output format (if missing implied by the output filename)",
)
group.add_argument(
    "--sanitize",
    default=False,
    action="store_true",
    help="Ensure the animation is 512x512 and 30 or 60 fps",
)
group.add_argument(
    "--optimize",
    "-O",
    default=1,
    type=int,
    choices=[0, 1, 2],
    help="Optimize the animation parameter: 0 no optimization, 1 truncate floats, 2 truncate floats and names",
)


for importer in importers:
    _add_options(parser, "import", importer)

if __name__ == "__main__":
    ns = parser.parse_args()

    infile = ns.infile
    importer = None
    if infile == "-":
        infile = sys.stdin
    else:
        suf = os.path.splitext(infile)[1][1:]
        for p in importers:
            if suf in p.extensions:
                importer = p
                break
    if ns.input_format:
        importer = None
        for p in importers:
            if p.slug == ns.input_format:
                importer = p
                break
    if not importer:
        sys.stderr.write("Unknown importer\n")
        sys.exit(1)

    outfile = ns.outfile
    exporter = None
    if outfile == "-":
        outfile = sys.stdout
    else:
        exporter = exporters.get_from_filename(outfile)
    if ns.output_format:
        exporter = exporters.get(ns.output_format)

    if not exporter:
        sys.stderr.write("Unknown exporter\n")
        sys.exit(1)

    i_options = {}
    for opt in importer.extra_options:
        i_options[opt.name] = getattr(ns, opt.nsvar(importer.slug))

    o_options = exporter.argparse_options(ns)

    an = importer.load(infile, i_options)
    if ns.optimize == 1:
        float_strip(an)
    elif ns.optimize >= 2:
        heavy_strip(an)
    if ns.sanitize:
        an.tgs_sanitize()
    exporter.export(an, outfile, o_options)
