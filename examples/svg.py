import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.parsers.svg import parse_svg_file
from tgs import NVector


an = parse_svg_file(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "blep.svg"
))

layer = an.find("durg")
layer.transform.anchor_point.value = NVector(256, 256)
layer.transform.position.value = NVector(256, 256)
layer.transform.rotation.add_keyframe(0, 0)
layer.transform.rotation.add_keyframe(30, 180)
layer.transform.rotation.add_keyframe(60, 360)


exporters.multiexport(an, "/tmp/svg")
