import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.utils.animation import spring_pull


an = objects.Animation(100)

layer = objects.ShapeLayer()
an.add_layer(layer)

settings = [
    ([1,  1, 0], 128, 7),
    ([1,  0, 0], 256, 15),
    ([0, .5, 1], 384, 30),
]

for color, x, falloff in settings:
    group = layer.add_shape(objects.Group())
    ball = group.add_shape(objects.Ellipse())
    ball.size.value = [100, 100]
    group.add_shape(objects.Fill(color))
    group.transform.position.value = [x, -100]
    spring_pull(group.transform.position, [x, 256], 0, 60, falloff, 7)
    group.transform.position.add_keyframe(85, [x, -100])




exporters.multiexport(an, "/tmp/spring")

