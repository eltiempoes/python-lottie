import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.utils import script
from tgs import objects
from tgs.utils.animation import follow_path
from tgs import Point, Color

an = objects.Animation(180)

layer = objects.ShapeLayer()
an.add_layer(layer)

group = layer.add_shape(objects.Group())
ball = group.add_shape(objects.Ellipse())
ball.size.value = Point(10, 10)
group.add_shape(objects.Fill(Color(0, 1, 0)))

group = layer.add_shape(objects.Group())
bez = group.add_shape(objects.Path())
bez.shape.value.add_point(Point(256, 128), Point(0, 0), Point(64, 64))
bez.shape.value.add_point(Point(256, 256), Point(-64, -64), Point(-64, 64))
bez.shape.value.add_point(Point(256, 256+120), Point(0, 0), Point(0, 0))
group.add_shape(objects.Stroke(Color(1, 0, 0), 10))

follow_path(ball.position, bez.shape.value, 0, 90, 30)
follow_path(ball.position, bez.shape.value, 90, 180, 30, True)


script.script_main(an)
