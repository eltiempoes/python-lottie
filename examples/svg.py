#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.utils import script
from tgs import objects
from tgs.parsers.svg import parse_svg_file
from tgs import Point


an = parse_svg_file(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "blep.svg"
))

layer = an.find("durg")
layer.transform.anchor_point.value = Point(256, 256)
layer.transform.position.value = Point(256, 256)
layer.transform.rotation.add_keyframe(0, 0)
layer.transform.rotation.add_keyframe(30, 180)
layer.transform.rotation.add_keyframe(60, 360)


script.script_main(an)
