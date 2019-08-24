#!/usr/bin/env python3

import sys
import os
import argparse
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.exporters import export_tgs, export_lottie
from tgs.parsers.svg.importer import parse_color

parser = argparse.ArgumentParser(
    description="Vectorizes raster images into a TGS file"
)

parser.add_argument(
    "infile",
    nargs="+",
    help="Input frames"
)
parser.add_argument(
    "--output",
    "-o",
    default="-",
    help="Output file"
)
parser.add_argument(
    "--format",
    "-f",
    default="tgs",
    choices=["tgs", "lottie"],
    help="Output format"
)
parser.add_argument(
    "--framerate",
    default=60,
    type=int,
    help="Output file framerate"
)
parser.add_argument(
    "--delay", "-d",
    default=1,
    type=int,
    help="Delay between source images"
)
parser.add_argument(
    "--colors", "-c",
    default=1,
    type=int,
    help="Number of colors to quantize"
)
parser.add_argument(
    "--palette",
    "-p",
    type=parse_color,
    default=[],
    nargs="+",
    help="Custom palette"
)
parser.add_argument(
    "--color-mode",
    default="nearest",
    choices=["nearest", "exact"],
    help="How to quantize colors." +
         "nearest will map each color to the most similar in the palette." +
         " exact will only match exact colors"
)
parser.add_argument(
    "--mode",
    "-m",
    default="bezier",
    choices=["bezier", "pixel"],
    help="Vectorization mode"
)

if __name__ == "__main__":
    ns = parser.parse_args()
    if ns.mode == "bezier":
        from tgs.parsers.raster import QuanzationMode, raster_to_animation

        cm = QuanzationMode.Nearest if ns.color_mode == "nearest" else QuanzationMode.Exact

        animation = raster_to_animation(
            ns.infile, ns.colors, ns.delay,
            framerate=ns.framerate,
            palette=ns.palette,
            mode=cm
        )
    else:
        from tgs.parsers.pixel import pixel_to_animation
        animation = pixel_to_animation(
            ns.infile, ns.delay, ns.framerate
        )

    binary = ns.format == "tgs"
    if ns.output == "-":
        outfile = sys.stdout
        if binary:
            outfile = outfile.buffer
    else:
        outfile = open(ns.output, "w" + ("b" if binary else ""))

    if ns.format == "lottie":
        export_lottie(animation, outfile, True)
    else:
        export_tgs(animation, outfile)
