from .base import TgsObject, TgsProp, PseudoList


class KeyframeBezierPoint(TgsObject):
    _props = [
        TgsProp("time", "x", list=PseudoList),
        TgsProp("value", "y", list=PseudoList),
    ]

    def __init__(self, time=0, value=0):
        self.time = time
        self.value = value


class OffsetKeyframe(TgsObject):
    _props = {
        TgsProp("start", "s", float, True),
        TgsProp("end", "e", float, True),
        TgsProp("time", "t", float, False),
        TgsProp("in_value", "i", KeyframeBezierPoint, False),
        TgsProp("out_value", "o", KeyframeBezierPoint, False),
        TgsProp("in_tan", "ti", float, True),
        TgsProp("out_tan", "to", float, True),
        #TgsProp("h" ,"h"),
    }

    def __init__(self, time=0, start=None, end=None,
                 in_value=None, out_value=None, in_tan=None, out_tan=None):
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
        self.in_tan = in_tan
        # Out Spatial Tangent. Only for spatial properties. Array of numbers.
        self.out_tan = out_tan

    def set_tangents(self, end_time):
        start = self.start[0]
        end = self.end[0]

        self.in_value = KeyframeBezierPoint(
            (end_time - self.time) / 3,
            (end - start) / 3
        )
        self.out_value = KeyframeBezierPoint(
            (end_time - self.time) / 3,
            (end - start) / 3
        )

        time_scale = end_time - self.time
        value_scale = end - start
        if value_scale == 0:
            value_scale = 1e-9
        time_diff = self.time / time_scale
        value_diff = start / value_scale
        self.out_value.time += self.time
        self.out_value.value += start
        self.out_value.time = abs(self.out_value.time / time_scale - time_diff)
        self.out_value.value = abs(self.out_value.value / value_scale - value_diff)

        self.in_value.time = end_time - self.in_value.time
        self.in_value.value = end - self.in_value.value
        self.in_value.time = abs(self.in_value.time / time_scale - time_diff)
        self.in_value.value = abs(self.in_value.value / value_scale - value_diff)


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
            self.keyframes[-1].set_tangents(time)

        self.keyframes.append(OffsetKeyframe(
            time,
            value,
            None,
            None,
            None,
        ))


class Value(TgsObject):
    _props = [
        TgsProp("value", "k", float, False, lambda l: not l["a"]),
        TgsProp("property_index", "ix", int, False),
        TgsProp("animated", "a", bool, False),
        TgsProp("keyframes", "k", OffsetKeyframe, True, lambda l: l["a"]),
    ]

    def __init__(self, value=0):
        # Property Value
        self.value = value
        # Property Expression. An AE expression that modifies the value.
        self.expression = None
        # Property Index. Used for expressions.
        self.property_index = None
        self.animated = False
        self.keyframes = None

    def clear_animation(self, value):
        self.value = value
        self.animated = False

    def add_keyframe(self, time, value):
        if not self.animated:
            self.value = None
            self.keyframes = []
            self.animated = True
        else:
            self.keyframes[-1].end = [value]
            self.keyframes[-1].set_tangents(time)

        self.keyframes.append(OffsetKeyframe(
            time,
            [value],
            None,
            None,
            None,
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

