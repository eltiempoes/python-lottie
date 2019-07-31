import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.utils import script
from tgs import objects
from tgs import Color, Point
from tgs.utils.font import fonts


an = objects.Animation(120)
layer = objects.ShapeLayer()
an.add_layer(layer)

g = layer.add_shape(fonts["Ubuntu"]["Regular"].render(128, "Hello\nWorld"))
g.transform.position.value.y = g.line_height
layer.add_shape(objects.Fill(Color(0, 0, 0)))
layer.add_shape(objects.Stroke(Color(1, 1, 1), 8))

script.script_main(an)
