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
from lottie.utils.linediff import difflines_str
from lottie.parsers.tgs import parse_tgs_json


parser = argparse.ArgumentParser(
    description="Pretty prints two JSON files side by side, highlighting differences (useful to debug / diff lottie files)",
)
parser.add_argument(
    "file1",
    help="Left file"
)
parser.add_argument(
    "file2",
    help="Right file"
)

if __name__ == "__main__":
    ns = parser.parse_args()
    a = parse_tgs_json(ns.file1)
    ioa = StringIO()
    json.dump(a, ioa, indent=4, sort_keys=True)

    b = parse_tgs_json(ns.file2)
    iob = StringIO()
    json.dump(b, iob, indent=4, sort_keys=True)

    difflines_str(ioa.getvalue(), iob.getvalue())
