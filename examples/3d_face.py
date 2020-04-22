#!/usr/bin/env python3
import sys
import os
import math
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.utils import script
from lottie import objects
from lottie.utils import animation as anutils
from lottie import Size, Point3D, Point, Color


an = objects.Animation(120)

layer = objects.ShapeLayer()
an.add_layer(layer)

g = layer.add_shape(objects.Group())
b = g.add_shape(objects.Ellipse())
b.size.value = Size(256, 256)
b.position.value = Point(256, 256)
g.add_shape(objects.Fill(Color(1, 1, 0)))

g = layer.insert_shape(0, objects.Group())
eye1 = g.add_shape(objects.Ellipse())
eye1.size.value = Size(20, 20)
eye1.position.value = Point3D(256-50, 256-50, -100)
g.add_shape(objects.Fill(Color(0, 0, 0)))

g = layer.insert_shape(0, objects.Group())
eye2 = g.add_shape(objects.Ellipse())
eye2.size.value = Size(20, 20)
eye2.position.value = Point3D(256+50, 256-50, -100)
g.add_shape(objects.Fill(Color(0, 0, 0)))

g = layer.insert_shape(0, objects.Group())
nose = g.add_shape(objects.Ellipse())
nose.size.value = Size(64, 64)
nose.position.value = Point3D(256, 256+10, -150)
g.add_shape(objects.Fill(Color(1, 0, 0)))


g = layer.insert_shape(0, objects.Group())
mouth = g.add_shape(objects.Path())
bez = mouth.shape.value
bez.add_smooth_point(Point3D(256-80, 256+30, -80), Point3D(0, 0, 0))
bez.add_smooth_point(Point3D(256, 256+70, -100), -Point3D(50, 0, 0))
bez.add_smooth_point(Point3D(256+80, 256+30, -80), Point3D(0, 0, 0))
g.add_shape(objects.Stroke(Color(1, 0, 0), 2))

# Animate the circles using depth rotation
dr = anutils.DepthRotationDisplacer(Point3D(256, 256, 0), 0, 30, 10, Point3D(0, 4, 1), 0, 30)
dr.animate_point(eye1.position)
dr.animate_point(eye2.position)
dr.animate_point(nose.position)
dr.animate_bezier(mouth.shape)

dr = anutils.DepthRotationDisplacer(Point3D(256, 256, 0), 30, 90, 10, Point3D(0, 4, 1), 0, -60)
dr.animate_point(eye1.position)
dr.animate_point(eye2.position)
dr.animate_point(nose.position)
dr.animate_bezier(mouth.shape)

dr = anutils.DepthRotationDisplacer(Point3D(256, 256, 0), 90, 120, 10, Point3D(0, 4, 1), 0, 30)
dr.animate_point(eye1.position)
dr.animate_point(eye2.position)
dr.animate_point(nose.position)
dr.animate_bezier(mouth.shape)


script.script_main(an)
