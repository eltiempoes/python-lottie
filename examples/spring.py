#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.utils import script
from lottie import objects
from lottie.utils.animation import spring_pull
from lottie import Point, Color


an = objects.Animation(100)

layer = objects.ShapeLayer()
an.add_layer(layer)

settings = [
    (Color(1,  1, 0), 128, 7),
    (Color(1,  0, 0), 256, 15),
    (Color(0, .5, 1), 384, 30),
]

for color, x, falloff in settings:
    group = layer.add_shape(objects.Group())
    ball = group.add_shape(objects.Ellipse())
    ball.size.value = Point(100, 100)
    group.add_shape(objects.Fill(color))
    group.transform.position.value = Point(x, -100)
    spring_pull(group.transform.position, Point(x, 256), 0, 60, falloff, 7)
    group.transform.position.add_keyframe(85, Point(x, -100))


script.script_main(an)
