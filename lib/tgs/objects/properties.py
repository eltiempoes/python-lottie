import math
from functools import reduce
from .base import TgsObject, TgsProp, PseudoList, PseudoBool
from . import easing
from ..utils.nvector import NVector


##\ingroup Lottie
class OffsetKeyframe(TgsObject):
    """!
    Keyframe for MultiDimensional values
    """
    _props = {
        TgsProp("start", "s", NVector, False),
        TgsProp("end", "e", NVector, False),
        TgsProp("time", "t", float, False),
        TgsProp("in_value", "i", easing.KeyframeBezierHandle, False),
        TgsProp("out_value", "o", easing.KeyframeBezierHandle, False),
        TgsProp("in_tan", "ti", float, True),
        TgsProp("out_tan", "to", float, True),
        #TgsProp("h" ,"h"),
    }

    def __init__(self, time=0, start=None, end=None,
                 in_value=None, out_value=None, in_tan=None, out_tan=None):
        ## Start value of keyframe segment.
        self.start = start
        ## End value of keyframe segment.
        self.end = end
        ## Start time of keyframe segment.
        self.time = time
        ## Bezier curve easing in value.
        self.in_value = in_value
        ## Bezier curve easing out value.
        self.out_value = out_value
        ## In Spatial Tangent. Only for spatial properties. Array of numbers.
        self.in_tan = in_tan
        ## Out Spatial Tangent. Only for spatial properties. Array of numbers.
        self.out_tan = out_tan

    def set_tangents(self, end_time, interp):
        """!
        Updates the bezier tangents for this keyframe
        \param end_time The time of the next keyframe
        \param interp   Callable that performs the easing
        """
        to_val = lambda vals: math.sqrt(sum(map(lambda x: x**2, vals)))
        start = to_val(self.start)
        end = to_val(self.end)
        interp(self, start, end, end_time)


class AnimatableMixin:
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
        \note Always call add_keyframe with increasing \p time value
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
            self.keyframes[-1].end = value
            self.keyframes[-1].set_tangents(time, interp)

        self.keyframes.append(self.keyframe_type(
            time,
            value,
            None,
        ))

    def get_value(self, time=0):
        """!
        \brief Returns the value of the property at the given frame/time
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
                if kp and isinstance(val, NVector):
                    prev = kp.start
                    # TODO honour easing
                    val = prev.lerp(val, (time - kp.time) / (k.time - kp.time))
                break
            if k.end is not None:
                val = k.end
        return val


##\ingroup Lottie
class MultiDimensional(TgsObject, AnimatableMixin):
    """!
    An animatable property that holds a NVector
    """
    keyframe_type = OffsetKeyframe
    _props = [
        TgsProp("value", "k", NVector, False, lambda l: not l["a"]),
        TgsProp("property_index", "ix", int, False),
        TgsProp("animated", "a", PseudoBool, False),
        TgsProp("keyframes", "k", OffsetKeyframe, True, lambda l: l["a"]),
    ]


##\ingroup Lottie
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


##\ingroup Lottie
class Value(TgsObject, AnimatableMixin):
    """!
    An animatable property that holds a float
    """
    keyframe_type = OffsetKeyframe
    _props = [
        TgsProp("value", "k", float, False, lambda l: not l["a"]),
        TgsProp("property_index", "ix", int, False),
        TgsProp("animated", "a", PseudoBool, False),
        TgsProp("keyframes", "k", keyframe_type, True, lambda l: l["a"]),
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


##\ingroup Lottie
# \todo Use BezierPoint and convert to in_point/out_point/vertices on import/export
class Bezier(TgsObject):
    """!
    Single bezier curve
    """
    _props = [
        TgsProp("closed", "c", bool, False),
        TgsProp("in_point", "i", NVector, True),
        TgsProp("out_point", "o", NVector, True),
        TgsProp("vertices", "v", NVector, True),
    ]

    def __init__(self):
        ## Closed property of shape
        self.closed = False
        ## Bezier curve In points. Array of 2 dimensional arrays.
        self.in_point = []
        ## Bezier curve Out points. Array of 2 dimensional arrays.
        self.out_point = []
        ## Bezier curve Vertices. Array of 2 dimensional arrays.
        self.vertices = []

    def insert_point(self, index, pos, inp=NVector(0, 0), outp=NVector(0, 0)):
        """!
        Inserts a point at the given index
        \param index    Index to insert the point at
        \param pos      Point to add
        \param inp      Tangent entering the point, as a vector relative to \p pos
        \param outp     Tangent exiting the point, as a vector relative to \p pos
        \returns \c self, for easy chaining
        """
        self.vertices.insert(index, pos)
        self.in_point.insert(index, inp.clone())
        self.out_point.insert(index, outp.clone())
        return self

    def add_point(self, pos, inp=NVector(0, 0), outp=NVector(0, 0)):
        """!
        Appends a point to the curve
        \see insert_point
        """
        self.insert_point(len(self.vertices), pos, inp, outp)
        return self

    def add_smooth_point(self, pos, inp):
        """!
        Appends a point with symmetrical tangents
        \see insert_point
        """
        self.add_point(pos, inp, -inp)
        return self

    def close(self, closed=True):
        """!
        Updates self.closed
        \returns \c self, for easy chaining
        """
        self.closed = closed
        return self

    def point_at(self, t):
        """!
        \param t    A value between 0 and 1, percentage along the length of the curve
        \returns    The point at \p t in the curve
        """
        i, t = self._index_t(t)
        points = self._bezier_points(i, True)
        return self._solve_bezier(t, points)

    def _split(self, t):
        i, t = self._index_t(t)
        cub = self._bezier_points(i, True)
        split1, split2 = self._split_segment(t, cub)
        return i, split1, split2

    def _split_segment(self, t, cub):
        quad = self._solve_bezier_step(t, cub)
        lin = self._solve_bezier_step(t, quad)
        k = self._solve_bezier_step(t, lin)[0]
        split1 = [cub[0], quad[0]-cub[0], lin[0]-k, k]
        split2 = [k, lin[-1]-k, quad[-1]-cub[-1], cub[-1]]
        return split1, split2

    def split_at(self, t):
        """!
        Get two pieces out of a Bezier curve
        \param t    A value between 0 and 1, percentage along the length of the curve
        \returns Two Bezier objects that correspond to self, but split at \p t
        """
        i, split1, split2 = self._split(t)

        seg1 = Bezier()
        seg2 = Bezier()
        for j in range(i):
            seg1.add_point(self.vertices[j].clone(), self.in_point[j].clone(), self.out_point[j].clone())
        for j in range(i+2, len(self.vertices)):
            seg2.add_point(self.vertices[j].clone(), self.in_point[j].clone(), self.out_point[j].clone())

        seg1.add_point(split1[0], self.in_point[i].clone(), split1[1])
        seg1.add_point(split1[3], split1[2], split2[1])

        seg2.insert_point(0, split2[0], split1[2], split2[1])
        seg2.insert_point(1, split2[3], split2[2], self.out_point[i+1].clone())

        return seg1, seg2

    def segment(self, t1, t2):
        """!
        Splits a Bezier in two points and returns the segment between the
        \param t1   A value between 0 and 1, percentage along the length of the curve
        \param t2   A value between 0 and 1, percentage along the length of the curve
        \returns Bezier object that correspond to the segment between \p t1 and \p t2
        """
        if t1 > t2:
            [t1, t2] = [t2, t1]
        elif t1 == t2:
            seg = Bezier()
            p = self.point_at(t1)
            seg.add_point(p)
            seg.add_point(p)
            return seg

        seg1, seg2 = self.split_at(t1)
        t2p = (t2-t1) / (1-t1)
        seg3, seg4 = seg2.split_at(t2p)
        return seg3

    def split_self_multi(self, positions):
        """!
        Adds more points to the Bezier
        \param positions    list of percentages along the curve
        """
        if not len(positions):
            return
        t1 = positions[0]
        seg1, seg2 = self.split_at(t1)
        self.vertices = []
        self.in_point = []
        self.out_point = []

        self.vertices = seg1.vertices[:-1]
        self.in_point = seg1.in_point[:-1]
        self.out_point = seg1.out_point[:-1]

        for t2 in positions[1:]:
            t = (t2-t1) / (1-t1)
            seg1, seg2 = seg2.split_at(t)
            t1 = t
            self.vertices += seg1.vertices[:-1]
            self.in_point += seg1.in_point[:-1]
            self.out_point += seg1.out_point[:-1]

        self.vertices += seg2.vertices
        self.in_point += seg2.in_point
        self.out_point += seg2.out_point

    def split_each_segment(self):
        """!
        Adds a point in the middle of the segment between every pair of points in the Bezier
        """
        vertices = self.vertices
        in_point = self.in_point
        out_point = self.out_point

        self.vertices = []
        self.in_point = []
        self.out_point = []

        for i in range(len(vertices)-1):
            tocut = [vertices[i], out_point[i]+vertices[i], in_point[i+1]+vertices[i+1], vertices[i+1]]
            split1, split2 = self._split_segment(0.5, tocut)
            if i:
                self.out_point[-1] = split1[1]
            else:
                self.add_point(vertices[0], in_point[0], split1[1])
            self.add_point(split1[3], split1[2], split2[1])
            self.add_point(vertices[i+1], split2[2], NVector(0, 0))

    def split_self_chunks(self, n_chunks):
        """!
        Adds points the Bezier, splitting it into \p n_chunks additional chunks.
        """
        splits = [i/n_chunks for i in range(1, n_chunks)]
        return self.split_self_multi(splits)

    def _bezier_points(self, i, optimize):
        v1 = self.vertices[i].clone()
        v2 = self.vertices[i+1].clone()
        points = [v1]
        t1 = self.out_point[i].clone()
        if optimize or t1.length != 0:
            points.append(t1+v1)
        t2 = self.in_point[i+1].clone()
        if optimize or t1.length != 0:
            points.append(t2+v2)
        points.append(v2)
        return points

    def _solve_bezier_step(self, t, points):
        next = []
        p1 = points[0]
        for p2 in points[1:]:
            next.append(p1 * (1-t) + p2 * t)
            p1 = p2
        return next

    def _solve_bezier(self, t, points):
        while len(points) > 1:
            points = self._solve_bezier_step(t, points)
        return points[0]

    def _index_t(self, t):
        if t <= 0:
            return 0, 0

        if t >= 1:
            return len(self.vertices)-2, 1

        n = len(self.vertices)-1
        for i in range(n):
            if (i+1) / n > t:
                break

        return i, (t - (i/n)) * n

    def reverse(self):
        """!
        Reverses the Bezier curve
        """
        self.vertices = list(reversed(self.vertices))
        out_point = list(reversed(self.in_point))
        in_point = list(reversed(self.out_point))
        self.in_point = in_point
        self.out_point = out_point


##\ingroup Lottie
class ShapePropKeyframe(TgsObject):
    """!
    Keyframe holding Bezier objects
    """
    _props = [
        TgsProp("start", "s", Bezier, PseudoList),
        TgsProp("end", "e", Bezier, PseudoList),
        TgsProp("time", "t", float, False),
        TgsProp("in_value", "i", easing.KeyframeBezierHandle, False),
        TgsProp("out_value", "o", easing.KeyframeBezierHandle, False),
    ]

    def __init__(self, time=0, start=None, end=None):
        ## Start value of keyframe segment.
        self.start = start
        ## End value of keyframe segment.
        self.end = end
        ## Start time of keyframe segment.
        self.time = time
        ## Bezier curve easing in value.
        self.in_value = None
        ## Bezier curve easing out value.
        self.out_value = None

    def set_tangents(self, end_time, interp=easing.Linear()):
        """!
        Updates the bezier tangents for this keyframe
        \param end_time The time of the next keyframe
        \param interp   Callable that performs the easing
        """
        interp(self, 0, 0, end_time)


##\ingroup Lottie
class ShapeProperty(TgsObject, AnimatableMixin):
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

    def __init__(self):
        super().__init__(Bezier())
