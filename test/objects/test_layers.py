from .. import base
from tgs import objects
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
