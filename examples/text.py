#!/usr/bin/env python3
"""
@note Text layers are not supported by telegram
"""
import sys
import os
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.utils import script
from lottie import objects
from lottie import Color, Point


an = objects.Animation(120)
an.fonts = objects.text.FontList()
an.fonts.append(objects.text.Font("sans", name="sans"))
layer = objects.TextLayer()
an.add_layer(layer)

layer.data.add_keyframe(0, objects.text.TextDocument("Text", 200, Color(1, 0, 0), "sans"))
layer.data.add_keyframe(60, objects.text.TextDocument("Here", 200, Color(0, 1, 0), "sans"))
layer.transform.position.value = Point(30, 200)


script.script_main(an)
