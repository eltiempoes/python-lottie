#!/usr/bin/env python3

import json
import sys
import os
import argparse
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.exporters import prettyprint, prettyprint_summary
from tgs.objects import Animation
from tgs.parsers.tgs import parse_tgs

parser = argparse.ArgumentParser(
    description="Pretty prints a tgs / lottie file with more readable annotations (useful to debug / diff lottie files)"
)
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

