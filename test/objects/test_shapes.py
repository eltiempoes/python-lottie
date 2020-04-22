from .. import base
from lottie import objects


class TestBoundingBox(base.TestCase):
    def test_null_ctor(self):
        bb = objects.BoundingBox()
        self.assertTrue(bb.isnull())

    def test_nonnull_ctor(self):
        bb = objects.BoundingBox(0, 0, 10, 10)
        self.assertFalse(bb.isnull())

    def test_null_include(self):
        bb = objects.BoundingBox()
        bb.include(10, 20)
        self.assertEqual(bb.x1, 10)
        self.assertEqual(bb.y1, 20)
        self.assertEqual(bb.x2, 10)
        self.assertEqual(bb.y2, 20)

    def test_nonnull_include_null(self):
        bb = objects.BoundingBox(0, 0, 30, 30)
        bb.include(None, None)
        self.assertEqual(bb.x1, 0)
        self.assertEqual(bb.y1, 0)
        self.assertEqual(bb.x2, 30)
        self.assertEqual(bb.y2, 30)

    def test_nonnull_include_inside(self):
        bb = objects.BoundingBox(0, 0, 30, 30)
        bb.include(10, 20)
        self.assertEqual(bb.x1, 0)
        self.assertEqual(bb.y1, 0)
        self.assertEqual(bb.x2, 30)
        self.assertEqual(bb.y2, 30)

    def test_nonnull_include_outside(self):
        bb = objects.BoundingBox(0, 0, 30, 30)
        bb.include(50, 40)
        self.assertEqual(bb.x1, 0)
        self.assertEqual(bb.y1, 0)
        self.assertEqual(bb.x2, 50)
        self.assertEqual(bb.y2, 40)

    def test_center(self):
        bb = objects.BoundingBox(0, 0, 30, 40)
        c = bb.center()
        self.assertEqual(c[0], 15)
        self.assertEqual(c[1], 20)

    def test_repr(self):
        x = repr(objects.BoundingBox(11, 22, 30, 40))
        self.assertIn("11", x)
        self.assertIn("22", x)
        self.assertIn("30", x)
        self.assertIn("40", x)

    def test_null_expand_nonnull(self):
        a = objects.BoundingBox()
        b = objects.BoundingBox(1, 2, 3, 4)
        a.expand(b)
        self.assertEqual(a.x1, 1)
        self.assertEqual(a.y1, 2)
        self.assertEqual(a.x2, 3)
        self.assertEqual(a.y2, 4)

    def test_null_expand_null(self):
        a = objects.BoundingBox()
        b = objects.BoundingBox()
        a.expand(b)
        self.assertEqual(a.x1, None)
        self.assertEqual(a.y1, None)
        self.assertEqual(a.x2, None)
        self.assertEqual(a.y2, None)

    def test_nonnull_expand_inside(self):
        a = objects.BoundingBox(0, 0, 4, 5)
        b = objects.BoundingBox(1, 2, 3, 4)
        a.expand(b)
        self.assertEqual(a.x1, 0)
        self.assertEqual(a.y1, 0)
        self.assertEqual(a.x2, 4)
        self.assertEqual(a.y2, 5)

    def test_nonnull_expand_outside(self):
        a = objects.BoundingBox(1, 2, 3, 4)
        b = objects.BoundingBox(0, 0, 4, 5)
        a.expand(b)
        self.assertEqual(a.x1, 0)
        self.assertEqual(a.y1, 0)
        self.assertEqual(a.x2, 4)
        self.assertEqual(a.y2, 5)


class TestRect(base.TestCase):
    def test_empty(self):
        sh = objects.Rect()
        self.assertDictEqual(
            sh.to_dict(),
            {
                "ty": "rc",
                "d": 0,
                "p": {"a": 0, "k": [0, 0]},
                "s": {"a": 0, "k": [0, 0]},
                "r": {"a": 0, "k": 0},
            }
        )

    def test_sized(self):
        sh = objects.Rect()
        sh.size.value = [10, 20]
        sh.position.value = [30, 40]
        sh.name = "foo"
        self.assertDictEqual(
            sh.to_dict(),
            {
                "ty": "rc",
                "d": 0,
                "p": {"a": 0, "k": [30, 40]},
                "s": {"a": 0, "k": [10, 20]},
                "r": {"a": 0, "k": 0},
                "nm": "foo",
            }
        )

    def test_boundingbox(self):
        sh = objects.Rect()
        sh.position.value = [30, 40]
        sh.size.value = [10, 20]

        bb = sh.bounding_box()
        c = bb.center()
        self.assertEqual(bb.x1, 30-5)
        self.assertEqual(bb.y1, 40-10)
        self.assertEqual(bb.x2, 30+5)
        self.assertEqual(bb.y2, 40+10)
        self.assertEqual(c[0], 30)
        self.assertEqual(c[1], 40)


class TestStar(base.TestCase):
    def test_empty(self):
        sh = objects.Star()
        self.assertDictEqual(
            sh.to_dict(),
            {
                "ty": "sr",
                "d": 0,
                "p": {"a": 0, "k": [0, 0]},
                "ir": {"a": 0, "k": 0},
                "is": {"a": 0, "k": 0},
                "or": {"a": 0, "k": 0},
                "os": {"a": 0, "k": 0},
                "r": {"a": 0, "k": 0},
                "pt": {"a": 0, "k": 5},
                "sy": 1,
            }
        )

    def test_sized(self):
        sh = objects.Star()
        sh.outer_radius.value = 20
        sh.position.value = [30, 40]
        sh.name = "foo"
        sh.star_type = objects.StarType.Polygon
        sh.points.value = 6
        self.assertDictEqual(
            sh.to_dict(),
            {
                "ty": "sr",
                "d": 0,
                "p": {"a": 0, "k": [30, 40]},
                "ir": {"a": 0, "k": 0},
                "is": {"a": 0, "k": 0},
                "or": {"a": 0, "k": 20},
                "os": {"a": 0, "k": 0},
                "r": {"a": 0, "k": 0},
                "pt": {"a": 0, "k": 6},
                "sy": 2,
                "nm": "foo",
            }
        )

    def test_boundingbox(self):
        sh = objects.Star()
        sh.outer_radius.value = 20
        sh.position.value = [30, 40]

        bb = sh.bounding_box()
        c = bb.center()
        self.assertEqual(bb.x1, 30-20)
        self.assertEqual(bb.y1, 40-20)
        self.assertEqual(bb.x2, 30+20)
        self.assertEqual(bb.y2, 40+20)
        self.assertEqual(c[0], 30)
        self.assertEqual(c[1], 40)


class TestEllipse(base.TestCase):
    def test_empty(self):
        sh = objects.Ellipse()
        self.assertDictEqual(
            sh.to_dict(),
            {
                "ty": "el",
                "d": 0,
                "p": {"a": 0, "k": [0, 0]},
                "s": {"a": 0, "k": [0, 0]},
            }
        )

    def test_sized(self):
        sh = objects.Ellipse()
        sh.size.value = [10, 20]
        sh.position.value = [30, 40]
        sh.name = "foo"
        self.assertDictEqual(
            sh.to_dict(),
            {
                "ty": "el",
                "d": 0,
                "p": {"a": 0, "k": [30, 40]},
                "s": {"a": 0, "k": [10, 20]},
                "nm": "foo",
            }
        )

    def test_boundingbox(self):
        sh = objects.Ellipse()
        sh.position.value = [30, 40]
        sh.size.value = [10, 20]

        bb = sh.bounding_box()
        c = bb.center()
        self.assertEqual(bb.x1, 30-5)
        self.assertEqual(bb.y1, 40-10)
        self.assertEqual(bb.x2, 30+5)
        self.assertEqual(bb.y2, 40+10)
        self.assertEqual(c[0], 30)
        self.assertEqual(c[1], 40)

