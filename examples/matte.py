#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.utils import script
from lottie import objects
from lottie.parsers.svg import parse_svg_file
from lottie import Point, Color


an = parse_svg_file(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "blep.svg"
))

layer = an.insert_layer(0, objects.ShapeLayer())
r = layer.add_shape(objects.Rect())
r.position.value = Point(256, 256)
r.size.value = Point(512, 512)
gf = layer.add_shape(objects.GradientFill([(0, Color(1, 1, 1)), (1, Color(0, 0, 0))]))
gf.start_point.value = Point(256, 256)
gf.end_point.value = Point(256, 64)

an.layers[-1].matte_mode = objects.MatteMode.Luma


script.script_main(an)

