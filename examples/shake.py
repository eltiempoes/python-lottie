#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.utils import script
from lottie import objects
from lottie.utils.animation import shake, rot_shake
from lottie import Point, Color

an = objects.Animation(59)

layer = objects.ShapeLayer()
an.add_layer(layer)

circle = layer.add_shape(objects.Ellipse())
circle.size.value = Point(100, 100)
circle.position.value = Point(256, 128)

shake(circle.position, 10, 15, 0, 59, 25)


g = layer.add_shape(objects.Group())
box = g.add_shape(objects.Rect())
box.size.value = Point(200, 100)
g.transform.anchor_point.value = g.transform.position.value = box.position.value = Point(256, 384)
rot_shake(g.transform.rotation, Point(-15, 15), 0, 60, 10)


layer.add_shape(objects.Fill(Color(1, 1, 0)))


script.script_main(an)
