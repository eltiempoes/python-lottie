#!/usr/bin/env python3
import os
import sys
import math
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.utils import script
from lottie import objects
from lottie.nvector import Point, PolarVector
from lottie.utils import color


an = objects.Animation(59)

layer = objects.ShapeLayer()
an.add_layer(layer)


bezier = objects.Bezier()
radius = 128
angle = -math.pi / 2
for i in range(5+1):
    bezier.add_point(PolarVector(radius, angle))
    angle += 2 * math.pi * 2 / 5
bezier.closed = True
bezier.reverse()

g = layer.add_shape(objects.Group())
g.transform.position.value = Point(radius, radius)
g.add_shape(objects.Path(bezier))
fill = g.add_shape(objects.Fill(color.from_uint8(255, 0, 100)))
fill.fill_rule = objects.FillRule.NonZero

g = layer.add_shape(objects.Group())
g.transform.position.value = Point(512-radius, 512-radius)
g.add_shape(objects.Path(bezier))
fill = g.add_shape(objects.Fill(color.from_uint8(255, 100, 0)))
fill.fill_rule = objects.FillRule.EvenOdd

script.script_main(an)

