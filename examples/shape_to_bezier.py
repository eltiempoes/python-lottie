#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.utils import script
from lottie import objects
from lottie import Point, Color


an = objects.Animation(60)

layer = objects.ShapeLayer()
an.add_layer(layer)

shapes = layer.add_shape(objects.Group())

circle = shapes.add_shape(objects.Ellipse())
circle.size.add_keyframe(0, Point(100, 100))
circle.size.add_keyframe(30, Point(50, 120))
circle.size.add_keyframe(60, Point(100, 100))
circle.position.add_keyframe(0, Point(220, 110))
circle.position.add_keyframe(20, Point(180, 110))
circle.position.add_keyframe(40, Point(220, 110))

star = shapes.add_shape(objects.Star())
star.inner_radius.add_keyframe(0, 20)
star.inner_radius.add_keyframe(30, 50)
star.inner_radius.add_keyframe(60, 20)
star.outer_radius.value = 50
#star.inner_roundness.value = 100
#star.outer_roundness.value = 40
star.rotation.value = 45
star.position.value = Point(330, 110)

rect = shapes.add_shape(objects.Rect())
rect.size.add_keyframe(0, Point(100, 100))
rect.size.add_keyframe(30, Point(50, 120))
rect.size.add_keyframe(60, Point(100, 100))
rect.position.add_keyframe(0, Point(110, 110))
rect.position.add_keyframe(20, Point(80, 110))
rect.position.add_keyframe(40, Point(110, 110))


rrect = shapes.add_shape(objects.Rect())
rrect.size.value = Point(100, 100)
rrect.position.value = Point(440, 110)
rrect.rounded.add_keyframe(0, 0)
rrect.rounded.add_keyframe(30, 30)
rrect.rounded.add_keyframe(60, 0)

fill = shapes.add_shape(objects.Fill(Color(1, 1, 0)))
stroke = shapes.add_shape(objects.Stroke(Color(0, 0, 0), 5))


beziers = layer.add_shape(objects.Group())
beziers.transform.position.value = Point(0, 130)
beziers.add_shape(rect.to_bezier())
beziers.add_shape(rrect.to_bezier())
beziers.add_shape(circle.to_bezier())
beziers.add_shape(star.to_bezier())



fill = beziers.add_shape(objects.Fill(Color(0, 0, 1)))
stroke = beziers.add_shape(objects.Stroke(Color(1, 1, 1), 5))


script.script_main(an)
