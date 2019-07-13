import sys
import os

sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.objects import easing

an = objects.Animation(180)

layer = objects.ShapeLayer()
an.add_layer(layer)

easings = [
    (easing.Linear(),            [1, 1, 1]),
    (easing.EaseOut(1),          [1, 0, 0]),
    (easing.EaseOut(1 / 2),      [1 / 2, 0, 0]),
    (easing.EaseOut(1 / 3),      [1 / 3, 0, 0]),
    (easing.EaseOut(1 / 5),      [1 / 5, 0, 0]),
    (easing.EaseOut(1 / 10),     [1 / 19, 0, 0]),
    (easing.EaseIn(1),           [0, 1, 0]),
    (easing.EaseIn(1 / 2),       [0, 1 / 2, 0]),
    (easing.EaseIn(1 / 3),       [0, 1 / 3, 0]),
    (easing.EaseIn(1 / 5),       [0, 1 / 5, 0]),
    (easing.EaseIn(1 / 10),      [0, 1 / 10, 0]),
    (easing.Sigmoid(1),          [0, 0, 1]),
    (easing.Sigmoid(1 / 2),      [0, 0, 1 / 2]),
    (easing.Sigmoid(1 / 3),      [0, 0, 1 / 3]),
    (easing.Sigmoid(1 / 5),      [0, 0, 1 / 5]),
    (easing.Sigmoid(1 / 10),     [0, 0, 1 / 10]),
    (easing.Jump(),              [0, 0, 0]),
]
height = 512 / len(easings)
width = height

for i in range(len(easings)):
    rect = layer.add_shape(objects.Rect())
    rect.size.value = [width, height]
    y = i * height + height / 2
    rect.position.add_keyframe(0, [width / 2, y])
    rect.position.add_keyframe(90, [512 - width / 2, y], easings[i][0])
    rect.position.add_keyframe(180, [width / 2, y], easings[i][0])
    layer.add_shape(objects.Fill(easings[i][1]))

exporters.multiexport(an, "/tmp/easing")
