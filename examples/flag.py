#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.utils import script
from lottie import objects
from lottie.utils import animation as anutils
from lottie import Point, Color

an = objects.Animation(60)

layer = objects.ShapeLayer()
an.add_layer(layer)
g = layer.add_shape(objects.Group())

sine_displacer = anutils.SineDisplacer(300, 50, 0, 60, 10, 1, 45)
# Keep the left side fixed
displacer = anutils.DisplacerDampener(sine_displacer, lambda p: p.x / 128 if p.x < 128 else 1)

for i in range(0, 512+1, 16):
    b = g.add_shape(objects.Ellipse())
    b.size.value = Point(16, 16)
    b.position.value = Point(i, 100)
    displacer.animate_point(b.position)


bez = g.add_shape(objects.Path())
bez.shape.value.add_smooth_point(Point(256, 200), Point(50, 0))
bez.shape.value.add_smooth_point(Point(156, 300), Point(0, -50))
bez.shape.value.add_smooth_point(Point(256, 400), Point(-50, 0))
bez.shape.value.add_smooth_point(Point(356, 300), Point(0, 50))
bez.shape.value.close()
bez.shape.value.split_self_chunks(8)
displacer.animate_bezier(bez.shape)

g.add_shape(objects.Fill(Color(1, 1, 0)))


g = layer.add_shape(objects.Group())
bez = g.add_shape(objects.Path())
g.add_shape(objects.Stroke(Color(1, 0, 0), 5))
g.add_shape(objects.Fill(Color(0, 0, 1)))
for i in range(9):
    bez.shape.value.add_point(Point(i*64, 160), Point(-20, 0), Point(20, 0))

for i in range(9):
    bez.shape.value.add_point(Point(512-i*64, 420), Point(20, 0), Point(-20, 0))
bez.shape.value.close()
displacer.animate_bezier(bez.shape)


script.script_main(an)


