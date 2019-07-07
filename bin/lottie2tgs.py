#!/usr/bin/env python3

import gzip
import json
import sys
import codecs

inf = sys.stdin
outf = sys.stdout

if len(sys.argv) > 1 and sys.argv[1] != "-":
    inf = open(sys.argv[1], "r")

if len(sys.argv) > 2 and sys.argv[2] != "-":
    outf = sys.argv[2]


data = json.load(inf)
data["tgs"] = 1

with gzip.open(outf, "wb") as fil:
    json.dump(data, codecs.getwriter('utf-8')(fil))

