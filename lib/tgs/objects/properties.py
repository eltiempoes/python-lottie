from .base import TgsObject, TgsProp


class KeyframeBezierPoint(TgsObject):
    _props = [
        TgsProp("x", "x"),
        TgsProp("y", "y"),
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def load(cls, value):
        return cls(**value)


class OffsetKeyframe(TgsObject):
    _props = {
        TgsProp("start", "s", float, True),
        TgsProp("end", "e", float, True),
        TgsProp("time", "t", float, False),
        TgsProp("in_value", "i", KeyframeBezierPoint, False),
        TgsProp("out_value", "o", KeyframeBezierPoint, False),
        TgsProp("in_tangent", "ti", float, True),
        TgsProp("out_tangent", "to", float, True),
        #TgsProp("h" ,"h"),
    }

    def __init__(self, time=0, start=None, end=None,
                 in_value=None, out_value=None, in_tangent=None, out_tangent=None):
        # Start value of keyframe segment.
        self.start = start # number
        self.end = end # number
        # Start time of keyframe segment.
        self.time = time
        # Bezier curve interpolation in value.
        self.in_value = in_value
        # Bezier curve interpolation out value.
        self.out_value = out_value
        #self.h = 1 #???
        # In Spatial Tangent. Only for spatial properties. Array of numbers.
        self.in_tangent = in_tangent
        # Out Spatial Tangent. Only for spatial properties. Array of numbers.
        self.out_tangent = out_tangent

    @classmethod
    def load_lottie_obj(cls, name, value):
        if name in {"i", "o"}:
            return KeyframeBezierPoint.load(value)
        return super().load_lottie_obj(name, value)


class MultiDimensional(TgsObject):
    _props = [
        TgsProp("value", "k", float, True, lambda l: not l["a"]),
        TgsProp("property_index", "ix", int, False),
        TgsProp("animated", "a", bool, False),
        TgsProp("keyframes", "k", OffsetKeyframe, True, lambda l: l["a"]),
    ]

    def __init__(self, value=None):
        # Property Value
        self.value = value
        # Property Index. Used for expressions.
        self.property_index = None
        self.animated = False
        # Property Value keyframes
        self.keyframes = None # [OffsetKeyframe]

    def clear_animation(self, value):
        self.value = value
        self.animated = False

    def add_keyframe(self, time, value):
        if not self.animated:
            self.value = None
            self.keyframes = []
            self.animated = True
        else:
            self.keyframes[-1].end = value

        # TODO see calc_tangent in the exporter
        self.keyframes.append(OffsetKeyframe(
            time,
            value,
            None,
            KeyframeBezierPoint(0, 0),
            KeyframeBezierPoint(0, 0),
            [1, 1],
            [0, 0]
        ))


class ShapeProp(TgsObject): # TODO check
    _props = [
        TgsProp("closed", "c", float, False),
        TgsProp("in_point", "i", float, True),
        TgsProp("out_point", "o", float, True),
        TgsProp("vertices", "v", float, True),
    ]

    def __init__(self):
        # Closed property of shape
        self.closed = None
        # Bezier curve In points. Array of 2 dimensional arrays.
        self.in_point = [] # array
        # Bezier curve Out points. Array of 2 dimensional arrays.
        self.out_point = [] # array
        # Bezier curve Vertices. Array of 2 dimensional arrays.
        self.vertices = [] # array


class ShapePropKeyframe(TgsObject): # TODO check
    _props = [
        TgsProp("start", "s", ShapeProp, True),
        TgsProp("time", "t", float, False),
        TgsProp("in_value", "i", float, False),
        TgsProp("out_value", "o", float, False),
    ]

    def __init__(self):
        # Start value of keyframe segment.
        self.start = [] # ShapeProp
        # Start time of keyframe segment.
        self.time = 0
        # Bezier curve interpolation in value.
        self.in_value = None
        # Bezier curve interpolation out value.
        self.out_value = None


class ShapePropertyKeyframed(TgsObject): # TODO check
    _props = [
        TgsProp("keyframes", "k", ShapePropKeyframe, True),
        TgsProp("expression", "x", str, False),
        TgsProp("property_index", "ix", float, False),
        TgsProp("in_tangent", "ti", float, True),
        TgsProp("out_tangent", "to", float, True),
    ]

    def __init__(self):
        # Property Value keyframes
        self.keyframes = [] # ShapePropKeyframe
        # Property Expression. An AE expression that modifies the value.
        self.expression = ""
        # Property Index. Used for expressions.
        self.property_index = 0
        # In Spatial Tangent. Only for spatial properties. Array of numbers.
        self.in_tangent = []
        # Out Spatial Tangent. Only for spatial properties. Array of numbers.
        self.out_tangent = []



class ShapeProperty(TgsObject): # TODO check
    _props = [
        TgsProp("value", "k", ShapeProp, False),
        TgsProp("expression", "x", str, False),
        TgsProp("property_index", "ix", float, False),
        TgsProp("animated", "a", float, False),
    ]

    def __init__(self):
        # Property Value
        self.value = ShapeProp()
        # Property Expression. An AE expression that modifies the value.
        self.expression = ""
        # Property Index. Used for expressions.
        self.property_index = 0
        # Defines if property is animated
        self.animated = 0



class DoubleKeyframe(TgsObject): # TODO check
    _props = [
        TgsProp("start", "s", float, False),
        TgsProp("time", "t", float, False),
        TgsProp("in_value", "i", float, False),
        TgsProp("out_value", "o", float, False),
    ]

    def __init__(self):
        # Start value of keyframe segment.
        self.start = 0
        # Start time of keyframe segment.
        self.time = 0
        # Bezier curve interpolation in value.
        self.in_value = None
        # Bezier curve interpolation out value.
        self.out_value = None


class ValueKeyframe(TgsObject): # TODO check
    _props = [
        TgsProp("start", "s", float, False),
        TgsProp("time", "t", float, False),
        TgsProp("in_value", "i", float, False),
    ]

    def __init__(self):
        # Start value of keyframe segment.
        self.start = 0
        # Start time of keyframe segment.
        self.time = 0
        # Bezier curve interpolation in value.
        self.in_value = None


class Value(TgsObject): # TODO check
    _props = [
        TgsProp("value", "k", float, False),
        TgsProp("expression", "x", str, False),
        TgsProp("property_index", "ix", float, False),
    ]

    def __init__(self, value=0):
        # Property Value
        self.value = value
        # Property Expression. An AE expression that modifies the value.
        self.expression = ""
        # Property Index. Used for expressions.
        self.property_index = 0


class ValueKeyframed(TgsObject): # TODO check
    _props = [
        TgsProp("keyframes", "k", ValueKeyframe, True),
        TgsProp("expression", "x", str, False),
        TgsProp("property_index", "ix", float, False),
    ]

    def __init__(self):
        # Property Value keyframes
        self.keyframes = [] # ValueKeyframe
        # Property Expression. An AE expression that modifies the value.
        self.expression = ""
        # Property Index. Used for expressions.
        self.property_index = 0
