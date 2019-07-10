#!/usr/bin/env python3

import gzip
import json
import sys

inf = sys.stdin.buffer
outf = sys.stdout

if len(sys.argv) > 1 and sys.argv[1] != "-":
    inf = sys.argv[1]

if len(sys.argv) > 2 and sys.argv[2] != "-":
    outf = open(sys.argv[2], "w")


with gzip.open(inf, "rb") as unzipped:
    json.dump(
        json.load(unzipped),
        outf,
        indent=4
    )
