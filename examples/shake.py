import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.utils.animation import shake, rot_shake
from tgs import NVector

an = objects.Animation(59)

layer = objects.ShapeLayer()
an.add_layer(layer)

circle = layer.add_shape(objects.Ellipse())
circle.size.value = NVector(100, 100)
circle.position.value = NVector(256, 128)

shake(circle.position, 10, 15, 0, 59, 25)


g = layer.add_shape(objects.Group())
box = g.add_shape(objects.Rect())
box.size.value = NVector(200, 100)
g.transform.anchor_point.value = g.transform.position.value = box.position.value = NVector(256, 384)
rot_shake(g.transform.rotation, NVector(-15, 15), 0, 60, 10)


layer.add_shape(objects.Fill(NVector(1, 1, 0)))


exporters.multiexport(an, "/tmp/shake")
