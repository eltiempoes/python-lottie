#!/usr/bin/env python3

import json
import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.exporters import prettyprint
from tgs.objects import Animation


prettyprint(Animation.load(json.load(open(sys.argv[1]))))

