#!/usr/bin/env python3

import sys
import os
import argparse
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.parsers.svg.importer import parse_color


parser = argparse.ArgumentParser(
    description="Converts a CSS color into a normalized array, as used in lottie"
)
parser.add_argument(
    "color",
    help="Color to inspect (in one of the CSS color formats)"
)

if __name__ == "__main__":
    ns = parser.parse_args()
    print(parse_color(ns.color).components)

