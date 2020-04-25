#!/usr/bin/env python3

import sys
import os
import re
import argparse
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.parsers.svg.importer import parse_color
from lottie import NVector
from lottie import __version__


def _parse_color(color):
    # Inkscape colors
    if re.match(r"^[0-9a-fA-F]{8}$", color):
        return NVector(*(
            int(color[i:i+2], 16) / 0xff
            for i in range(0, 8, 2)
        ))
    return parse_color(color)



parser = argparse.ArgumentParser(
    description="Converts a CSS color into a normalized array, as used in lottie"
)
parser.add_argument("--version", "-v", action="version", version="%(prog)s - python-lottie " + __version__)
parser.add_argument(
    "color",
    help="Color to inspect (in one of the CSS color formats)"
)

if __name__ == "__main__":
    ns = parser.parse_args()
    print(_parse_color(ns.color).components)
