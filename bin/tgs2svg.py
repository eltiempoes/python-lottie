#!/usr/bin/env python3

import sys
import os
import argparse
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.exporters import export_svg
from tgs.parsers.tgs import parse_tgs

parser = argparse.ArgumentParser(
    description="Extract a SVG from a lottie/tgs file"
)
parser.add_argument(
    "infile",
    help="Input file"
)
parser.add_argument(
    "outfile",
    default="-",
    help="Input file"
)
parser.add_argument(
    "--frame",
    "-f",
    type=float,
    default=0,
    help="(Frame) time at which to get the snapshot"
)
parser.add_argument(
    "--percent",
    "-p",
    type=float,
    default=None,
    help="(Frame) time at which to get the snapshot, as a percentage (eg 50 => middle frame)"
)

if __name__ == "__main__":
    ns = parser.parse_args()

    an = parse_tgs(ns.infile)

    time = ns.frame
    if ns.percent is not None:
        time = an.out_point * ns.percent / 100

    outfile = ns.outfile
    if outfile == "-":
        outfile = sys.stdout
    export_svg(an, outfile, time)
