#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
import math
from lottie.utils import script
from lottie import objects
from lottie.parsers.svg import parse_svg_file
from lottie.utils.color import ManagedColor

last_frame = 60
an = parse_svg_file(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "blep.svg"
), 0, last_frame)

layer = an.find("durg")

n_frames = 24
for fill in layer.find_all((objects.Fill, objects.Stroke)):
    color = ManagedColor.from_color(fill.color.value)
    color.convert(ManagedColor.Mode.LCH_uv)

    for frame in range(n_frames):
        off = frame / (n_frames-1)
        color.hue = (color.hue + math.tau / (n_frames-1)) % math.tau
        fill.color.add_keyframe(off * last_frame, color.converted(ManagedColor.Mode.RGB).vector)


script.script_main(an)
