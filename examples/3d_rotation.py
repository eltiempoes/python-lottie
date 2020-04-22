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
from lottie import Point, Color, Point3D, Size

an = objects.Animation(120)

layer = objects.ShapeLayer()
an.add_layer(layer)

# Build a sphere out of circles
balls = []
axes = [
    Point(1, 0),
    Point(0, 1),
]
for i in range(20):
    a = i/20 * math.pi * 2
    for axis in axes:
        g = layer.add_shape(objects.Group())
        b = g.add_shape(objects.Ellipse())
        b.size.value = Size(20, 20)
        xz = axis * math.sin(a)*128
        pos = Point3D(256+xz[0], 256+math.cos(a)*128, xz[1])
        b.position.value = pos
        balls.append(b)
        g.add_shape(objects.Fill(Color(0, 1, 0)))

# Animate the circles using depth rotation
dr = anutils.DepthRotationDisplacer(Point3D(256, 256, 0), 0, 120, 10, Point3D(0, 2, -1))
for b in balls:
    dr.animate_point(b.position)

script.script_main(an)
