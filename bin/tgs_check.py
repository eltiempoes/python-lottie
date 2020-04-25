#!/usr/bin/env python3

import sys
import os
import argparse
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.exporters.tgs_validator import TgsValidator, Severity
from lottie import __version__


parser = argparse.ArgumentParser(
    description="Checks a lottie or tgs file to see if it's compatible with telegram stickers",
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("--version", "-v", action="version", version="%(prog)s - python-lottie " + __version__)
parser.add_argument(
    "infile",
    help="Input file"
)
parser.add_argument(
    "--level", "-l",
    choices=list(Severity.__members__.keys()),
    help="Error level:\n"
    "* Note   : the feature is not officially supported but works regardless\n"
    "* Warning: the feature is not supported, might result in different animations than expected\n"
    "* Error  : Telegram will not recognize the sticker\n",
    default="Note",
)


if __name__ == "__main__":
    ns = parser.parse_args()
    severity = Severity.__members__[ns.level]

    validator = TgsValidator(severity)
    validator.check_file(ns.infile)
    if validator.errors:
        sys.stdout.write("\n".join(map(str, validator.errors))+"\n")
        sys.exit(1)
