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


