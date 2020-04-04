import math
from ..nvector import NVector


def _sign(x):
    if x < 0:
        return -1
    return 1


class TransformMatrix:
    scalar = float

    def __init__(self):
        """ Creates an Identity matrix """
        self.to_identity()

    def clone(self):
        m = TransformMatrix()
        m._mat = list(self._mat)
        return m

        return self

    def __getitem__(self, key):
        row, col = key
        return self._mat[row*3+col]

    def __setitem__(self, key, value):
        row, col = key
        self._mat[row*3+col] = self.scalar(value)

    @property
    def a(self):
        return self[0, 0]

    @a.setter
    def a(self, v):
        self[0, 0] = self.scalar(v)

    @property
    def b(self):
        return self[1, 0]

    @b.setter
    def b(self, v):
        self[1, 0] = self.scalar(v)

    @property
    def c(self):
        return self[0, 1]

    @c.setter
    def c(self, v):
        self[0, 1] = self.scalar(v)

    @property
    def d(self):
        return self[1, 1]

    @d.setter
    def d(self, v):
        self[1, 1] = self.scalar(v)

    @property
    def tx(self):
        return self[0, 2]

    @tx.setter
    def tx(self, v):
        self[0, 2] = self.scalar(v)

    @property
    def ty(self):
        return self[1, 2]

    @ty.setter
    def ty(self, v):
        self[1, 2] = self.scalar(v)

    def __str__(self):
        return str(self._mat)

    def scale(self, x, y=None):
        if y is None:
            y = x

        m = TransformMatrix()
        m.a = x
        m.d = y
        self *= m
        return self

    def translate(self, x, y):
        m = TransformMatrix()
        m.tx = x
        m.ty = y
        self *= m
        return self

    def skew(self, x_rad, y_rad):
        m = TransformMatrix()
        m.c = math.tan(x_rad)
        m.b = math.tan(y_rad)
        self *= m
        return self

    def row(self, i):
        return NVector(self[i, 0], self[i, 1], self[i, 2])

    def column(self, i):
        return NVector(self[0, i], self[1, i], self[2, i])

    def to_identity(self):
        self._mat = [
            1., 0., 0.,
            0., 1., 0.,
            0., 0., 1.,
        ]

    def apply(self, vector):
        vector3 = NVector(vector.x, vector.y, 1)
        return NVector(
            self.row(0).dot(vector3),
            self.row(1).dot(vector3),
        )

    @classmethod
    def rotation(cls, radians):
        m = cls()
        m.a = math.cos(radians)
        m.b = math.sin(radians)
        m.c = -math.sin(radians)
        m.d = math.cos(radians)
        return m

    def __mul__(self, other):
        m = TransformMatrix()
        for row in range(3):
            for col in range(3):
                m[row, col] = self.row(row).dot(other.column(col))
        return m

    def __imul__(self, other):
        m = self * other
        self._mat = m._mat
        return self

    def rotate(self, radians):
        self *= TransformMatrix.rotation(radians)
        return self

    def extract_transform(self):
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        tx = self.tx
        ty = self.ty

        dest_trans = {
            "translation": NVector(tx, ty),
            "angle": 0,
            "scale": NVector(1, 1),
            "skew_axis": 0,
            "skew_angle": 0,
        }

        delta = a * d - b * c
        if a != 0 or b != 0:
            r = math.hypot(a, b)
            dest_trans["angle"] = _sign(b) * math.acos(a/r)
            sx = r
            sy = delta / r
            dest_trans["skew_axis"] = 0
            sm = 1
        else:
            r = math.hypot(c, d)
            dest_trans["angle"] = math.pi / 2 - _sign(d) * math.acos(c / r)
            sx = delta / r
            sy = r
            dest_trans["skew_axis"] = math.pi / 2
            sm = -1

        dest_trans["scale"] = NVector(sx, sy)

        skew = sm * math.atan2(a * c + b * d, r * r)
        dest_trans["skew_angle"] = skew

        return dest_trans

