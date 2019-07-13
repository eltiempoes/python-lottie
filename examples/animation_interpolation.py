import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.objects import interpolation

an = objects.Animation(180)

layer = objects.ShapeLayer()
an.add_layer(layer)

interpolations = [
    interpolation.Linear(),
    interpolation.EaseIn(),
    interpolation.Sigmoid(),
    interpolation.Jump(),
]
height = 512 / len(interpolations)
width = height

for i in range(len(interpolations)):
    rect = layer.add_shape(objects.Rect())
    rect.size.value = [width, height]
    y = i * height + height / 2
    rect.position.add_keyframe(0, [width/2, y])
    rect.position.add_keyframe(90, [512-width/2, y], interpolations[i])
    rect.position.add_keyframe(180, [width/2, y], interpolations[i])

layer.add_shape(objects.Fill([1, 0, 0]))

exporters.multiexport(an, "/tmp/animation_interpolation")

