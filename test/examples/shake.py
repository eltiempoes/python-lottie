import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.utils.animation import shake

an = objects.Animation(59)

layer = objects.ShapeLayer()
an.add_layer(layer)

circle = layer.add_shape(objects.Ellipse())
circle.size.value = [100, 100]
circle.position.value = [256, 256]

shake(circle, 10, 15, 0, 59, 25)


layer.add_shape(objects.Fill([1, 1, 0]))


exporters.multiexport(an, "/tmp/shake")
