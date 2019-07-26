#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.parsers.svg.importer import parse_color

print(parse_color(sys.argv[1]).components)

