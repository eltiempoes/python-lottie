#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.utils import script
from lottie import objects
from lottie import Point, Color, NVector


last_frame = 180
an = objects.Animation(last_frame)


base = an.add_layer(objects.NullLayer())
base.transform.anchor_point.value = base.transform.position.value = Point(256, 256)
base.transform.rotation.add_keyframe(0, 0)
base.transform.rotation.add_keyframe(last_frame, 360)


star_layer = objects.ShapeLayer()
base.add_child(star_layer)
star = star_layer.add_shape(objects.Star())
star.inner_radius.value = 20
star.outer_radius.value = 50
star.position.value = Point(50, 50)
star_layer.add_shape(objects.Fill(Color(1, 1, 0)))
star_layer.add_shape(objects.Stroke(Color(0, 0, 0), 5))
star_layer.transform.anchor_point = star.position
star_layer.transform.position.value = Point(50, 256)
star_layer.transform.rotation.add_keyframe(0, 0)
star_layer.transform.rotation.add_keyframe(last_frame, -360)


circle_layer = objects.ShapeLayer()
an.add_layer(circle_layer)
circle_layer.parent = base
circle = circle_layer.add_shape(objects.Ellipse())
circle.size.value = NVector(100, 100)
circle_layer.add_shape(objects.Fill(Color(1, 0, 0)))
circle_layer.add_shape(objects.Stroke(Color(0, 0, 0), 5))
circle_layer.transform.position.add_keyframe(0, Point(256, 512-50))
circle_layer.transform.position.add_keyframe(last_frame/2, Point(256, 50))
circle_layer.transform.position.add_keyframe(last_frame, Point(256, 512-50))


scl = base.add_child(objects.SolidColorLayer("#0000ff"))
scl.transform.scale.value.x *= 0.2
scl.transform.position.value.x = 205


star_background = star_layer.add_child(objects.SolidColorLayer("#0000ff", 100, 100))


script.script_main(an)

