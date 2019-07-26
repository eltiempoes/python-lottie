#!/usr/bin/env python3

import json
import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.utils.linediff import difflines
from tgs.objects import Animation
from tgs.parsers.tgs import parse_tgs


a1 = parse_tgs(sys.argv[1])
a2 = parse_tgs(sys.argv[2])
difflines(a1, a2)
