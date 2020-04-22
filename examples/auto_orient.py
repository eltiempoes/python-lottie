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


layer = objects.ShapeLayer()
an.add_layer(layer)
layer.auto_orient = True

group = layer.add_shape(objects.Group())
star = objects.Star()
star.inner_radius.value = 20
star.outer_radius.value = 50
star.position.value = Point(0, 0)
group.add_shape(star)

group.add_shape(objects.Ellipse(NVector(0, 35), NVector(16, 16)))

layer.add_shape(objects.Fill(Color(1, 1, 0)))


tl = 120
layer.transform.position.add_keyframe(last_frame/4*0, Point(+50, 256), out_tan=NVector(0, -tl), in_tan=NVector(-tl, 0))
layer.transform.position.add_keyframe(last_frame/4*1, Point(256, +50), out_tan=NVector(+tl, 0), in_tan=NVector(0, -tl))
layer.transform.position.add_keyframe(last_frame/4*2, Point(462, 256), out_tan=NVector(0, +tl), in_tan=NVector(+tl, 0))
layer.transform.position.add_keyframe(last_frame/4*3, Point(256, 462), out_tan=NVector(-tl, 0), in_tan=NVector(0, +tl))
layer.transform.position.add_keyframe(last_frame/4*4, Point(+50, 256), out_tan=NVector(0, -tl), in_tan=NVector(-tl, 0))


layer1 = objects.ShapeLayer()
an.add_layer(layer1)
layer1.add_shape(group)
layer1.add_shape(objects.Fill(Color(1, 0, 0)))
layer1.transform = layer.transform


bg = an.add_layer(objects.ShapeLayer())
track = bg.add_shape(objects.Path()).shape.value
track.closed = True
track.add_point(Point(+50, 256), NVector(0, +tl), NVector(0, -tl))
track.add_point(Point(256, +50), NVector(-tl, 0), NVector(+tl, 0))
track.add_point(Point(462, 256), NVector(0, -tl), NVector(0, +tl))
track.add_point(Point(256, 462), NVector(+tl, 0), NVector(-tl, 0))
bg.add_shape(objects.Stroke(Color(0, 0, 1), 50))


script.script_main(an)

