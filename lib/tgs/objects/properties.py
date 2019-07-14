import math
from functools import reduce
from .base import TgsObject, TgsProp, PseudoList, PseudoBool
from . import easing
from ..utils.nvector import NVector


class OffsetKeyframe(TgsObject):
    _props = {
        TgsProp("start", "s", float, True),
        TgsProp("end", "e", float, True),
        TgsProp("time", "t", float, False),
        TgsProp("in_value", "i", easing.KeyframeBezierPoint, False),
        TgsProp("out_value", "o", easing.KeyframeBezierPoint, False),
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
        # Bezier curve easing in value.
        self.in_value = in_value
        # Bezier curve easing out value.
        self.out_value = out_value
        #self.h = 1 #???
        # In Spatial Tangent. Only for spatial properties. Array of numbers.
        self.in_tan = in_tan
        # Out Spatial Tangent. Only for spatial properties. Array of numbers.
        self.out_tan = out_tan

    def set_tangents(self, end_time, interp):
        to_val = lambda vals: math.sqrt(sum(map(lambda x: x**2, vals)))
        start = to_val(self.start)
        end = to_val(self.end)
        interp(self, start, end, end_time)


class AnimatableMixin:
    def __init__(self, value=None):
        self.value = value
        self.property_index = None
        self.animated = False
        self.keyframes = None

    def clear_animation(self, value):
        self.value = value
        self.animated = False

    def add_keyframe(self, time, value, interp=easing.Linear()):
        if not self.animated:
            self.value = None
            self.keyframes = []
            self.animated = True
        else:
            self.keyframes[-1].end = value
            self.keyframes[-1].set_tangents(time, interp)

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
            if time <= 0:
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

    def add_keyframe(self, time, colors=None, ease=easing.Linear()):
        self.colors.add_keyframe(time, self._flatten_colors(colors) if colors else [], ease)


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

    def add_keyframe(self, time, value, ease=easing.Linear()):
        super().add_keyframe(time, [value], ease)

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

    def insert_point(self, index, pos, inp=[0, 0], outp=[0, 0]):
        self.vertices.insert(index, pos)
        self.in_point.insert(index, list(inp))
        self.out_point.insert(index, list(outp))
        return self

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

    def point_at(self, t):
        i, t = self._index_t(t)
        points = self._bezier_points(i, True)
        return self._solve_bezier(t, points)

    def _split(self, t):
        i, t = self._index_t(t)
        cub = self._bezier_points(i, True)
        quad = self._solve_bezier_step(t, cub)
        lin = self._solve_bezier_step(t, quad)
        k = self._solve_bezier_step(t, lin)[0]
        split1 = [cub[0], quad[0]-cub[0], lin[0]-k, k]
        split2 = [k, lin[-1]-k, quad[-1]-cub[-1], cub[-1]]
        return i, split1, split2

    def split_at(self, t):
        i, split1, split2 = self._split(t)

        seg1 = Bezier()
        seg2 = Bezier()
        for j in range(i):
            seg1.add_point(list(self.vertices[j]), list(self.in_point[j]), list(self.out_point[j]))
        for j in range(i+2, len(self.vertices)):
            seg2.add_point(list(self.vertices[j]), list(self.in_point[j]), list(self.out_point[j]))

        seg1.add_point(split1[0].to_list(), list(self.in_point[i]), split1[1].to_list())
        seg1.add_point(split1[3].to_list(), split1[2].to_list(), split2[1].to_list())

        seg2.insert_point(0, split2[0].to_list(), split1[2].to_list(), split2[1].to_list())
        seg2.insert_point(1, split2[3].to_list(), split2[2].to_list(), list(self.out_point[i+1]))

        return seg1, seg2

    def segment(self, t1, t2):
        if t1 > t2:
            [t1, t2] = [t2, t1]
        elif t1 == t2:
            seg = Bezier()
            p = self.point_at(t1)
            seg.add_point(p.to_list())
            seg.add_point(p.to_list())
            return seg

        seg1, seg2 = self.split_at(t1)
        t2p = (t2-t1) / (1-t1)
        seg3, seg4 = seg2.split_at(t2p)
        return seg3

    def split_self_multi(self, positions):
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

    def split_self_chunks(self, n_chunks):
        splits = [i/n_chunks for i in range(1, n_chunks)]
        return self.split_self_multi(splits)

    def _bezier_points(self, i, optimize):
        v1 = NVector(*self.vertices[i])
        v2 = NVector(*self.vertices[i+1])
        points = [v1]
        t1 = NVector(*self.out_point[i])
        if optimize or t1.length != 0:
            points.append(t1+v1)
        t2 = NVector(*self.in_point[i+1])
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
        self.vertices = list(reversed(self.vertices))
        out_point = list(reversed(self.in_point))
        in_point = list(reversed(self.out_point))
        self.in_point = in_point
        self.out_point = out_point


class ShapePropKeyframe(TgsObject):
    _props = [
        TgsProp("start", "s", Bezier, PseudoList),
        TgsProp("end", "e", Bezier, PseudoList),
        TgsProp("time", "t", float, False),
        TgsProp("in_value", "i", easing.KeyframeBezierPoint, False),
        TgsProp("out_value", "o", easing.KeyframeBezierPoint, False),
    ]

    def __init__(self, time=0, start=None, end=None):
        # Start value of keyframe segment.
        self.start = start
        self.end = end
        # Start time of keyframe segment.
        self.time = time
        # Bezier curve easing in value.
        self.in_value = None
        # Bezier curve easing out value.
        self.out_value = None

    def set_tangents(self, end_time, interp=easing.Linear()):
        interp(self, 0, 0, end_time)


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
