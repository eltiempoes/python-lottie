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


g1 = layer.add_shape(objects.Group())
circle = g1.add_shape(objects.Ellipse())
circle.size.value = [100, 100]
circle.position.value = [200, 100]
g1.add_shape(objects.Fill([1,0, 0]))
g1.add_shape(objects.Stroke([0, 0, 0], 5))

g2 = layer.add_shape(objects.Group())
star = g2.add_shape(objects.Star())
star.inner_radius.value = 10
star.outer_radius.value = 50
star.position.value = [300, 100]
g2.add_shape(objects.Fill([0, 1, 0]))
g2.add_shape(objects.Stroke([0, 0, 0], 5))

g3 = layer.add_shape(objects.Group())
rect = g3.add_shape(objects.Rect())
rect.size.value = [100, 100]
rect.position.value = [100, 100]
g3.add_shape(objects.Fill([0, 0, 1]))
g3.add_shape(objects.Stroke([1, 1, 1], 5))


exporters.multiexport(an, "/tmp/groups")

