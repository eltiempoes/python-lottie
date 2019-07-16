import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs import NVector


an = objects.Animation(60)

layer = objects.ShapeLayer()
an.add_layer(layer)

shapes = layer.add_shape(objects.Group())

circle = shapes.add_shape(objects.Ellipse())
circle.size.add_keyframe(0, NVector(100, 100))
circle.size.add_keyframe(30, NVector(50, 120))
circle.size.add_keyframe(60, NVector(100, 100))
circle.position.add_keyframe(0, NVector(220, 110))
circle.position.add_keyframe(20, NVector(180, 110))
circle.position.add_keyframe(40, NVector(220, 110))

star = shapes.add_shape(objects.Star())
star.inner_radius.add_keyframe(0, 20)
star.inner_radius.add_keyframe(30, 50)
star.inner_radius.add_keyframe(60, 20)
star.outer_radius.value = 50
#star.inner_roundness.value = 100
#star.outer_roundness.value = 40
star.rotation.value = 45
star.position.value = NVector(330, 110)

rect = shapes.add_shape(objects.Rect())
rect.size.add_keyframe(0, NVector(100, 100))
rect.size.add_keyframe(30, NVector(50, 120))
rect.size.add_keyframe(60, NVector(100, 100))
rect.position.add_keyframe(0, NVector(110, 110))
rect.position.add_keyframe(20, NVector(80, 110))
rect.position.add_keyframe(40, NVector(110, 110))


rrect = shapes.add_shape(objects.Rect())
rrect.size.value = NVector(100, 100)
rrect.position.value = NVector(440, 110)
rrect.rounded.add_keyframe(0, 0)
rrect.rounded.add_keyframe(30, 30)
rrect.rounded.add_keyframe(60, 0)

fill = shapes.add_shape(objects.Fill(NVector(1, 1, 0)))
stroke = shapes.add_shape(objects.Stroke(NVector(0, 0, 0), 5))


beziers = layer.add_shape(objects.Group())
beziers.transform.position.value = NVector(0, 130)
beziers.add_shape(rect.to_bezier())
beziers.add_shape(rrect.to_bezier())
beziers.add_shape(circle.to_bezier())
beziers.add_shape(star.to_bezier())



fill = beziers.add_shape(objects.Fill(NVector(0, 0, 1)))
stroke = beziers.add_shape(objects.Stroke(NVector(1, 1, 1), 5))


exporters.multiexport(an, "/tmp/shape_to_bezier")
