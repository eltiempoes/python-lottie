import math
from .. import base
from lottie.utils.transform import TransformMatrix, NVector


class TestTransform(base.TestCase):
    def test_properties_get(self):
        m = TransformMatrix()
        m._mat = [
             0,  1,  2,  3,
             4,  5,  6,  7,
             8,  9, 10, 11,
            12, 13, 14, 15
        ]

        self.assertEqual(m.a, 0)
        self.assertEqual(m.b, 1)
        self.assertEqual(m.c, 4)
        self.assertEqual(m.d, 5)
        self.assertEqual(m.tx, 12)
        self.assertEqual(m.ty, 13)

    def test_properties_set(self):
        m = TransformMatrix()
        m.a = 1
        m.b = 2
        m.c = 3
        m.d = 4
        m.tx = 5
        m.ty = 6

        self.assertEqual(m._mat, list(map(float, [
            1, 2, 0, 0,
            3, 4, 0, 0,
            0, 0, 1, 0,
            5, 6, 0, 1,
        ])))

    def test_init(self):
        self.assertEqual(TransformMatrix()._mat, [
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1,
        ])

    def test_getitem(self):
        m = TransformMatrix()
        m._mat = [
             0,  1,  2,  3,
             4,  5,  6,  7,
             8,  9, 10, 11,
            12, 13, 14, 15
        ]

        self.assertEqual(m[0, 0], 0)
        self.assertEqual(m[0, 1], 1)
        self.assertEqual(m[0, 2], 2)
        self.assertEqual(m[0, 3], 3)
        self.assertEqual(m[1, 0], 4)
        self.assertEqual(m[1, 1], 5)
        self.assertEqual(m[1, 2], 6)
        self.assertEqual(m[1, 3], 7)
        self.assertEqual(m[2, 0], 8)
        self.assertEqual(m[2, 1], 9)
        self.assertEqual(m[2, 2], 10)
        self.assertEqual(m[2, 3], 11)
        self.assertEqual(m[3, 0], 12)
        self.assertEqual(m[3, 1], 13)
        self.assertEqual(m[3, 2], 14)
        self.assertEqual(m[3, 3], 15)

    def test_setitem(self):
        m = TransformMatrix()

        m[0, 0] = 0
        m[0, 1] = 1
        m[0, 2] = 2
        m[0, 3] = 3
        m[1, 0] = 4
        m[1, 1] = 5
        m[1, 2] = 6
        m[1, 3] = 7
        m[2, 0] = 8
        m[2, 1] = 9
        m[2, 2] = 10
        m[2, 3] = 11
        m[3, 0] = 12
        m[3, 1] = 13
        m[3, 2] = 14
        m[3, 3] = 15

        self.assertEqual(m._mat, [
             0,  1,  2,  3,
             4,  5,  6,  7,
             8,  9, 10, 11,
            12, 13, 14, 15
        ])

    def test_clone(self):
        m = TransformMatrix()
        m._mat = [
             0,  1,  2,  3,
             4,  5,  6,  7,
             8,  9, 10, 11,
            12, 13, 14, 15
        ]

        m1 = m.clone()
        self.assertEqual(m1._mat, m._mat)
        self.assertIsNot(m1._mat, m._mat)

    def test_scale(self):
        m = TransformMatrix()
        self.assertIs(m.scale(2), m)
        self.assertEqual(m._mat, [
            2, 0, 0, 0,
            0, 2, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1,
        ])
        self.assertIs(m.scale(3, 4), m)
        self.assertEqual(m._mat, [
            6, 0, 0, 0,
            0, 8, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1,
        ])

    def test_translate(self):
        m = TransformMatrix()
        self.assertIs(m.translate(2, 3), m)
        self.assertEqual(m._mat, [
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            2, 3, 0, 1,
        ])
        self.assertEqual(m.tx, 2)
        self.assertEqual(m.ty, 3)

    def asssert_matrix_almost_equal(self, m, comps):
        for i in range(9):
            self.assertAlmostEqual(m._mat[i], comps[i], msg="%s\n%s" % (m, comps))

    def test_skew(self):
        m = TransformMatrix()
        self.assertIs(m.skew(math.pi / 4, math.pi*(2-1/4)), m)
        self.asssert_matrix_almost_equal(m, [
            1,-1, 0, 0,
            1, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1,
        ])
        self.assertAlmostEqual(m.c, 1)
        self.assertAlmostEqual(m.b, -1)

    def test_row_col(self):
        m = TransformMatrix()
        m._mat = [
             0,  1,  2,  3,
             4,  5,  6,  7,
             8,  9, 10, 11,
            12, 13, 14, 15
        ]
        self.assertEqual(m.row(0), NVector(0, 1, 2, 3))
        self.assertEqual(m.row(1), NVector(4, 5, 6, 7))
        self.assertEqual(m.row(2), NVector(8, 9, 10, 11))
        self.assertEqual(m.row(3), NVector(12, 13, 14, 15))

        self.assertEqual(m.column(0), NVector(0, 4, 8, 12))
        self.assertEqual(m.column(1), NVector(1, 5, 9, 13))
        self.assertEqual(m.column(2), NVector(2, 6, 10, 14))
        self.assertEqual(m.column(3), NVector(3, 7, 11, 15))

    def test_to_identity(self):
        m = TransformMatrix()
        m._mat = [
             0,  1,  2,  3,
             4,  5,  6,  7,
             8,  9, 10, 11,
            12, 13, 14, 15
        ]
        m.to_identity()
        self.assertEqual(m._mat, [
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1,
        ])

    def test_apply(self):
        m = TransformMatrix()
        v = NVector(1, 2)
        self.assertEqual(m.apply(v), v)
        m.scale(2, 4)
        self.assertEqual(m.apply(v), NVector(2, 8))
        m.translate(-1, -3)
        self.assertEqual(m.apply(v), NVector(1, 5))
        m.rotate(-math.pi/2)
        self.assert_nvector_equal(m.apply(v), NVector(-5, 1))

    def test_rotation(self):
        m = TransformMatrix.rotation(math.pi/2)
        self.asssert_matrix_almost_equal(m, [
            0, -1, 0, 0,
            1, 0, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1,
        ])

    def test_mul(self):
        m1 = TransformMatrix()
        m1._mat = [
            2, 3, 4, 0,
            5, 6, 7, 0,
            8, 9, 10, 0,
            0, 0, 0, 1,
        ]
        m2 = TransformMatrix()
        m2._mat = [
            .1, .2, .3, 0,
            .4, .5, .6, 0,
            .7, .8, .9, 0,
             0,  0,  0, 1,
        ]
        self.asssert_matrix_almost_equal(m1 * m2, [
             4.2,  5.1,  6.0, 0,
             7.8,  9.6, 11.4, 0,
            11.4, 14.1, 16.8, 0,
               0,    0,    0, 1,
        ])

    def test_imul(self):
        m1 = TransformMatrix()
        m1._mat = [
            2, 3, 4, 0,
            5, 6, 7, 0,
            8, 9, 10, 0,
            0, 0, 0, 1,
        ]
        m2 = TransformMatrix()
        m2._mat = [
            .1, .2, .3, 0,
            .4, .5, .6, 0,
            .7, .8, .9, 0,
             0,  0,  0, 1,
        ]
        m1 *= m2
        self.asssert_matrix_almost_equal(m1, [
             4.2,  5.1,  6.0, 0,
             7.8,  9.6, 11.4, 0,
            11.4, 14.1, 16.8, 0,
               0,    0,    0, 1,
        ])

    def test_rotate(self):
        m = TransformMatrix()
        m.scale(2)
        m.rotate(math.pi / 3)
        self.asssert_matrix_almost_equal(m, [
             2 * math.cos(math.pi/3),  2 * -math.sin(math.pi/3),  0, 0,
             2 * math.sin(math.pi/3),  2 * math.cos(math.pi/3), 0, 0,
             0, 0, 1, 0,
             0, 0, 0, 1,
        ])

    def test_extract_transform_id(self):
        m = TransformMatrix()
        tr = m.extract_transform()
        self.assert_nvector_equal(tr["translation"], NVector(0, 0))
        self.assert_nvector_equal(tr["scale"], NVector(1, 1))
        self.assertAlmostEqual(tr["angle"], 0)
        self.assertAlmostEqual(tr["skew_axis"], 0)
        self.assertAlmostEqual(tr["skew_angle"], 0)

    def test_extract_transform_trans(self):
        m = TransformMatrix()
        m.translate(10, 23)
        tr = m.extract_transform()
        self.assert_nvector_equal(tr["translation"], NVector(10, 23))
        self.assert_nvector_equal(tr["scale"], NVector(1, 1))
        self.assertAlmostEqual(tr["angle"], 0)
        self.assertAlmostEqual(tr["skew_axis"], 0)
        self.assertAlmostEqual(tr["skew_angle"], 0)

    def test_extract_transform_scale(self):
        m = TransformMatrix()
        m.scale(2, 3)
        tr = m.extract_transform()
        self.assert_nvector_equal(tr["translation"], NVector(0, 0))
        self.assert_nvector_equal(tr["scale"], NVector(2, 3))
        self.assertAlmostEqual(tr["angle"], 0)
        self.assertAlmostEqual(tr["skew_axis"], 0)
        self.assertAlmostEqual(tr["skew_angle"], 0)

    def test_extract_transform_rotate(self):
        m = TransformMatrix()
        m.rotate(math.pi / 6)
        tr = m.extract_transform()
        self.assert_nvector_equal(tr["translation"], NVector(0, 0))
        self.assert_nvector_equal(tr["scale"], NVector(1, 1))
        self.assertAlmostEqual(tr["angle"], math.pi / 6)
        self.assertAlmostEqual(tr["skew_axis"], 0)
        self.assertAlmostEqual(tr["skew_angle"], 0)

    def test_extract_transform_skew_x(self):
        m = TransformMatrix()
        m.skew(math.pi/3, 0)
        tr = m.extract_transform()
        self.assert_nvector_equal(tr["translation"], NVector(0, 0))
        self.assert_nvector_equal(tr["scale"], NVector(1, 1))
        self.assertAlmostEqual(tr["angle"], 0)
        self.assertAlmostEqual(tr["skew_axis"], 0)
        self.assertAlmostEqual(tr["skew_angle"], math.pi/3)

    def test_extract_transform_complex(self):
        m = TransformMatrix()
        m.scale(2, 3)
        #m.skew(math.pi/3, 0)
        m.rotate(math.pi / 6)
        m.translate(10, 23)
        self.asssert_matrix_almost_equal(m, (
            TransformMatrix().scale(2, 3) *
            #TransformMatrix().skew(math.pi/3, 0) *
            TransformMatrix.rotation(math.pi/6) *
            TransformMatrix().translate(10, 23)
        )._mat)
        tr = m.extract_transform()
        self.assert_nvector_equal(tr["translation"], NVector(10, 23))
        self.assert_nvector_equal(tr["scale"], NVector(2, 3))
        self.assertAlmostEqual(tr["angle"], math.pi / 6)
        #self.assertAlmostEqual(tr["skew_axis"], 0)
        #self.assertAlmostEqual(tr["skew_angle"], math.pi/3)
