import sys
import os

sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.objects import easing
from tgs import NVector

an = objects.Animation(180)

layer = objects.ShapeLayer()
an.add_layer(layer)

easings = [
    (easing.Linear(),            NVector(1, 1, 1)),
    (easing.EaseOut(1),          NVector(1, 0, 0)),
    (easing.EaseOut(1 / 2),      NVector(1 / 2, 0, 0)),
    (easing.EaseOut(1 / 3),      NVector(1 / 3, 0, 0)),
    (easing.EaseOut(1 / 5),      NVector(1 / 5, 0, 0)),
    (easing.EaseOut(1 / 10),     NVector(1 / 19, 0, 0)),
    (easing.EaseIn(1),           NVector(0, 1, 0)),
    (easing.EaseIn(1 / 2),       NVector(0, 1 / 2, 0)),
    (easing.EaseIn(1 / 3),       NVector(0, 1 / 3, 0)),
    (easing.EaseIn(1 / 5),       NVector(0, 1 / 5, 0)),
    (easing.EaseIn(1 / 10),      NVector(0, 1 / 10, 0)),
    (easing.Sigmoid(1),          NVector(0, 0, 1)),
    (easing.Sigmoid(1 / 2),      NVector(0, 0, 1 / 2)),
    (easing.Sigmoid(1 / 3),      NVector(0, 0, 1 / 3)),
    (easing.Sigmoid(1 / 5),      NVector(0, 0, 1 / 5)),
    (easing.Sigmoid(1 / 10),     NVector(0, 0, 1 / 10)),
    (easing.Jump(),              NVector(0, 0, 0)),
]
height = 512 / len(easings)
width = height

for i in range(len(easings)):
    rect = layer.add_shape(objects.Rect())
    rect.size.value = [width, height]
    y = i * height + height / 2
    rect.position.add_keyframe(0, NVector(width / 2, y))
    rect.position.add_keyframe(90, NVector(512 - width / 2, y), easings[i][0])
    rect.position.add_keyframe(180, NVector(width / 2, y), easings[i][0])
    layer.add_shape(objects.Fill(easings[i][1]))

exporters.multiexport(an, "/tmp/easing")
