#!/usr/bin/env python3

import sys
import json
from io import StringIO
import os
import argparse
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))

from tgs.parsers.tgs import parse_tgs_json


parser = argparse.ArgumentParser(
    description="Pretty prints a JSON file (or gzipped JSON file), useful to debug / diff lottie files",
)
parser.add_argument(
    "infile",
    help="Input file"
)

if __name__ == "__main__":
    ns = parser.parse_args()
    a = parse_tgs_json(ns.infile)
    json.dump(a, sys.stdout, indent=4, sort_keys=True)
