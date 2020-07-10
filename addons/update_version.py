#!/usr/bin/env python3

import sys
import os
import re

blender_addon_dir = os.path.join(os.path.dirname(__file__), "blender", "lottie_io")
sys.path.insert(0, blender_addon_dir)
import lottie

tup = repr(lottie.version_tuple)


with open(os.path.join(blender_addon_dir, "__init__.py")) as f:
    data_in = f.read()

data_out = re.sub("(version\": )(.*),", "\\1%s," % tup, data_in)

with open(os.path.join(blender_addon_dir, "__init__.py"), "w") as f:
    f.write(data_out)
