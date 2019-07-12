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
circle.position.add_keyframe(0, [0, 256])
circle.position.add_keyframe(20, [256, 256])
circle.position.add_keyframe(40, [256, 0])
circle.position.add_keyframe(60, [0, 256])


fill = layer.add_shape(objects.Fill([1, 1, 0]))
fill.opacity.add_keyframe(0, 100)
fill.opacity.add_keyframe(30, 10)
fill.opacity.add_keyframe(60, 100)


exporters.multiexport(an, "/tmp/simple_animations")


