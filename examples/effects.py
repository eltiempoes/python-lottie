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


last_frame = 120
an = parse_svg_file(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "blep.svg"),
    last_frame
)

gaussian = objects.effects.GaussianBlurEffect()
an.layers[0].effects = [
    #objects.effects.TritoneEffect(Color(1, 0, 0), Color(0, 1, 0), Color(0, 0, 1)),
    #objects.effects.FillEffect(color=Color(1, 0, 0), opacity=0.5)
    objects.effects.DropShadowEffect(Color(0, 0, 0), 128, 135, 10, 7),
    objects.effects.TintEffect(Color(0, 0, 0), Color(0, 1, 0), 90),
    gaussian,
]
gaussian.sigma.add_keyframe(last_frame/2, 0)
gaussian.sigma.add_keyframe(last_frame*3/4, 25)
gaussian.sigma.add_keyframe(last_frame, 0)

exporters.multiexport(an, "/tmp/effects")
