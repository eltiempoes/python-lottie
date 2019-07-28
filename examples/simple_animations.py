import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.utils import script
from tgs import objects
from tgs import Point, Color


an = objects.Animation(59)

layer = objects.ShapeLayer()
an.add_layer(layer)

circle = layer.add_shape(objects.Ellipse())
circle.size.value = Point(100, 100)
circle.position.add_keyframe(0, Point(0, 256))
circle.position.add_keyframe(20, Point(256, 256))
circle.position.add_keyframe(40, Point(256, 0))
circle.position.add_keyframe(60, Point(0, 256))


fill = layer.add_shape(objects.Fill(Color(1, 1, 0)))
fill.opacity.add_keyframe(0, 100)
fill.opacity.add_keyframe(30, 10)
fill.opacity.add_keyframe(60, 100)


script.script_main(an)


