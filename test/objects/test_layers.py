from .. import base
from lottie import objects
from .test_helpers import TestTransform


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
                "bm": 0,
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
                "bm": 0,
            }
        )
