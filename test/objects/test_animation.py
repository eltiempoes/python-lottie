from .. import base
from lottie import objects, NVector
from .test_helpers import TestTransform


class TestAnimation(base.TestCase):
    def test_default(self):
        an = objects.Animation()
        self.assertDictEqual(
            an.to_dict(),
            {
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
                        "ind": 2,
                        "ip": 0,
                        "op": 60,
                        "bm": 0,
                    },
                    {
                        "ty": 3,
                        "ks": TestTransform._plain_out,
                        "ao": 0,
                        "ddd": 0,
                        "st": 0,
                        "sr": 1,
                        "ind": 0,
                        "ip": 0,
                        "op": 60,
                        "bm": 0,
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
                        "bm": 0,
                        "ind": 42,
                        "ip": 10,
                        "op": 20,
                    },
                ],
                "assets": [],
            }
        )

    def test_clone_same(self):
        an = objects.Animation()
        nl = objects.NullLayer()
        nl.in_point = 10
        nl.out_point = 20
        an.add_layer(nl)
        an2 = an.clone()

        self.assertDictEqual(
            an2.to_dict(),
            {
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
                        "bm": 0,
                        "ind": 0,
                        "ip": 10,
                        "op": 20,
                    },
                ],
                "assets": [],
            }
        )

    def test_clone_noalias(self):
        an = objects.Animation()
        nl = objects.NullLayer()
        nl.in_point = 10
        nl.out_point = 20
        an.add_layer(nl)
        an2 = an.clone()

        nl.in_point = 14
        nl.out_point = 24
        an.width = 100
        an.height = 200
        an.add_layer(objects.NullLayer())

        self.assertDictEqual(
            an2.to_dict(),
            {
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
                        "bm": 0,
                        "ind": 0,
                        "ip": 10,
                        "op": 20,
                    },
                ],
                "assets": [],
            }
        )

        self.assertNotEqual(an2.to_dict(), an.to_dict())

    def test_sanitize_noanim(self):
        an = objects.Animation()
        an.add_layer(objects.NullLayer())
        an.width = 128
        an.height = 256
        an.frame_rate = 69
        an.tgs_sanitize()
        self.assertEqual(
            an.to_dict(),
            {
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
                        "ks": {
                            "a": {"a": 0, "k": [0, 0]},
                            "p": {"a": 0, "k": [0, 0]},
                            "s": {"a": 0, "k": [200, 200]},
                            "r": {"a": 0, "k": 0},
                            "o": {"a": 0, "k": 100},
                            "sk": {"a": 0, "k": 0},
                            "sa": {"a": 0, "k": 0},
                        },
                        "ao": 0,
                        "ddd": 0,
                        "st": 0,
                        "sr": 1,
                        "bm": 0,
                        "ind": 0,
                        "ip": 0,
                        "op": 60,
                    },
                ],
                "assets": [],
            }
        )

    def test_sanitize_noop(self):
        an = objects.Animation()
        an.add_layer(objects.NullLayer())
        an.tgs_sanitize()
        self.assertEqual(
            an.to_dict(),
            {
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
                        "ks": {
                            "a": {"a": 0, "k": [0, 0]},
                            "p": {"a": 0, "k": [0, 0]},
                            "s": {"a": 0, "k": [100, 100]},
                            "r": {"a": 0, "k": 0},
                            "o": {"a": 0, "k": 100},
                            "sk": {"a": 0, "k": 0},
                            "sa": {"a": 0, "k": 0},
                        },
                        "ao": 0,
                        "ddd": 0,
                        "st": 0,
                        "sr": 1,
                        "bm": 0,
                        "ind": 0,
                        "ip": 0,
                        "op": 60,
                    },
                ],
                "assets": [],
            }
        )

    def test_sanitize_anim(self):
        an = objects.Animation()
        nl = an.add_layer(objects.NullLayer())
        nl.transform.scale.add_keyframe(0, NVector(50, 50))
        nl.transform.scale.add_keyframe(60, NVector(200, 200))
        nl.transform.scale.keyframes[-1].start = None
        an.width = 128
        an.height = 256
        an.frame_rate = 69
        an.tgs_sanitize()
        self.assertEqual(
            an.to_dict(),
            {
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
                        "ks": {
                            "a": {"a": 0, "k": [0, 0]},
                            "p": {"a": 0, "k": [0, 0]},
                            "s": {"a": 1, "k": [
                                {
                                    "s": [100, 100],
                                    "e": [400, 400],
                                    "t": 0,
                                    "o": {"x": [0], "y": [0]},
                                    "i": {"x": [1], "y": [1]},
                                },
                                {
                                    "t": 60,
                                },
                            ]},
                            "r": {"a": 0, "k": 0},
                            "o": {"a": 0, "k": 100},
                            "sk": {"a": 0, "k": 0},
                            "sa": {"a": 0, "k": 0},
                        },
                        "ao": 0,
                        "ddd": 0,
                        "st": 0,
                        "sr": 1,
                        "bm": 0,
                        "ind": 0,
                        "ip": 0,
                        "op": 60,
                    },
                ],
                "assets": [],
            }
        )

    def test_sanitize_lowfr(self):
        an = objects.Animation()
        an.add_layer(objects.NullLayer())
        an.frame_rate = 23
        an.tgs_sanitize()
        self.assertEqual(
            an.to_dict(),
            {
                "ip": 0,
                "op": 60,
                "fr": 30,
                "w": 512,
                "h": 512,
                "ddd": 0,
                "v": objects.Animation._version,
                "layers": [
                    {
                        "ty": 3,
                        "ks": {
                            "a": {"a": 0, "k": [0, 0]},
                            "p": {"a": 0, "k": [0, 0]},
                            "s": {"a": 0, "k": [100, 100]},
                            "r": {"a": 0, "k": 0},
                            "o": {"a": 0, "k": 100},
                            "sk": {"a": 0, "k": 0},
                            "sa": {"a": 0, "k": 0},
                        },
                        "ao": 0,
                        "ddd": 0,
                        "st": 0,
                        "sr": 1,
                        "bm": 0,
                        "ind": 0,
                        "ip": 0,
                        "op": 60,
                    },
                ],
                "assets": [],
            }
        )

    def test_remove_layer(self):
        an = objects.Animation()
        l0 = objects.layers.NullLayer()
        l1 = objects.layers.NullLayer()
        l2 = objects.layers.NullLayer()
        l3 = objects.layers.NullLayer()

        an.add_layer(l0)
        an.add_layer(l1)
        an.add_layer(l2)
        an.add_layer(l3)

        l2.parent = l1

        self.assertIn(l0, an.layers)
        self.assertIn(l1, an.layers)
        self.assertIn(l2, an.layers)
        self.assertIn(l3, an.layers)

        an.remove_layer(l1)

        self.assertIn(l0, an.layers)
        self.assertNotIn(l1, an.layers)
        self.assertNotIn(l2, an.layers)
        self.assertIn(l3, an.layers)
