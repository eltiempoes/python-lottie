#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.utils import script
from tgs import objects
from tgs import Color, Point
from tgs.utils.font import FontShape


an = objects.Animation(120)
layer = objects.ShapeLayer()
an.add_layer(layer)

t = layer.add_shape(FontShape("Hello\nWorld\nF\U0001F600O", "Ubuntu", 128))
t.refresh()
t.wrapped.transform.position.value.y += t.line_height
layer.add_shape(objects.Fill(Color(0, 0, 0)))
layer.add_shape(objects.Stroke(Color(1, 1, 1), 2))

script.script_main(an)
