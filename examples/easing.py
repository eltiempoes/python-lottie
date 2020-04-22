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
from lottie.objects import easing
from lottie import Point, Color, Size

an = objects.Animation(180)

layer = objects.ShapeLayer()
an.add_layer(layer)

easings = [
    (easing.Linear(),            Color(1, 1, 1)),
    (easing.Jump(),              Color(0, 0, 0)),
    (easing.EaseOut(1),          Color(1, 0, 0)),
    (easing.EaseOut(1 / 2),      Color(1 / 2, 0, 0)),
    (easing.EaseOut(1 / 3),      Color(1 / 3, 0, 0)),
    (easing.EaseOut(1 / 5),      Color(1 / 5, 0, 0)),
    (easing.EaseOut(1 / 10),     Color(1 / 19, 0, 0)),
    (easing.EaseIn(1),           Color(0, 1, 0)),
    (easing.EaseIn(1 / 2),       Color(0, 1 / 2, 0)),
    (easing.EaseIn(1 / 3),       Color(0, 1 / 3, 0)),
    (easing.EaseIn(1 / 5),       Color(0, 1 / 5, 0)),
    (easing.EaseIn(1 / 10),      Color(0, 1 / 10, 0)),
    (easing.Sigmoid(1),          Color(0, 0, 1)),
    (easing.Sigmoid(1 / 2),      Color(0, 0, 1 / 2)),
    (easing.Sigmoid(1 / 3),      Color(0, 0, 1 / 3)),
    (easing.Sigmoid(1 / 5),      Color(0, 0, 1 / 5)),
    (easing.Sigmoid(1 / 10),     Color(0, 0, 1 / 10)),
]
height = 512 / len(easings)
width = height

for i in range(len(easings)):
    group = layer.add_shape(objects.Group())

    rectgroup = group.add_shape(objects.Group())
    rect = rectgroup.add_shape(objects.Rect())
    rect.size.value = Size(width, height)
    y = i * height + height / 2
    group.transform.position.add_keyframe(0, Point(width / 2, y), easings[i][0])
    group.transform.position.add_keyframe(90, Point(512 - width / 2, y), easings[i][0])
    group.transform.position.add_keyframe(180, Point(width / 2, y), easings[i][0])
    rectgroup.add_shape(objects.Fill(easings[i][1]))

    bezgroup = group.insert_shape(0, objects.Group())
    bez = group.transform.position.keyframes[0].bezier()
    bezgroup.transform.scale.value = Size(100*width, -100*height)
    bezgroup.transform.position.value = Point(-width/2, width/2)
    bezgroup.add_shape(objects.Path()).shape.value = bez
    sc = Color(0, 0, 0) if easings[i][1].length == math.sqrt(3) else Color(1, 1, 1)
    bezgroup.add_shape(objects.Stroke(sc, 0.1))



script.script_main(an)
