#!/usr/bin/env python3

import sys
import json
from io import StringIO
import os
import argparse
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))

from lottie.parsers.tgs import parse_tgs_json


parser = argparse.ArgumentParser(
    description="Pretty prints a JSON file (or gzipped JSON file), useful to debug / diff lottie files",
)
parser.add_argument(
    "infile",
    help="Input file"
)
parser.add_argument(
    "--no-sort",
    action="store_false",
    help="Don't sort keys",
    dest="sort"
)

if __name__ == "__main__":
    ns = parser.parse_args()
    infile = ns.infile
    if infile == "-":
        infile = sys.stdin
    a = parse_tgs_json(infile)
    json.dump(a, sys.stdout, indent=4, sort_keys=ns.sort)
