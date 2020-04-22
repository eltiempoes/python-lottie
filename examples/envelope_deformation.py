#!/usr/bin/env python3
import sys
import os
import math
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.utils import script
from lottie import objects
from lottie.utils import animation as anutils
from lottie import Point, Color


an = objects.Animation(60)

layer = objects.ShapeLayer()
an.add_layer(layer)

heart = objects.Bezier()
heart.add_point(Point(50, 20), Point(50, -20), Point(-50, -20))
heart.add_smooth_point(Point(0, 50), Point(-5, -10))
heart.add_smooth_point(Point(50, 100), Point(-10, 0))
heart.add_smooth_point(Point(100, 50), Point(-5, 10))
heart.closed = True

g1 = layer.add_shape(objects.Group())
shape = g1.add_shape(objects.Path())
shape.shape.value = heart
fill = layer.add_shape(objects.Fill(Color(1, 0, 0)))
stroke = layer.add_shape(objects.Stroke(Color(0, 0, 0), 5))



g2 = layer.add_shape(objects.Group())
bb = shape.bounding_box()
shapeb = g2.add_shape(objects.Path())
shapeb.shape.value.add_point(Point(bb.x1, bb.y1))
shapeb.shape.value.add_point(Point(bb.x2, bb.y1))
shapeb.shape.value.add_point(Point(bb.x2, bb.y2))
shapeb.shape.value.add_point(Point(bb.x1, bb.y2))
fill = layer.add_shape(objects.Fill([1, 1, 0]))


env = anutils.EnvelopeDeformation(Point(bb.x1, bb.y1), Point(bb.x2, bb.y2))

env.add_keyframe(
    0,
    Point(256-128, 256-128),
    Point(256+128, 256-128),
    Point(256+128, 256+128),
    Point(256-128, 256+128),
)

env.add_keyframe(
    30,
    Point(256, 256-64),
    Point(256, 256-128-64),
    Point(256, 256+128+64),
    Point(256, 256+64),
)
env.add_keyframe(
    60,
    Point(256+128, 256-128),
    Point(256-128, 256-128),
    Point(256-128, 256+128),
    Point(256+128, 256+128),
)

env.animate_bezier(shape.shape)
env.animate_bezier(shapeb.shape)


script.script_main(an)

