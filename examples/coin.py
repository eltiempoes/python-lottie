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
from tgs.objects import easing


rot_time = 45
an = objects.Animation(rot_time*4)


layer = objects.ShapeLayer()
an.add_layer(layer)


def add_shape(shape, color, parent):
    g = parent.add_shape(objects.Group())
    s = g.add_shape(shape)
    g.add_shape(objects.Fill(color))
    return s


face1 = add_shape(objects.Ellipse(), NVector(1, 1, 0), layer)
face2 = add_shape(objects.Ellipse(), NVector(0, 1, 0), layer)

side = layer.add_shape(objects.Group())
side1 = add_shape(objects.Ellipse(), NVector(1, 0, 0), side)
side2 = add_shape(objects.Ellipse(), NVector(1, 0, 0), side)
sider = add_shape(objects.Rect(), NVector(1, 0, 0), side)


width = 10

face1.size.add_keyframe(rot_time*0, NVector(256, 256))
face1.size.add_keyframe(rot_time*1, NVector(0, 256), easing.EaseIn())
face1.size.add_keyframe(rot_time*2, NVector(0, 256))
face1.size.add_keyframe(rot_time*3, NVector(0, 256))
face1.size.add_keyframe(rot_time*4, NVector(256, 256), easing.EaseOut())
face1.position.add_keyframe(rot_time*0, NVector(256, 256))
face1.position.add_keyframe(rot_time*1, NVector(256-width, 256), easing.EaseIn())
face1.position.add_keyframe(rot_time*2, NVector(256-width, 256))
face1.position.add_keyframe(rot_time*3, NVector(256+width, 256))
face1.position.add_keyframe(rot_time*4, NVector(256, 256), easing.EaseOut())


face2.size.add_keyframe(rot_time*0, NVector(0, 256))
face2.size.add_keyframe(rot_time*1, NVector(0, 256))
face2.size.add_keyframe(rot_time*2, NVector(256, 256), easing.EaseOut())
face2.size.add_keyframe(rot_time*3, NVector(0, 256), easing.EaseIn())
face2.position.add_keyframe(rot_time*0, NVector(256+width, 256))
face2.position.add_keyframe(rot_time*1, NVector(256+width, 256))
face2.position.add_keyframe(rot_time*2, NVector(256, 256), easing.EaseOut())
face2.position.add_keyframe(rot_time*3, NVector(256-width, 256), easing.EaseIn())


side1.size = face1.size
side1.position.add_keyframe(rot_time*0, NVector(256, 256))
side1.position.add_keyframe(rot_time*1, NVector(256+width, 256), easing.EaseIn())
side1.position.add_keyframe(rot_time*2, NVector(256-width, 256))
side1.position.add_keyframe(rot_time*3, NVector(256-width, 256))
side1.position.add_keyframe(rot_time*4, NVector(256, 256), easing.EaseOut())

sider.position.value = NVector(256, 256)
sider.size.add_keyframe(rot_time*0, NVector(0, 256))
sider.size.add_keyframe(rot_time*1, NVector(2*width, 256))
sider.size.add_keyframe(rot_time*2, NVector(0, 256))
sider.size.add_keyframe(rot_time*3, NVector(2*width, 256))

side2.size = face2.size
side2.position.add_keyframe(rot_time*0, NVector(256-width, 256))
side2.position.add_keyframe(rot_time*1, NVector(256-width, 256))
side2.position.add_keyframe(rot_time*2, NVector(256, 256), easing.EaseOut())
side2.position.add_keyframe(rot_time*3, NVector(256+width, 256), easing.EaseIn())
side2.position.add_keyframe(rot_time*4, NVector(256-width, 256))


exporters.multiexport(an, "/tmp/coin")
