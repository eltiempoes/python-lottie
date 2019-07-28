import math
from .base import TgsObject, TgsProp, PseudoList, PseudoBool


## \ingroup Lottie
class KeyframeBezierHandle(TgsObject):
    """!
    Bezier handle for keyframe interpolation
    """
    _props = [
        TgsProp("x", "x", list=PseudoList),
        TgsProp("y", "y", list=PseudoList),
    ]

    def __init__(self, x=0, y=0):
        ## x position of the handle.
        ## This represents the change in time of the keyframe
        self.x = x
        ## y position of the handle.
        ## This represents the change in value of the keyframe
        self.y = y


class Linear:
    """!
    Linear easing, the value will change from start to end in a straight line
    """
    def __call__(self, keyframe):
        keyframe.out_value = KeyframeBezierHandle(
            0,
            0
        )
        keyframe.in_value = KeyframeBezierHandle(
            1,
            1
        )


class EaseIn:
    """!
    The value lingers near the start before accelerating towards the end
    """
    def __init__(self, delay=1/3):
        self.delay = delay

    def __call__(self, keyframe):
        keyframe.out_value = KeyframeBezierHandle(
            self.delay,
            0
        )
        keyframe.in_value = KeyframeBezierHandle(
            1,
            1
        )


class EaseOut:
    """!
    The value starts fast before decelerating towards the end
    """
    def __init__(self, delay=1/3):
        self.delay = delay

    def __call__(self, keyframe):
        keyframe.out_value = KeyframeBezierHandle(
            0,
            0
        )
        keyframe.in_value = KeyframeBezierHandle(
            1-self.delay,
            1
        )


class Jump:
    """!
    Jumps to the end value at the end of the keyframe
    """
    def __call__(self, keyframe):
        keyframe.jump = True


class Sigmoid:
    """!
    Combines the effects of EaseIn and EaseOut
    """
    def __init__(self, delay=1/3):
        self.delay = delay

    def __call__(self, keyframe):
        keyframe.out_value = KeyframeBezierHandle(
            self.delay,
            0
        )
        keyframe.in_value = KeyframeBezierHandle(
            1 - self.delay,
            1
        )
