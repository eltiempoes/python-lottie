#!/usr/bin/env python3

import sys
import os
import argparse
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.exporters import export_sif
from tgs.parsers.tgs import parse_tgs

parser = argparse.ArgumentParser(
    description="Converts a lottie/tgs file into a sif animation"
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

ns = parser.parse_args()

an = parse_tgs(ns.infile)

outfile = ns.outfile
if outfile == "-":
    outfile = sys.stdout
export_sif(an, outfile)



