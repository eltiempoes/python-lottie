"""
@note Text layers are not supported by telegram
"""
import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.utils import script
from tgs import objects
from tgs import Color, Point



an = objects.Animation(120)
an.fonts = objects.text.FontList()
an.fonts.append(objects.text.Font("sans", name="sans"))
layer = objects.TextLayer()
an.add_layer(layer)
layer.data.add_keyframe(0, objects.text.TextItem("Text", 200, Color(1, 0, 0), "sans"))
layer.data.add_keyframe(60, objects.text.TextItem("Here", 200, Color(0, 1, 0), "sans"))
layer.transform.position.value = Point(30, 200)


script.script_main(an)
