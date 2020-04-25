#!/usr/bin/env python3

import json
import sys
import os
import argparse
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.exporters import prettyprint, prettyprint_summary
from lottie.objects import Animation
from lottie.parsers.tgs import parse_tgs
from lottie import __version__

parser = argparse.ArgumentParser(
    description="Pretty prints a tgs / lottie file with more readable annotations (useful to debug / diff lottie files)"
)
parser.add_argument("--version", "-v", action="version", version="%(prog)s - python-lottie " + __version__)
parser.add_argument(
    "infile",
    help="Input file"
)
parser.add_argument(
    "--summary",
    "-s",
    action="store_true",
    help="Just show a short summary"
)

if __name__ == "__main__":
    ns = parser.parse_args()

    an = parse_tgs(ns.infile)

    if ns.summary:
        prettyprint_summary(an)
    else:
        prettyprint(an)

