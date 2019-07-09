#!/usr/bin/env python3

import json
import sys
from io import StringIO
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))

from tgs.utils.linediff import difflines_str

a = json.load(open(sys.argv[1]))
ioa = StringIO()
json.dump(a, ioa, indent=4, sort_keys=True)

b = json.load(open(sys.argv[2]))
iob = StringIO()
json.dump(b, iob, indent=4, sort_keys=True)

difflines_str(ioa.getvalue(), iob.getvalue())
