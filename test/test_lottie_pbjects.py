import unittest
from . import base
from tgs import objects


class TestAnimation(base.TestCase):
    def test_default(self):
        an = objects.Animation()
        self.assertDictEqual(
            an.to_dict(),
            {
                "tgs": 1,
                "ip": 0,
                "op": 60,
                "fr": 60,
                "w": 512,
                "h": 512,
                "ddd": 0,
                "v": objects.Animation._version,
                "layers": [],
                "assets": [],
            }
        )

    def test_name(self):
        an = objects.Animation()
        an.name = "Foobar"
        self.assertDictEqual(
            an.to_dict(),
            {
                "tgs": 1,
                "ip": 0,
                "op": 60,
                "fr": 60,
                "w": 512,
                "h": 512,
                "ddd": 0,
                "v": objects.Animation._version,
                "layers": [],
                "assets": [],
                "nm": "Foobar"
            }
        )

    def test_n_frames(self):
        an = objects.Animation(180)
        self.assertDictEqual(
            an.to_dict(),
            {
                "tgs": 1,
                "ip": 0,
                "op": 180,
                "fr": 60,
                "w": 512,
                "h": 512,
                "ddd": 0,
                "v": objects.Animation._version,
                "layers": [],
                "assets": [],
            }
        )

    def test_framerate(self):
        an = objects.Animation(60, 24)
        self.assertDictEqual(
            an.to_dict(),
            {
                "tgs": 1,
                "ip": 0,
                "op": 60,
                "fr": 24,
                "w": 512,
                "h": 512,
                "ddd": 0,
                "v": objects.Animation._version,
                "layers": [],
                "assets": [],
            }
        )

    def test_layers(self):
        an = objects.Animation()
        an.add_layer(objects.NullLayer())
        an.add_layer(objects.ShapeLayer())
        an.insert_layer(0, objects.NullLayer())
        self.assertDictEqual(
            an.to_dict(),
            {
                "tgs": 1,
                "ip": 0,
                "op": 60,
                "fr": 60,
                "w": 512,
                "h": 512,
                "ddd": 0,
                "v": objects.Animation._version,
                "layers": [
                    {
                        "ty": 3,
                        "ks": TestTransform._plain_out,
                        "ao": 0,
                        "ddd": 0,
                        "st": 0,
                        "sr": 1,
                        "ef": [],
                        "ind": 2,
                        "ip": 0,
                        "op": 60,
                    },
                    {
                        "ty": 3,
                        "ks": TestTransform._plain_out,
                        "ao": 0,
                        "ddd": 0,
                        "st": 0,
                        "sr": 1,
                        "ef": [],
                        "ind": 0,
                        "ip": 0,
                        "op": 60,
                    },
                    {
                        "ty": 4,
                        "ks": TestTransform._plain_out,
                        "ao": 0,
                        "bm": 0,
                        "ddd": 0,
                        "st": 0,
                        "sr": 1,
                        "shapes": [],
                        "ind": 1,
                        "ip": 0,
                        "op": 60,
                    }
                ],
                "assets": [],
            }
        )


    def test_layers_preserve(self):
        an = objects.Animation()
        nl = objects.NullLayer()
        nl.index = 42
        nl.in_point = 10
        nl.out_point = 20
        an.add_layer(nl)
        self.assertDictEqual(
            an.to_dict(),
            {
                "tgs": 1,
                "ip": 0,
                "op": 60,
                "fr": 60,
                "w": 512,
                "h": 512,
                "ddd": 0,
                "v": objects.Animation._version,
                "layers": [
                    {
                        "ty": 3,
                        "ks": TestTransform._plain_out,
                        "ao": 0,
                        "ddd": 0,
                        "st": 0,
                        "sr": 1,
                        "ef": [],
                        "ind": 42,
                        "ip": 10,
                        "op": 20,
                    },
                ],
                "assets": [],
            }
        )


class TestTransform(base.TestCase):
    _plain_out = {
        "a": {"a": 0, "k": [0, 0, 0]},
        "p": {"a": 0, "k": [0, 0]},
        "s": {"a": 0, "k": [100, 100]},
        "r": {"a": 0, "k": 0},
        "o": {"a": 0, "k": 100},
        "sk": {"a": 0, "k": 0},
        "sa": {"a": 0, "k": 0},
    }
    def test_plain(self):
        tr = objects.Transform()
        self.assertDictEqual(
            tr.to_dict(),
            self._plain_out
        )


class TestNullLayer(base.TestCase):
    def test_empty(self):
        lay = objects.NullLayer()
        self.assertDictEqual(
            lay.to_dict(),
            {
                "ty": 3,
                "ks": TestTransform._plain_out,
                "ao": 0,
                "ddd": 0,
                "st": 0,
                "sr": 1,
                "ef": [],
            }
        )


class TestShapeLayer(base.TestCase):
    def test_empty(self):
        lay = objects.ShapeLayer()
        self.assertDictEqual(
            lay.to_dict(),
            {
                "ty": 4,
                "ks": TestTransform._plain_out,
                "ao": 0,
                "bm": 0,
                "ddd": 0,
                "st": 0,
                "sr": 1,
                "shapes": [],
            }
        )


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


class TestMultiDimensional(base.TestCase):
    def test_zero(self):
        md = objects.MultiDimensional([0, 0])
        self.assertDictEqual(
            md.to_dict(),
            {
                "a": 0,
                "k": [0, 0]
            }
        )

    def test_value(self):
        md = objects.MultiDimensional([0, 0])
        md.value = [1, 2]
        self.assertDictEqual(
            md.to_dict(),
            {
                "a": 0,
                "k": [1, 2]
            }
        )

    def test_keyframes(self):
        md = objects.MultiDimensional([0, 0])
        md.add_keyframe(0, [1, 2])
        md.add_keyframe(3, [4, 5])
        self.assertDictEqual(
            md.to_dict(),
            {
                "a": 1,
                "k": [
                    {
                        "t": 0,
                        "s": [1, 2],
                        "e": [4, 5],
                        "i": {"x": [0], "y": [0]},
                        "o": {"x": [0], "y": [0]},
                    },
                    {
                        "t": 3,
                        "s": [4, 5],
                    }
                ]
            }
        )

    def test_clear(self):
        md = objects.MultiDimensional([0, 0])
        md.add_keyframe(0, [1, 2])
        md.add_keyframe(3, [4, 5])
        md.clear_animation([6, 7])
        self.assertDictEqual(
            md.to_dict(),
            {
                "a": 0,
                "k": [6, 7]
            }
        )

    def test_get_value_noanim(self):
        md = objects.MultiDimensional([0, 0])
        md.value = [1, 2]
        self.assertEqual(md.get_value(), [1, 2])
        self.assertEqual(md.get_value(0), [1, 2])
        self.assertEqual(md.get_value(3), [1, 2])
        self.assertEqual(md.get_value(4), [1, 2])

    def test_get_value_anim(self):
        md = objects.MultiDimensional([0, 0])
        md.add_keyframe(0, [1, 2])
        md.add_keyframe(3, [4, 5])
        self.assertEqual(md.get_value(), [1, 2])
        self.assertEqual(md.get_value(0), [1, 2])
        self.assertEqual(md.get_value(3), [4, 5])
        self.assertEqual(md.get_value(4), [4, 5])

    def test_get_value_anim_nonestart(self):
        md = objects.MultiDimensional([0, 0])
        md.add_keyframe(0, [1, 2])
        md.add_keyframe(3, [4, 5])
        md.keyframes[-1].start = None # bodymovin exports them like this
        self.assertEqual(md.get_value(), [1, 2])
        self.assertEqual(md.get_value(0), [1, 2])
        self.assertEqual(md.get_value(3), [4, 5])
        self.assertEqual(md.get_value(4), [4, 5])

    def test_get_value_inconsistent(self):
        md = objects.MultiDimensional([0, 0])
        md.value = [1, 2]
        md.animated = True
        self.assertEqual(md.get_value(),  None)
        self.assertEqual(md.get_value(0), None)
        self.assertEqual(md.get_value(3), None)
        self.assertEqual(md.get_value(4), None)

    def test_load_noanim(self):
        md = objects.MultiDimensional.load({
            "a": 0,
            "k": [1, 2],
        })
        self.assertIs(md.animated, False)
        self.assertIsNone(md.keyframes)
        self.assertEqual(md.value, [1, 2])

    def test_load_anim(self):
        md = objects.MultiDimensional.load({
                "a": 1,
                "k": [
                    {
                        "t": 0,
                        "s": [1, 2],
                        "e": [4, 5],
                        "i": {"x": [6], "y": [7]},
                        "o": {"x": [8], "y": [9]},
                    },
                    {
                        "t": 3,
                        "s": [4, 5],
                    }
                ]
        })
        self.assertIs(md.animated, True)
        self.assertIsNone(md.value)
        self.assertEqual(len(md.keyframes), 2)

        self.assertEqual(md.keyframes[0].time, 0)
        self.assertEqual(md.keyframes[0].start, [1, 2])
        self.assertEqual(md.keyframes[0].end, [4, 5])
        self.assertEqual(md.keyframes[0].in_value.x, 6)
        self.assertEqual(md.keyframes[0].in_value.y, 7)
        self.assertEqual(md.keyframes[0].out_value.x, 8)
        self.assertEqual(md.keyframes[0].out_value.y, 9)

        self.assertEqual(md.keyframes[1].time, 3)
        self.assertEqual(md.keyframes[1].start, [4, 5])
        self.assertEqual(md.keyframes[1].end, None)
        self.assertEqual(md.keyframes[1].in_value, None)
        self.assertEqual(md.keyframes[1].out_value, None)



