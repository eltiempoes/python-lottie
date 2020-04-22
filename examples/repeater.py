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

group = layer.add_shape(objects.Group())

star = group.add_shape(objects.Star())
star.inner_radius.value = 20
star.outer_radius.value = 50
star.position.value = Point(91, 91)

fill = group.add_shape(objects.Fill(Color(1, 1, 0)))
stroke = group.add_shape(objects.Stroke(Color(0, 0, 0), 5))

repeater = layer.add_shape(objects.Repeater(4))
repeater.transform.position.value.x = 110
repeater.transform.end_opacity.value = 20

repeater1 = layer.add_shape(objects.Repeater(4))
repeater1.transform.position.value = Point(0, 110)
repeater1.transform.end_opacity.value = 20

script.script_main(an)

