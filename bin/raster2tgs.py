#!/usr/bin/env python3

import sys
import os
import argparse
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.parsers.raster import raster_frames_to_animation
from tgs.exporters import export_tgs, export_lottie

parser = argparse.ArgumentParser(
    description="Converts raster images into a TGS file"
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

ns = parser.parse_args()

animation = raster_frames_to_animation(ns.infile, ns.colors, ns.delay, framerate=ns.framerate)

binary = ns.format == "tgs"
if ns.output == "-":
    outfile = sys.stdout
    if binary:
        outfile = outfile.buffer
else:
    outfile = open(ns.output, "w" + ("b" if binary else ""))

if ns.format == "lottie":
    export_lottie(animation, outfile)
else:
    export_tgs(animation, outfile)
