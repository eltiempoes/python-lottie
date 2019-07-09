import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "lib"
))
from tgs import exporters
from tgs import objects


an = objects.Animation(59)

layer = objects.ShapeLayer()
an.add_layer(layer)

circle = layer.add_shape(objects.Ellipse())
circle.size.value = [100, 100]
circle.position.value = [256, 256]


fill = layer.add_shape(objects.GradientFill())
fill.start_point.value = [200, 0]
fill.end_point.value = [300, 0]
fill.colors.set_colors([[1, 0, 0], [1, 1, 0]])


stroke = layer.add_shape(objects.GradientStroke(5))
stroke.start_point.value = [200, 0]
stroke.end_point.value = [300, 0]
stroke.colors.add_keyframe(0, [[1, 0, 0], [1, 1, 0]])
stroke.colors.add_keyframe(10, [[1, 1, 0], [0, 1, 0]])
stroke.colors.add_keyframe(30, [[1, 0, 1], [0, 0, 1]])
stroke.colors.add_keyframe(59, [[1, 0, 0], [1, 1, 0]])
stroke.colors.count = 2
stroke.stroke_width.value = 10


exporters.multiexport(an, "/tmp/gradients")
