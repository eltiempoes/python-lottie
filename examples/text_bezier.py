#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.utils import script
from lottie import objects
from lottie import Color, Point
from lottie.utils.font import FontShape


an = objects.Animation(120)
layer = objects.ShapeLayer()
an.add_layer(layer)

# The font name "Ubuntu" here, can be detected among the system fonts if fontconfig is available
# Otherwise you can use the full path to the font file
t = layer.add_shape(FontShape("Hello\nWorld\nF\U0001F600O", "Ubuntu", 128))
t.refresh()
t.wrapped.transform.position.value.y += t.line_height
layer.add_shape(objects.Fill(Color(0, 0, 0)))
layer.add_shape(objects.Stroke(Color(1, 1, 1), 2))

script.script_main(an)
