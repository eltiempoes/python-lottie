#!/usr/bin/env python3

import sys
import json
from io import StringIO
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))

from tgs.parsers.tgs import parse_tgs_json

a = parse_tgs_json(sys.argv[1])
json.dump(a, sys.stdout, indent=4, sort_keys=True)
