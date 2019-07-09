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


a1 = Animation.load(json.load(open(sys.argv[1])))
a2 = Animation.load(json.load(open(sys.argv[2])))
difflines(a1, a2)
