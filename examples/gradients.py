import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.utils import script
from tgs import objects
from tgs import Color, Point


an = objects.Animation(59)

layer = objects.ShapeLayer()
an.add_layer(layer)

g1 = layer.add_shape(objects.Group())

circle = g1.add_shape(objects.Ellipse())
circle.size.value = Point(100, 100)
circle.position.value = Point(128, 256)


fill = g1.add_shape(objects.GradientFill())
fill.start_point.value = Point(100, 0)
fill.end_point.value = Point(200, 0)
fill.colors.set_colors([Color(1, 0, 0), Color(1, 1, 0)])


stroke = g1.add_shape(objects.GradientStroke(5))
stroke.start_point.value = Point(100, 0)
stroke.end_point.value = Point(200, 0)
stroke.colors.add_keyframe(0, [Color(1, 0, 0), Color(1, 1, 0)])
stroke.colors.add_keyframe(10, [Color(1, 1, 0), Color(0, 1, 0)])
stroke.colors.add_keyframe(30, [Color(1, 0, 1), Color(0, 0, 1)])
stroke.colors.add_keyframe(59, [Color(1, 0, 0), Color(1, 1, 0)])
stroke.colors.count = 2
stroke.width.value = 10



g2 = layer.add_shape(objects.Group())

circle = g2.add_shape(objects.Ellipse())
circle.size.value = Point(200, 200)
circle.position.value = Point(128+256, 256)


fill = g2.add_shape(objects.GradientFill())
fill.gradient_type = objects.GradientType.Radial
fill.start_point.value = Point(128+256, 256)
fill.end_point.value = Point(128+256+100, 256)
fill.colors.set_colors([Color(1, 0, 0), Color(1, 1, 0)])
#fill.highlight_length.add_keyframe(0, -50)
#fill.highlight_length.add_keyframe(30, 50)
#fill.highlight_length.add_keyframe(59, -50)
#fill.highlight_angle.value = 45
fill.highlight_length.value = 90


script.script_main(an)
