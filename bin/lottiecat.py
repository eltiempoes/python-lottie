#!/usr/bin/env python3

import json
import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.exporters import prettyprint, prettyprint_summary
from tgs.objects import Animation


prettyprint_summary(Animation.load(json.load(open(sys.argv[1]))))

