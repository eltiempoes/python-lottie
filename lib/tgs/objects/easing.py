import math
from .base import TgsObject, TgsProp, PseudoList, PseudoBool


## \ingroup Lottie
class KeyframeBezierPoint(TgsObject):
    _props = [
        TgsProp("x", "x", list=PseudoList),
        TgsProp("y", "y", list=PseudoList),
    ]

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Linear:
    def __call__(self, keyframe, start, end, end_time):
        keyframe.in_value = KeyframeBezierPoint(
            0,
            0
        )
        keyframe.out_value = KeyframeBezierPoint(
            0,
            0
        )


class EaseIn:
    def __init__(self, delay=1 / 3):
        self.delay = delay

    def __call__(self, keyframe, start, end, end_time):
        keyframe.in_value = KeyframeBezierPoint(
            (end_time - keyframe.time) * self.delay,
            (end - start) * self.delay
        )
        keyframe.out_value = KeyframeBezierPoint(
            (end_time - keyframe.time) * self.delay,
            0
        )
        Sigmoid.adjust(keyframe, start, end, end_time)


class EaseOut:
    def __init__(self, delay=1 / 3):
        self.delay = delay

    def __call__(self, keyframe, start, end, end_time):
        keyframe.in_value = KeyframeBezierPoint(
            (end_time - keyframe.time) * self.delay,
            0
        )
        keyframe.out_value = KeyframeBezierPoint(
            (end_time - keyframe.time) * self.delay,
            (end - start) * self.delay
        )
        Sigmoid.adjust(keyframe, start, end, end_time)


class Jump:
    def __call__(self, keyframe, start, end, end_time):
        keyframe.in_value = KeyframeBezierPoint(
            (end_time - keyframe.time),
            0
        )
        keyframe.out_value = KeyframeBezierPoint(
            0,
            0
        )


class Sigmoid:
    def __init__(self, delay=1 / 3):
        self.delay = delay

    def __call__(self, keyframe, start, end, end_time):
        keyframe.in_value = KeyframeBezierPoint(
            (end_time - keyframe.time) * self.delay,
            0
        )
        keyframe.out_value = KeyframeBezierPoint(
            -(end_time - keyframe.time) * self.delay,
            0
        )
        Sigmoid.adjust(keyframe, start, end, end_time)

    @staticmethod
    def adjust(keyframe, start, end, end_time):
        time_scale = end_time - keyframe.time
        time_diff = keyframe.time / time_scale
        value_scale = end - start
        if value_scale == 0:
            value_scale = 1e-9
        value_diff = start / value_scale

        keyframe.in_value.x = end_time - keyframe.in_value.x
        keyframe.in_value.y = end - keyframe.in_value.y
        keyframe.in_value.x = abs(keyframe.in_value.x / time_scale - time_diff)
        keyframe.in_value.y = abs(keyframe.in_value.y / value_scale - value_diff)

        keyframe.out_value.x += keyframe.time
        keyframe.out_value.y += start
        keyframe.out_value.x = abs(keyframe.out_value.x / time_scale - time_diff)
        keyframe.out_value.y = abs(keyframe.out_value.y / value_scale - value_diff)
