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
from lottie.utils import color


an = objects.Animation(59)

layer = objects.ShapeLayer()
an.add_layer(layer)

heart = objects.Bezier()
heart.add_point(Point(50, 20), Point(50, -20), Point(-50, -20))
heart.add_smooth_point(Point(0, 50), Point(-5, -10))
heart.add_smooth_point(Point(50, 100), Point(-10, 0))
heart.add_smooth_point(Point(100, 50), Point(-5, 10))
heart.closed = True
antiheart = (
    objects.Bezier()
    .add_smooth_point(Point(50, 0), Point(10, 0))
    .add_smooth_point(Point(0, 50), Point(0, -20))
    .add_point(Point(50, 80), Point(-50, 20), Point(50, 20))
    .add_smooth_point(Point(100, 50), Point(0, 20))
    .close()
)

g1 = layer.add_shape(objects.Group())
g1.transform.position.value = Point(100, 200)
shape = g1.add_shape(objects.Path())
shape.shape.value = heart

g2 = layer.add_shape(objects.Group())
g2.transform.position.value = Point(300, 200)
animated = g2.add_shape(objects.Path())
animated.shape.add_keyframe(0, heart)
animated.shape.add_keyframe(30, antiheart)
animated.shape.add_keyframe(59, heart)


fill = layer.add_shape(objects.Fill(color.from_uint8(255, 0, 0)))
stroke = layer.add_shape(objects.Stroke(Color(0, 0, 0), 5))


script.script_main(an)
