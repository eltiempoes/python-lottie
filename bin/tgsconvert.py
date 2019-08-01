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
try:
    import tgs.parsers.raster
    raster = True
except ImportError:
    raster = False


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
        ExtraOption("n_frames", type=int, default=60),
        ExtraOption("framerate", type=int, default=60),
    ]),
    Importer("Lottie JSON / Telegram Sticker", ["json", "tgs"], parsers.tgs.parse_tgs, [], "lottie"),
]
if raster:
    importers.append(
        Importer("Raster image", ["bmp", "png", "gif"], tgs.parsers.raster.raster_to_animation, [
            ExtraOption("n_colors", type=int, default=1, help="Number of colors to quantize"),
            ExtraOption("palette", type=parse_color, default=[], nargs="+", help="Custom palette"),
            # TODO color mode
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
    if ns.sanitize:
        an.tgs_sanitize()
    exporter.export(an, outfile, o_options)
