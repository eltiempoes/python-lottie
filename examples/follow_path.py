#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.utils import script
from lottie import objects
from lottie.utils.animation import follow_path
from lottie import Point, Color

an = objects.Animation(180)

layer = objects.ShapeLayer()
an.add_layer(layer)

group = layer.add_shape(objects.Group())
ball = group.add_shape(objects.Ellipse())
ball.size.value = Point(10, 10)

r1 = group.add_shape(objects.Rect())
r1.size.value = Point(50, 10)

r2 = group.add_shape(objects.Group())
r2.add_shape(objects.Rect()).size.value = Point(50, 10)
r2 = r2.transform

group.add_shape(objects.Fill(Color(0, 1, 0)))

group = layer.add_shape(objects.Group())
bez = group.add_shape(objects.Path())
bez.shape.value.add_point(Point(256, 128), Point(0, 0), Point(64, 64))
bez.shape.value.add_point(Point(256, 256), Point(-64, -64), Point(-64, 64))
bez.shape.value.add_point(Point(256, 256+120), Point(0, 0), Point(0, 0))
group.add_shape(objects.Stroke(Color(1, 0, 0), 10))

follow_path(ball.position, bez.shape.value,  0,  90, 30, False, Point(0, 0))
follow_path(ball.position, bez.shape.value, 90, 180, 30,  True, Point(0, 0))

follow_path(r1.position, bez.shape.value,  0,  90, 30, False, Point(150, 0))
follow_path(r1.position, bez.shape.value, 90, 180, 30,  True, Point(150, 0))

follow_path(r2.position, bez.shape.value,  0,  90, 30, False, Point(-150, 0), 0, r2.rotation, 90)
follow_path(r2.position, bez.shape.value, 90, 180, 30,  True, Point(-150, 0), 0, r2.rotation, 90)

script.script_main(an)
