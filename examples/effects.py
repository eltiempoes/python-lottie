"""
@note Effects are not supported by telegram
"""
import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.parsers.svg import parse_svg_file
from tgs import Point, Color


an = parse_svg_file(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "blep.svg"
))

gaussian = objects.effects.GaussianBlurEffect()
an.layers[0].effects = [gaussian]
gaussian.sigma.add_keyframe(0, 0)
gaussian.sigma.add_keyframe(30, 25)
gaussian.sigma.add_keyframe(60, 0)


exporters.multiexport(an, "/tmp/effects")
