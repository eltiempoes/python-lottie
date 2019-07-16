import sys
import os
import math
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.utils import animation as anutils
from tgs import NVector


an = objects.Animation(120)

layer = objects.ShapeLayer()
an.add_layer(layer)

g = layer.add_shape(objects.Group())
b = g.add_shape(objects.Ellipse())
b.size.value = NVector(256, 256)
b.position.value = NVector(256, 256)
g.add_shape(objects.Fill(NVector(1, 1, 0)))

g = layer.insert_shape(0, objects.Group())
eye1 = g.add_shape(objects.Ellipse())
eye1.size.value = NVector(20, 20)
eye1.position.value = NVector(256-50, 256-50, -100)
g.add_shape(objects.Fill(NVector(0, 0, 0)))

g = layer.insert_shape(0, objects.Group())
eye2 = g.add_shape(objects.Ellipse())
eye2.size.value = NVector(20, 20)
eye2.position.value = NVector(256+50, 256-50, -100)
g.add_shape(objects.Fill(NVector(0, 0, 0)))

g = layer.insert_shape(0, objects.Group())
nose = g.add_shape(objects.Ellipse())
nose.size.value = NVector(64, 64)
nose.position.value = NVector(256, 256+10, -150)
g.add_shape(objects.Fill(NVector(1, 0, 0)))


g = layer.insert_shape(0, objects.Group())
mouth = g.add_shape(objects.Shape())
bez = mouth.vertices.value
bez.add_smooth_point(NVector(256-80, 256+30, -80), NVector(0, 0, 0))
bez.add_smooth_point(NVector(256, 256+70, -100), -NVector(50, 0, 0))
bez.add_smooth_point(NVector(256+80, 256+30, -80), NVector(0, 0, 0))
g.add_shape(objects.Stroke(NVector(1, 0, 0), 2))

# Animate the circles using depth rotation
dr = anutils.DepthRotationDisplacer(NVector(256, 256, 0), 0, 30, 10, NVector(0, 4, 1), 0, 30)
dr.animate_point(eye1.position)
dr.animate_point(eye2.position)
dr.animate_point(nose.position)
dr.animate_bezier(mouth.vertices)

dr = anutils.DepthRotationDisplacer(NVector(256, 256, 0), 30, 90, 10, NVector(0, 4, 1), 0, -60, 20)
dr.animate_point(eye1.position)
dr.animate_point(eye2.position)
dr.animate_point(nose.position)
dr.animate_bezier(mouth.vertices)

dr = anutils.DepthRotationDisplacer(NVector(256, 256, 0), 90, 120, 10, NVector(0, 4, 1), 0, 30, -50)
dr.animate_point(eye1.position)
dr.animate_point(eye2.position)
dr.animate_point(nose.position)
dr.animate_bezier(mouth.vertices)


exporters.multiexport(an, "/tmp/3d_face")
