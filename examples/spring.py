import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.utils.animation import spring_pull
from tgs import NVector


an = objects.Animation(100)

layer = objects.ShapeLayer()
an.add_layer(layer)

settings = [
    (NVector(1,  1, 0), 128, 7),
    (NVector(1,  0, 0), 256, 15),
    (NVector(0, .5, 1), 384, 30),
]

for color, x, falloff in settings:
    group = layer.add_shape(objects.Group())
    ball = group.add_shape(objects.Ellipse())
    ball.size.value = NVector(100, 100)
    group.add_shape(objects.Fill(color))
    group.transform.position.value = NVector(x, -100)
    spring_pull(group.transform.position, NVector(x, 256), 0, 60, falloff, 7)
    group.transform.position.add_keyframe(85, NVector(x, -100))


exporters.multiexport(an, "/tmp/spring")
