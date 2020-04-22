#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.utils import script
from lottie import objects
from lottie import Point, Color

an = objects.Animation(59)

layer = objects.ShapeLayer()
an.add_layer(layer)


g1 = layer.add_shape(objects.Group())
circle = g1.add_shape(objects.Ellipse())
circle.size.value = Point(100, 100)
circle.position.value = Point(200, 100)
g1.add_shape(objects.Fill(Color(1, 0, 0)))
g1.add_shape(objects.Stroke(Color(0, 0, 0), 5))

g2 = layer.add_shape(objects.Group())
star = g2.add_shape(objects.Star())
star.inner_radius.value = 20
star.outer_radius.value = 50
star.position.value = Point(300, 100)
g2.add_shape(objects.Fill(Color(0, 1, 0)))
g2.add_shape(objects.Stroke(Color(0, 0, 0), 5))

g3 = layer.add_shape(objects.Group())
rect = g3.add_shape(objects.Rect())
rect.size.value = Point(100, 100)
rect.position.value = Point(100, 100)
g3.add_shape(objects.Fill(Color(0, 0, 1)))
g3.add_shape(objects.Stroke(Color(1, 1, 1), 5))


script.script_main(an)
