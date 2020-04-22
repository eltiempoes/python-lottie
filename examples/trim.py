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


last_frame = 60
an = objects.Animation(last_frame)

layer = objects.ShapeLayer()
an.add_layer(layer)

group = layer.add_shape(objects.Group())

star = objects.Star()
star.inner_radius.value = 40
star.outer_radius.value = 100
star.position.value = Point(256, 256)
star.name = "big start"
group.add_shape(star)

star = objects.Star()
star.inner_radius.value = 20
star.outer_radius.value = 50
star.position.value = Point(256, 256)
star.name = "small start"
group.add_shape(star)

obj = objects.Path()
obj.shape.value.add_point(Point(10, 10))
obj.shape.value.add_point(Point(500, 10))
group.add_shape(obj)

trim = layer.add_shape(objects.Trim())
#trim.offset.value = 350
trim.offset.add_keyframe(0, 0)
trim.offset.add_keyframe(last_frame, 360)
trim.start.value = 0
trim.end.value = 50
#trim.multiple = objects.TrimMultipleShapes.Individually

stroke = group.add_shape(objects.Stroke(Color(1, 1, 0), 10))

script.script_main(an)
