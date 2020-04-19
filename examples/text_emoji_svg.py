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
from tgs.utils.font import FontStyle


an = objects.Animation(120)
layer = objects.ShapeLayer()
an.add_layer(layer)

# The font name "Ubuntu" here, can be detected among the system fonts if fontconfig is available
# Otherwise you can use the full path to the font file
# `emoji_svg` needs to point to a directory with the supported emoji as svg
style = FontStyle("Ubuntu", 128, emoji_svg="twemoji/assets/svg/")
t = layer.add_shape(style.render("Hello\nWorld\nF\U0001F600O\nE🇪🇺U"))
t.transform.position.value.y += t.line_height
layer.add_shape(objects.Fill(Color(0, 0, 0)))
layer.add_shape(objects.Stroke(Color(1, 1, 1), 2))

script.script_main(an)

