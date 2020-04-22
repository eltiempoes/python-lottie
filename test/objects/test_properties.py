from .. import base
from lottie import objects
from lottie.nvector import NVector


class TestMultiDimensional(base.TestCase):
    def test_zero(self):
        md = objects.MultiDimensional(NVector(0, 0))
        self.assertDictEqual(
            md.to_dict(),
            {
                "a": 0,
                "k": [0, 0]
            }
        )

    def test_value(self):
        md = objects.MultiDimensional(NVector(0, 0))
        md.value = NVector(1, 2)
        self.assertDictEqual(
            md.to_dict(),
            {
                "a": 0,
                "k": [1, 2]
            }
        )

    def test_keyframes(self):
        md = objects.MultiDimensional(NVector(0, 0))
        md.add_keyframe(0, NVector(1, 2))
        md.add_keyframe(3, NVector(4, 5))
        self.assertDictEqual(
            md.to_dict(),
            {
                "a": 1,
                "k": [
                    {
                        "t": 0,
                        "s": [1, 2],
                        "e": [4, 5],
                        "i": {"x": [1], "y": [1]},
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
        md = objects.MultiDimensional(NVector(0, 0))
        md.add_keyframe(0, NVector(1, 2))
        md.add_keyframe(3, NVector(4, 5))
        md.clear_animation(NVector(6, 7))
        self.assertDictEqual(
            md.to_dict(),
            {
                "a": 0,
                "k": [6, 7]
            }
        )

    def test_get_value_noanim(self):
        md = objects.MultiDimensional(NVector(0, 0))
        md.value = NVector(1, 2)
        self.assertEqual(md.get_value(),  NVector(1, 2))
        self.assertEqual(md.get_value(0), NVector(1, 2))
        self.assertEqual(md.get_value(3), NVector(1, 2))
        self.assertEqual(md.get_value(4), NVector(1, 2))

    def test_get_value_anim(self):
        md = objects.MultiDimensional(NVector(0, 0))
        md.add_keyframe(0, NVector(1, 2))
        md.add_keyframe(3, NVector(4, 5))
        self.assertEqual(md.get_value(),  NVector(1, 2))
        self.assertEqual(md.get_value(0), NVector(1, 2))
        self.assertEqual(md.get_value(3), NVector(4, 5))
        self.assertEqual(md.get_value(4), NVector(4, 5))

    def test_get_value_anim_nonestart(self):
        md = objects.MultiDimensional(NVector(0, 0))
        md.add_keyframe(0, NVector(1, 2))
        md.add_keyframe(3, NVector(4, 5))
        md.keyframes[-1].start = None # bodymovin exports them like this
        self.assertEqual(md.get_value(),  NVector(1, 2))
        self.assertEqual(md.get_value(0), NVector(1, 2))
        self.assertEqual(md.get_value(3), NVector(4, 5))
        self.assertEqual(md.get_value(4), NVector(4, 5))

    def test_get_value_inconsistent(self):
        md = objects.MultiDimensional(NVector(0, 0))
        md.value = NVector(1, 2)
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
        self.assertEqual(md.value, NVector(1, 2))

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
        self.assertEqual(md.keyframes[0].start, NVector(1, 2))
        self.assertEqual(md.keyframes[0].end, NVector(4, 5))
        self.assertEqual(md.keyframes[0].in_value.x, 6)
        self.assertEqual(md.keyframes[0].in_value.y, 7)
        self.assertEqual(md.keyframes[0].out_value.x, 8)
        self.assertEqual(md.keyframes[0].out_value.y, 9)

        self.assertEqual(md.keyframes[1].time, 3)
        self.assertEqual(md.keyframes[1].start, NVector(4, 5))
        self.assertEqual(md.keyframes[1].end, None)
        self.assertEqual(md.keyframes[1].in_value, None)
        self.assertEqual(md.keyframes[1].out_value, None)

    def test_load_anim_nolist(self):
        md = objects.MultiDimensional.load({
                "a": 1,
                "k": [
                    {
                        "t": 0,
                        "s": [1, 2],
                        "e": [4, 5],
                        "i": {"x": 6, "y": 7},
                        "o": {"x": 8, "y": 9},
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
        self.assertEqual(md.keyframes[0].start, NVector(1, 2))
        self.assertEqual(md.keyframes[0].end, NVector(4, 5))
        self.assertEqual(md.keyframes[0].in_value.x, 6)
        self.assertEqual(md.keyframes[0].in_value.y, 7)
        self.assertEqual(md.keyframes[0].out_value.x, 8)
        self.assertEqual(md.keyframes[0].out_value.y, 9)

        self.assertEqual(md.keyframes[1].time, 3)
        self.assertEqual(md.keyframes[1].start, NVector(4, 5))
        self.assertEqual(md.keyframes[1].end, None)
        self.assertEqual(md.keyframes[1].in_value, None)
        self.assertEqual(md.keyframes[1].out_value, None)
