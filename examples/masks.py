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


maskshape = objects.Star()
maskshape.inner_radius.value = 100
maskshape.outer_radius.value = 200
maskshape.rotation.value = 180
maskshape.position.value = Point(256, 256)
#maskshape.size.value = Point(256, 256)
maskbez = maskshape.to_bezier()

mask = objects.Mask(maskbez.shape.value)
an.layers[0].masks = [mask]


g = an.layers[0].add_shape(objects.Group())
r = g.add_shape(objects.Rect())
r.position.value = Point(256, 256)
r.size.value = Point(512, 512)
g.add_shape(objects.Fill(Color(1, 1, 1)))


script.script_main(an)
