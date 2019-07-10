#!/usr/bin/env python3

import sys
import os
import argparse
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.parsers.svg import parse_svg_file
from tgs.exporters import export_tgs, export_lottie

parser = argparse.ArgumentParser(
    description="Converts a (static) SVG image into a TGS file"
)
parser.add_argument(
    "infile",
    nargs="?",
    default="-",
    help="Input file"
)
parser.add_argument(
    "outfile",
    nargs="?",
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
    "--frames",
    default=60,
    type=int,
    help="Output file frame count"
)
ns = parser.parse_args()

if ns.infile == "-":
    infile = sys.stdin
else:
    infile = ns.infile

animation = parse_svg_file(infile, ns.frames, ns.framerate)


binary = ns.format == "tgs"
if ns.outfile == "-":
    outfile = sys.stdout
    if binary:
        outfile = outfile.buffer
else:
    outfile = open(ns.outfile, "w" + ("b" if binary else ""))

if ns.format == "lottie":
    export_lottie(animation, outfile)
else:
    export_tgs(animation, outfile)
