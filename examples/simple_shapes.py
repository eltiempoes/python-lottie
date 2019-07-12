import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects


an = objects.Animation(59)

layer = objects.ShapeLayer()
an.add_layer(layer)

circle = layer.add_shape(objects.Ellipse())
circle.size.value = [100, 100]
circle.position.value = [220, 110]

star = layer.add_shape(objects.Star())
star.inner_radius.value = 10
star.outer_radius.value = 50
star.position.value = [330, 110]

rect = layer.add_shape(objects.Rect())
rect.size.value = [100, 100]
rect.position.value = [110, 110]


rrect = layer.add_shape(objects.Rect())
rrect.size.value = [100, 100]
rrect.position.value = [110, 220]
rrect.rounded.value = 30

fill = layer.add_shape(objects.Fill([1, 1, 0]))
stroke = layer.add_shape(objects.Stroke([0, 0, 0], 5))


exporters.multiexport(an, "/tmp/simple_shapes")
