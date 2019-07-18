import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.utils import animation as anutils
from tgs import Point, Color


an = objects.Animation(180)

layer = objects.ShapeLayer()
an.add_layer(layer)

group = layer.add_shape(objects.Group())
bez = group.add_shape(objects.Shape())
bez.vertices.value.add_point(Point(256, 128), Point(0, 0), Point(64, 64))
bez.vertices.value.add_smooth_point(Point(256, 256+120), Point(32, -32))
bez.vertices.value.add_point(Point(256, 256), Point(-64, -64), Point(-64, 64))
bez.vertices.value.add_point(Point(128, 256+120), Point(64, 64), Point(0, 0))
group.add_shape(objects.Stroke(Color(1, 0, 0), 10))


group = layer.add_shape(objects.Group())
sh = anutils.generate_path_segment(bez.vertices.value, 0, 180, 60, 180, 60, True)
group.add_shape(sh)
group.add_shape(objects.Stroke(Color(0, 1, 0), 20))


exporters.multiexport(an, "/tmp/bezier_segment")

