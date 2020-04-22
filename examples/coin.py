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
from lottie import Color, Point
from lottie.objects import easing


rot_time = 45
an = objects.Animation(rot_time*4)


layer = objects.ShapeLayer()
an.add_layer(layer)


def add_shape(shape, color, parent):
    g = parent.add_shape(objects.Group())
    s = g.add_shape(shape)
    g.add_shape(objects.Fill(color))
    return s


face1 = add_shape(objects.Ellipse(), Color(1, 1, 0), layer)
face2 = add_shape(objects.Ellipse(), Color(0, 1, 0), layer)

side = layer.add_shape(objects.Group())
side1 = add_shape(objects.Ellipse(), Color(1, 0, 0), side)
side2 = add_shape(objects.Ellipse(), Color(1, 0, 0), side)
sider = add_shape(objects.Rect(), Color(1, 0, 0), side)


width = 10

face1.size.add_keyframe(rot_time*0, Point(256, 256), easing.EaseIn())
face1.size.add_keyframe(rot_time*1, Point(0, 256))
face1.size.add_keyframe(rot_time*2, Point(0, 256))
face1.size.add_keyframe(rot_time*3, Point(0, 256), easing.EaseOut())
face1.size.add_keyframe(rot_time*4, Point(256, 256))
face1.position.add_keyframe(rot_time*0, Point(256, 256), easing.EaseIn())
face1.position.add_keyframe(rot_time*1, Point(256-width, 256))
face1.position.add_keyframe(rot_time*2, Point(256-width, 256))
face1.position.add_keyframe(rot_time*3, Point(256+width, 256), easing.EaseOut())
face1.position.add_keyframe(rot_time*4, Point(256, 256))


face2.size.add_keyframe(rot_time*0, Point(0, 256))
face2.size.add_keyframe(rot_time*1, Point(0, 256), easing.EaseOut())
face2.size.add_keyframe(rot_time*2, Point(256, 256), easing.EaseIn())
face2.size.add_keyframe(rot_time*3, Point(0, 256))
face2.position.add_keyframe(rot_time*0, Point(256+width, 256))
face2.position.add_keyframe(rot_time*1, Point(256+width, 256), easing.EaseOut())
face2.position.add_keyframe(rot_time*2, Point(256, 256), easing.EaseIn())
face2.position.add_keyframe(rot_time*3, Point(256-width, 256))


side1.size = face1.size
side1.position.add_keyframe(rot_time*0, Point(256, 256), easing.EaseIn())
side1.position.add_keyframe(rot_time*1, Point(256+width, 256))
side1.position.add_keyframe(rot_time*2, Point(256-width, 256))
side1.position.add_keyframe(rot_time*3, Point(256-width, 256), easing.EaseOut())
side1.position.add_keyframe(rot_time*4, Point(256, 256))

sider.position.value = Point(256, 256)
sider.size.add_keyframe(rot_time*0, Point(0, 256))
sider.size.add_keyframe(rot_time*1, Point(2*width, 256))
sider.size.add_keyframe(rot_time*2, Point(0, 256))
sider.size.add_keyframe(rot_time*3, Point(2*width, 256))

side2.size = face2.size
side2.position.add_keyframe(rot_time*0, Point(256-width, 256))
side2.position.add_keyframe(rot_time*1, Point(256-width, 256), easing.EaseOut())
side2.position.add_keyframe(rot_time*2, Point(256, 256), easing.EaseIn())
side2.position.add_keyframe(rot_time*3, Point(256+width, 256))
side2.position.add_keyframe(rot_time*4, Point(256-width, 256))


script.script_main(an)
