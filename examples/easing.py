import sys
import os

sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.utils import script
from tgs import objects
from tgs.objects import easing
from tgs import Point, Color, Size

an = objects.Animation(180)

layer = objects.ShapeLayer()
an.add_layer(layer)

easings = [
    (easing.Linear(),            Color(1, 1, 1)),
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
    (easing.Jump(),              Color(0, 0, 0)),
]
height = 512 / len(easings)
width = height

for i in range(len(easings)):
    rect = layer.add_shape(objects.Rect())
    rect.size.value = Size(width, height)
    y = i * height + height / 2
    rect.position.add_keyframe(0, Point(width / 2, y))
    rect.position.add_keyframe(90, Point(512 - width / 2, y), easings[i][0])
    rect.position.add_keyframe(180, Point(width / 2, y), easings[i][0])
    layer.add_shape(objects.Fill(easings[i][1]))

script.script_main(an)
