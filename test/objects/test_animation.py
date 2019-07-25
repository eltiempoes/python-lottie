from .. import base
from tgs import objects
from .test_helpers import TestTransform


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
                        "bm": 0,
                        "ind": 42,
                        "ip": 10,
                        "op": 20,
                    },
                ],
                "assets": [],
            }
        )
