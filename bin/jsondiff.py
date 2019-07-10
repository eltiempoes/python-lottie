#!/usr/bin/env python3

import sys
import json
from io import StringIO
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))

from tgs.utils.linediff import difflines_str
from tgs.parsers.tgs import parse_tgs_json

a = parse_tgs_json(sys.argv[1])
ioa = StringIO()
json.dump(a, ioa, indent=4, sort_keys=True)

b = parse_tgs_json(sys.argv[2])
iob = StringIO()
json.dump(b, iob, indent=4, sort_keys=True)

difflines_str(ioa.getvalue(), iob.getvalue())
