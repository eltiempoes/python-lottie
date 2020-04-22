from .. import base
from lottie import objects


class TestTransform(base.TestCase):
    _plain_out = {
        "a": {"a": 0, "k": [0, 0]},
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

