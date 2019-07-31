from .base import TgsObject, TgsProp
from ..utils.nvector import NVector


class BezierPointView:
    """
    View for bezier point
    """
    def __init__(self, bezier, index):
        self.bezier = bezier
        self.index = index

    @property
    def vertex(self):
        return self.bezier.vertices[self.index]

    @vertex.setter
    def vertex(self, point):
        self.bezier.vertices[self.index] = point

    @property
    def in_point(self):
        return self.in_point.vertices[self.index]

    @in_point.setter
    def in_point(self, point):
        self.in_point.vertices[self.index] = point

    @property
    def out_point(self):
        return self.out_point.vertices[self.index]

    @out_point.setter
    def out_point(self, point):
        self.out_point.vertices[self.index] = point


class AbsoluteBezierPointView(BezierPointView):
    @property
    def in_point(self):
        return self.in_point.vertices[self.index] + self.vertex

    @in_point.setter
    def in_point(self, point):
        self.in_point.vertices[self.index] = point - self.vertex

    @property
    def out_point(self):
        return self.out_point.vertices[self.index] + self.vertex

    @out_point.setter
    def out_point(self, point):
        self.out_point.vertices[self.index] = point - self.vertex


class BezierView:
    def __init__(self, bezier, absolute=False):
        self.bezier = bezier
        self.is_absolute = absolute

    def point(self, index):
        if self.is_absolute:
            return AbsoluteBezierPointView(self.bezier, index)
        return BezierPointView(self.bezier, index)

    def __len__(self):
        return len(self.bezier.vertices)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [
                self.point(i)
                for i in key
            ]
        return self.point(key)

    def __iter__(self):
        for i in range(len(self)):
            yield self.point(i)

    @property
    def absolute(self):
        return BezierView(self.bezier, True)


## \ingroup Lottie
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
        #self.rel_tangents = rel_tangents
        ## More convent way to  access points
        self.points = BezierView(self)

    def clone(self):
        clone = Bezier()
        clone.closed = self.closed
        clone.in_point = [p.clone() for p in self.in_point]
        clone.out_point = [p.clone() for p in self.out_point]
        clone.vertices = [p.clone() for p in self.vertices]
        #clone.rel_tangents = self.rel_tangents
        return clone

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
        #if not self.rel_tangents:
            #self.in_point[-1] += pos
            #self.out_point[-1] += pos
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

    """def to_absolute(self):
        if self.rel_tangents:
            self.rel_tangents = False
            for i in range(len(self.vertices)):
                p = self.vertices[i]
                self.in_point[i] += p
                self.out_point[i] += p
        return self"""
