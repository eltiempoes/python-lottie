import math
from functools import reduce
from .base import TgsObject, TgsProp, PseudoList, PseudoBool


class KeyframeBezierPoint(TgsObject):
    _props = [
        TgsProp("time", "x", list=PseudoList),
        TgsProp("value", "y", list=PseudoList),
    ]

    def __init__(self, time=0, value=0):
        self.time = time
        self.value = value


def _set_tangents(self, start, end, end_time):
    self.in_value = KeyframeBezierPoint(
        (end_time - self.time) / 3,
        (end - start) / 3
    )
    self.out_value = KeyframeBezierPoint(
        (end_time - self.time) / 3,
        (end - start) / 3
    )

    time_scale = end_time - self.time
    time_diff = self.time / time_scale
    value_scale = end - start
    if value_scale == 0:
        value_scale = 1e-9
    value_diff = start / value_scale

    self.in_value.time = end_time - self.in_value.time
    self.in_value.value = end - self.in_value.value
    self.in_value.time = abs(self.in_value.time / time_scale - time_diff)
    self.in_value.value = abs(self.in_value.value / value_scale - value_diff)

    self.out_value.time += self.time
    self.out_value.value += start
    self.out_value.time = abs(self.out_value.time / time_scale - time_diff)
    self.out_value.value = abs(self.out_value.value / value_scale - value_diff)


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
        to_val = lambda vals: math.sqrt(sum(map(lambda x: x**2, vals)))
        start = to_val(self.start)
        end = to_val(self.end)
        _set_tangents(self, start, end, end_time)


class AnimatableMixin:
    def __init__(self, value=None):
        self.value = value
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
            self.keyframes[-1].end = value
            self.keyframes[-1].set_tangents(time)

        self.keyframes.append(self.keyframe_type(
            time,
            value,
            None,
        ))

    def get_value(self, time=0):
        if not self.animated:
            return self.value

        if not self.keyframes:
            return None

        val = self.keyframes[0].start
        for k in self.keyframes:
            time -= k.time
            if time < 0:
                # TODO interpolate
                if k.start is not None:
                    val = k.start
                break
            if k.end is not None:
                val = k.end
        return val


class MultiDimensional(TgsObject, AnimatableMixin):
    keyframe_type = OffsetKeyframe
    _props = [
        TgsProp("value", "k", float, True, lambda l: not l["a"]),
        TgsProp("property_index", "ix", int, False),
        TgsProp("animated", "a", PseudoBool, False),
        TgsProp("keyframes", "k", OffsetKeyframe, True, lambda l: l["a"]),
    ]


class GradientColors(TgsObject):
    _props = [
        TgsProp("colors", "k", MultiDimensional),
        TgsProp("count", "p", int),
    ]

    def __init__(self):
        self.colors = MultiDimensional([])
        self.count = 0

    def set_colors(self, colors, keyframe=None):
        flat = self._flatten_colors(colors)
        if self.colors.animated and keyframe is not None:
            if keyframe > 1:
                self.colors.keyframes[keyframe-1].end = flat
            self.colors.keyframes[keyframe].start = flat
        else:
            self.colors.clear_animation(flat)
        self.count = len(colors)

    def _flatten_colors(self, colors):
        return reduce(
            lambda a, b: a + b,
            map(
                lambda it: [it[0] / (len(colors)-1)] + it[1],
                enumerate(colors),
            )
        )

    def add_color(self, offset, color, keyframe=None):
        flat = [offset] + color
        if self.colors.animated:
            if keyframe is None:
                for kf in self.colors.keyframes:
                    if kf.start:
                        kf.start += flat
                    if kf.end:
                        kf.end += flat
            else:
                if keyframe > 1:
                    self.colors.keyframes[keyframe-1].end += flat
                self.colors.keyframes[keyframe].start += flat
        else:
            self.colors.value += flat
        self.count += 1

    def add_keyframe(self, time, colors=None):
        self.colors.add_keyframe(time, self._flatten_colors(colors) if colors else [])


class Value(TgsObject, AnimatableMixin):
    keyframe_type = OffsetKeyframe
    _props = [
        TgsProp("value", "k", float, False, lambda l: not l["a"]),
        TgsProp("property_index", "ix", int, False),
        TgsProp("animated", "a", PseudoBool, False),
        TgsProp("keyframes", "k", keyframe_type, True, lambda l: l["a"]),
    ]

    def __init__(self, value=0):
        super().__init__(value)

    def add_keyframe(self, time, value):
        super().add_keyframe(time, [value])

    def get_value(self, time=0):
        v = super().get_value(time)
        if self.animated and self.keyframes:
            return v[0]
        return v


class Bezier(TgsObject):
    _props = [
        TgsProp("closed", "c", bool, False),
        TgsProp("in_point", "i", list, True),
        TgsProp("out_point", "o", list, True),
        TgsProp("vertices", "v", list, True),
    ]

    def __init__(self):
        # Closed property of shape
        self.closed = False
        # Bezier curve In points. Array of 2 dimensional arrays.
        self.in_point = []
        # Bezier curve Out points. Array of 2 dimensional arrays.
        self.out_point = []
        # Bezier curve Vertices. Array of 2 dimensional arrays.
        self.vertices = []

    def add_point(self, pos, inp=[0, 0], outp=[0, 0]):
        self.vertices.append(pos)
        self.in_point.append(list(inp))
        self.out_point.append(list(outp))
        return self

    def add_smooth_point(self, pos, inp):
        self.add_point(pos, inp, [-inp[0], -inp[1]])
        return self

    def close(self, closed=True):
        self.closed = closed
        return self


class ShapePropKeyframe(TgsObject):
    _props = [
        TgsProp("start", "s", Bezier, PseudoList),
        TgsProp("end", "e", Bezier, PseudoList),
        TgsProp("time", "t", float, False),
        TgsProp("in_value", "i", KeyframeBezierPoint, False),
        TgsProp("out_value", "o", KeyframeBezierPoint, False),
    ]

    def __init__(self, time=0, start=None, end=None):
        # Start value of keyframe segment.
        self.start = start
        self.end = end
        # Start time of keyframe segment.
        self.time = time
        # Bezier curve interpolation in value.
        self.in_value = None
        # Bezier curve interpolation out value.
        self.out_value = None

    def set_tangents(self, end_time):
        _set_tangents(self, 0, 0, end_time)


class ShapeProperty(TgsObject, AnimatableMixin):
    keyframe_type = ShapePropKeyframe
    _props = [
        TgsProp("value", "k", Bezier, False, lambda l: not l["a"]),
        #TgsProp("expression", "x", str, False),
        TgsProp("property_index", "ix", float, False),
        TgsProp("animated", "a", PseudoBool, False),
        TgsProp("keyframes", "k", keyframe_type, True, lambda l: l["a"]),
    ]

    def __init__(self):
        super().__init__(Bezier())
