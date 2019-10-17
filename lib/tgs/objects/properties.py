import math
from functools import reduce
from .base import TgsObject, TgsProp, PseudoList, PseudoBool
from . import easing
from ..nvector import NVector
from .bezier import Bezier


class KeyframeBezier:
    NEWTON_ITERATIONS = 4
    NEWTON_MIN_SLOPE = 0.001
    SUBDIVISION_PRECISION = 0.0000001
    SUBDIVISION_MAX_ITERATIONS = 10
    SPLINE_TABLE_SIZE = 11
    SAMPLE_STEP_SIZE = 1.0 / (SPLINE_TABLE_SIZE - 1.0)

    def __init__(self, h1, h2):
        self.h1 = h1
        self.h2 = h2
        self._sample_values = None

    @classmethod
    def from_keyframe(cls, keyframe):
        return cls(keyframe.out_value, keyframe.in_value)

    def bezier(self):
        bez = Bezier()
        bez.add_point(NVector(0, 0), outp=NVector(self.h1.x, self.h1.y))
        bez.add_point(NVector(1, 1), inp=NVector(self.h2.x-1, self.h2.y-1))
        return bez

    def _a(self, c1, c2):
        return 1 - 3 * c2 + 3 * c1

    def _b(self, c1, c2):
        return 3 * c2 - 6 * c1

    def _c(self, c1):
        return 3 * c1

    def _bezier_component(self, t, c1, c2):
        return ((self._a(c1, c2) * t + self._b(c1, c2)) * t + self._c(c1)) * t

    def point_at(self, t):
        return NVector(
            self._bezier_component(t, self.h1.x, self.h2.x),
            self._bezier_component(t, self.h1.y, self.h2.y)
        )

    def _slope_component(self, t, c1, c2):
        return 3 * self._a(c1, c2) * t * t + 2 * self._b(c1, c2) * t + self._c(c1)

    def slope_at(self, t):
        return NVector(
            self._slope_component(t, self.h1.x, self.h2.x),
            self._slope_component(t, self.h1.y, self.h2.y)
        )

    def _binary_subdivide(self, x, interval_start, interval_end):
        current_x = None
        t = None
        i = 0
        for i in range(self.SUBDIVISION_MAX_ITERATIONS):
            if current_x is not None and abs(current_x) < self.SUBDIVISION_PRECISION:
                break
            t = interval_start + (interval_end - interval_start) / 2.0
            current_x = self._bezier_component(t, self.h1.x, self.h2.x) - x
            if current_x > 0.0:
                interval_end = t
            else:
                interval_start = t
        return t

    def _newton_raphson(self, x, t_guess):
        for i in range(self.NEWTON_ITERATIONS):
            slope = self._slope_component(t_guess, self.h1.x, self.h2.x)
            if slope == 0:
                return t_guess
            current_x = self._bezier_component(t_guess, self.h1.x, self.h2.x) - x
            t_guess -= current_x / slope
        return t_guess

    def _get_sample_values(self):
        if self._sample_values is None:
            self._sample_values = [
                self._bezier_component(i * self.SAMPLE_STEP_SIZE, self.h1.x, self.h2.x)
                for i in range(self.SPLINE_TABLE_SIZE)
            ]
        return self._sample_values

    def t_for_x(self, x):
        sample_values = self._get_sample_values()
        interval_start = 0
        current_sample = 1
        last_sample = self.SPLINE_TABLE_SIZE - 1
        while current_sample != last_sample and sample_values[current_sample] <= x:
            interval_start += self.SAMPLE_STEP_SIZE
            current_sample += 1
        current_sample -= 1

        dist = (x - sample_values[current_sample]) / (sample_values[current_sample+1] - sample_values[current_sample])
        t_guess = interval_start + dist * self.SAMPLE_STEP_SIZE
        initial_slope = self._slope_component(t_guess, self.h1.x, self.h2.x)
        if initial_slope >= self.NEWTON_MIN_SLOPE:
            return self._newton_raphson(x, t_guess)
        if initial_slope == 0:
            return t_guess
        return self._binary_subdivide(x, interval_start, interval_start + self.SAMPLE_STEP_SIZE)

    def y_at_x(self, x):
        t = self.t_for_x(x)
        return self._bezier_component(t, self.h1.y, self.h2.y)


## \ingroup Lottie
class Keyframe(TgsObject):
    _props = [
        TgsProp("time", "t", float, False),
        TgsProp("in_value", "i", easing.KeyframeBezierHandle, False),
        TgsProp("out_value", "o", easing.KeyframeBezierHandle, False),
        TgsProp("jump", "h", PseudoBool),
    ]

    def __init__(self, time=0, easing_function=None):
        """!
        \param time             Start time of keyframe segment
        \param easing_function  Callable that performs the easing
        """
        ## Start time of keyframe segment.
        self.time = time
        ## Bezier curve easing in value.
        self.in_value = None
        ## Bezier curve easing out value.
        self.out_value = None
        ## Jump to the end value
        self.jump = None

        if easing_function:
            easing_function(self)

    def bezier(self):
        if self.jump:
            bez = Bezier()
            bez.add_point(NVector(0, 0))
            bez.add_point(NVector(1, 0))
            bez.add_point(NVector(1, 1))
            return bez
        else:
            return KeyframeBezier.from_keyframe(self).bezier()

    def lerp_factor(self, ratio):
        return KeyframeBezier.from_keyframe(self).y_at_x(ratio)


## \ingroup Lottie
class OffsetKeyframe(Keyframe):
    """!
    Keyframe for MultiDimensional values

    @par Bezier easing
    @parblock
    Imagine a quadratic bezier, with starting point at (0, 0) and end point at (1, 1).

    \p out_value and \p in_value are the other two handles for a quadratic bezier,
    expressed as absoulte values in this 0-1 space.

    See also https://cubic-bezier.com/
    @endparblock
    """
    _props = [
        TgsProp("start", "s", NVector, False),
        TgsProp("end", "e", NVector, False),
        TgsProp("in_tan", "ti", float, True),
        TgsProp("out_tan", "to", float, True),
    ]

    def __init__(self, time=0, start=None, end=None, easing_function=None):
        Keyframe.__init__(self, time, easing_function)
        ## Start value of keyframe segment.
        self.start = start
        ## End value of keyframe segment.
        self.end = end
        ## In Spatial Tangent. Only for spatial properties. Array of numbers.
        self.in_tan = None
        ## Out Spatial Tangent. Only for spatial properties. Array of numbers.
        self.out_tan = None

    def interpolated_value(self, ratio, next_start=None):
        end = next_start if self.end is None else self.end
        if end is None:
            return self.start
        if not self.in_value or not self.out_value:
            return self.start
        if ratio == 1:
            return end
        if ratio == 0:
            return self.start
        lerpv = self.lerp_factor(ratio)
        return self.start.lerp(end, lerpv)


class AnimatableMixin:
    keyframe_type = Keyframe

    def __init__(self, value=None):
        ## Non-animated value
        self.value = value
        ## Property index
        self.property_index = None
        ## Whether it's animated
        self.animated = False
        ## Keyframe list
        self.keyframes = None

    def clear_animation(self, value):
        """!
        Sets a fixed value, removing animated keyframes
        """
        self.value = value
        self.animated = False
        self.keyframes = None

    def add_keyframe(self, time, value, interp=easing.Linear()):
        """!
        \param time     The time this keyframe appears in
        \param value    The value the property should have at \p time
        \param interp   The easing callable used to update the tangents of the previous keyframe
        @note Always call add_keyframe with increasing \p time value
        """
        if not self.animated:
            self.value = None
            self.keyframes = []
            self.animated = True
        else:
            if self.keyframes[-1].time == time:
                if value != self.keyframes[-1].start:
                    self.keyframes[-1].start = value
                return
            else:
                self.keyframes[-1].end = value.clone()

        self.keyframes.append(self.keyframe_type(
            time,
            value,
            None,
            interp
        ))

    def get_value(self, time=0):
        """!
        @brief Returns the value of the property at the given frame/time
        \todo honour easing
        """
        if not self.animated:
            return self.value

        if not self.keyframes:
            return None

        val = self.keyframes[0].start
        for i in range(len(self.keyframes)):
            k = self.keyframes[i]
            if time - k.time <= 0:
                if k.start is not None:
                    val = k.start

                kp = self.keyframes[i-1] if i > 0 else None
                if kp:
                    end = kp.end
                    if end is None and i + 1 < len(self.keyframes):
                        end = self.keyframes[i+1].start
                    if end is not None:
                        val = kp.interpolated_value((time - kp.time) / (k.time - kp.time), end)
                break
            if k.end is not None:
                val = k.end
        return val

    def to_dict(self):
        d = super().to_dict()
        if self.animated:
            last = d["k"][-1]
            last.pop("i", None)
            last.pop("o", None)
        return d


## \ingroup Lottie
class MultiDimensional(AnimatableMixin, TgsObject):
    """!
    An animatable property that holds a NVector
    """
    keyframe_type = OffsetKeyframe
    _props = [
        TgsProp("value", "k", NVector, False, lambda l: not l.get("a", None)),
        TgsProp("property_index", "ix", int, False),
        TgsProp("animated", "a", PseudoBool, False),
        TgsProp("keyframes", "k", OffsetKeyframe, True, lambda l: l.get("a", None)),
    ]


## \ingroup Lottie
# \todo use a more convenient representation and convert to the weird array on import/export
class GradientColors(TgsObject):
    """!
    Represents colors and offsets in a gradient
    """
    _props = [
        TgsProp("colors", "k", MultiDimensional),
        TgsProp("count", "p", int),
    ]

    def __init__(self, colors=[]):
        ## Animatable colors, as a vector containing [offset, r, g, b] values as a flat array
        self.colors = MultiDimensional(NVector())
        ## Number of colors
        self.count = 0
        if colors:
            self.set_colors(colors)

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
        return NVector(*reduce(
            lambda a, b: a + b,
            map(
                lambda it: [it[0] / (len(colors)-1)] + it[1].components,
                enumerate(colors),
            )
        ))

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
                    self.colors.keyframes[keyframe-1].end.components += flat
                self.colors.keyframes[keyframe].start.components += flat
        else:
            self.colors.value.components += flat
        self.count += 1

    def add_keyframe(self, time, colors=None, ease=easing.Linear()):
        self.colors.add_keyframe(time, self._flatten_colors(colors) if colors else NVector(), ease)


## \ingroup Lottie
class Value(AnimatableMixin, TgsObject):
    """!
    An animatable property that holds a float
    """
    keyframe_type = OffsetKeyframe
    _props = [
        TgsProp("value", "k", float, False, lambda l: not l.get("a", None)),
        TgsProp("property_index", "ix", int, False),
        TgsProp("animated", "a", PseudoBool, False),
        TgsProp("keyframes", "k", keyframe_type, True, lambda l: l.get("a", None)),
    ]

    def __init__(self, value=0):
        super().__init__(value)

    def add_keyframe(self, time, value, ease=easing.Linear()):
        super().add_keyframe(time, NVector(value), ease)

    def get_value(self, time=0):
        v = super().get_value(time)
        if self.animated and self.keyframes:
            return v[0]
        return v


## \ingroup Lottie
class ShapePropKeyframe(Keyframe):
    """!
    Keyframe holding Bezier objects
    """
    _props = [
        TgsProp("start", "s", Bezier, PseudoList),
        TgsProp("end", "e", Bezier, PseudoList),
    ]

    def __init__(self, time=0, start=None, end=None, easing_function=None):
        Keyframe.__init__(self, time, easing_function)
        ## Start value of keyframe segment.
        self.start = start
        ## End value of keyframe segment.
        self.end = end

    def interpolated_value(self, ratio, next_start=None):
        end = next_start if self.end is None else self.end
        if end is None:
            return self.start
        if not self.in_value or not self.out_value:
            return self.start
        if ratio == 1:
            return end
        if ratio == 0 or len(self.start.vertices) != len(end.vertices):
            return self.start

        lerpv = self.lerp_factor(ratio)
        bez = Bezier()
        bez.closed = self.start.closed
        for i in range(len(self.start.vertices)):
            bez.vertices.append(self.start.vertices[i].lerp(end.vertices[i], lerpv))
            bez.in_tangents.append(self.start.in_tangents[i].lerp(end.in_tangents[i], lerpv))
            bez.out_tangents.append(self.start.out_tangents[i].lerp(end.out_tangents[i], lerpv))
        return bez


## \ingroup Lottie
class ShapeProperty(AnimatableMixin, TgsObject):
    """!
    An animatable property that holds a Bezier
    """
    keyframe_type = ShapePropKeyframe
    _props = [
        TgsProp("value", "k", Bezier, False, lambda l: not l["a"]),
        #TgsProp("expression", "x", str, False),
        TgsProp("property_index", "ix", float, False),
        TgsProp("animated", "a", PseudoBool, False),
        TgsProp("keyframes", "k", keyframe_type, True, lambda l: l["a"]),
    ]

    def __init__(self, bezier=None):
        super().__init__(bezier or Bezier())
