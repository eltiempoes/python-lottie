#!/usr/bin/env python3

import json
import sys
import os
import argparse
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.utils.font import fonts
from lottie import __version__

parser = argparse.ArgumentParser(
    description="List available fonts",
)
parser.add_argument("--version", "-v", action="version", version="%(prog)s - python-lottie " + __version__)
parser.add_argument(
    "fonts",
    default=[],
    nargs="*",
    help="Font family names"
)


def _fonts(flist):
    for font in flist:
        if font in fonts:
            yield font


if __name__ == "__main__":
    ns = parser.parse_args()
    font_iter = _fonts(ns.fonts) if ns.fonts else fonts
    for font in font_iter:
        print("* %s" % font)
        for style in fonts[font].files.keys():
            print("  * %s" % " ".join(style))
