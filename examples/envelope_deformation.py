import sys
import os
import math
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.utils import animation as anutils
from tgs import NVector


an = objects.Animation(60)

layer = objects.ShapeLayer()
an.add_layer(layer)

heart = objects.Bezier()
heart.add_point(NVector(50, 20), NVector(50, -20), NVector(-50, -20))
heart.add_smooth_point(NVector(0, 50), NVector(-5, -10))
heart.add_smooth_point(NVector(50, 100), NVector(-10, 0))
heart.add_smooth_point(NVector(100, 50), NVector(-5, 10))
heart.closed = True

g1 = layer.add_shape(objects.Group())
shape = g1.add_shape(objects.Shape())
shape.vertices.value = heart
fill = layer.add_shape(objects.Fill([1, 0, 0]))
stroke = layer.add_shape(objects.Stroke([0, 0, 0], 5))



g2 = layer.add_shape(objects.Group())
bb = shape.bounding_box()
shapeb = g2.add_shape(objects.Shape())
shapeb.vertices.value.add_point(NVector(bb.x1, bb.y1))
shapeb.vertices.value.add_point(NVector(bb.x2, bb.y1))
shapeb.vertices.value.add_point(NVector(bb.x2, bb.y2))
shapeb.vertices.value.add_point(NVector(bb.x1, bb.y2))
fill = layer.add_shape(objects.Fill([1, 1, 0]))


env = anutils.EnvelopeDeformation(NVector(bb.x1, bb.y1), NVector(bb.x2, bb.y2))

env.add_keyframe(
    0,
    NVector(256-128, 256-128),
    NVector(256+128, 256-128),
    NVector(256+128, 256+128),
    NVector(256-128, 256+128),
)

env.add_keyframe(
    30,
    NVector(256, 256-64),
    NVector(256, 256-128-64),
    NVector(256, 256+128+64),
    NVector(256, 256+64),
)
env.add_keyframe(
    60,
    NVector(256+128, 256-128),
    NVector(256-128, 256-128),
    NVector(256-128, 256+128),
    NVector(256+128, 256+128),
)

env.animate_bezier(shape.vertices)
env.animate_bezier(shapeb.vertices)


exporters.multiexport(an, "/tmp/envelope_deformation")

