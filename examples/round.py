import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.utils import script
from tgs import objects
from tgs import Point, Color


last_frame = 180
an = objects.Animation(last_frame)

layer = objects.ShapeLayer()
an.add_layer(layer)

group = layer.add_shape(objects.Group())

star = group.add_shape(objects.Star())
star.inner_radius.value = 40
star.outer_radius.value = 100
star.position.value = Point(256, 256)

star = group.add_shape(objects.Star())
star.inner_radius.value = 20
star.outer_radius.value = 50
star.position.value = Point(256, 256)

round = layer.add_shape(objects.Round())
round.radius.add_keyframe(0, 0)
round.radius.add_keyframe(last_frame/2, 30)
round.radius.add_keyframe(last_frame, 0)

stroke = group.add_shape(objects.Stroke(Color(1, 1, 0), 10))


script.script_main(an)

