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

last_frame = 120
an = objects.Animation(last_frame)
layer = objects.ShapeLayer()
an.add_layer(layer)


def f(x):
    return -64*x/400+64


def fp(x, offset):
    return Point(x, offset+f(x))


def displace(f):
    return Point(0, math.cos(f*math.pi*2)*80)


handle_length = 30


def setup(offset, exp):
    g = layer.add_shape(objects.Group())
    shape1 = g.add_shape(objects.Path())
    bez1 = shape1.shape.value
    g.transform.opacity.value = 60
    g.add_shape(objects.Fill(Color(0, 1, 1)))

    g = layer.add_shape(objects.Group())
    shape2 = g.add_shape(objects.Path())
    bez2 = shape2.shape.value
    g.add_shape(objects.Fill(Color(0, 0, 1)))

    for i in range(6):
        p1 = Point(300/5 * i, offset-(1-(300/5 * i)/300)*16+16)
        p2 = Point(400/5 * i, offset - f(400/5 * i))

        if i == 5:
            t2 = Point(0, 0)
            t1 = Point(0, 0)
        else:
            t2 = Point(400/5 * i - handle_length, offset - f(400/5 * i - handle_length)) - p2
            t1 = Point(300/5 * i - handle_length, offset-(1-(300/5 * i - handle_length)/300)*16+16) - p1

        bez1.add_smooth_point(p1, t1)
        bez2.add_smooth_point(p2, t2)

    for i in range(4, -1, -1):
        p1 = fp(300/5 * i, offset)
        t1 = fp(300/5 * i + handle_length, offset) - p1
        bez1.add_smooth_point(p1, t1)

        p2 = fp(400/5 * i, offset)
        t2 = fp(400/5 * i + handle_length, offset) - p2
        bez2.add_smooth_point(p2, t2)

    displacer = anutils.FollowDisplacer(Point(400, offset), 200, displace, 0, last_frame, 10, exp)
    displacer.animate_bezier(shape1.shape)
    displacer.animate_bezier(shape2.shape)


setup(128, 1/2)
setup(256, 1)
setup(256+128, 2)


script.script_main(an)
