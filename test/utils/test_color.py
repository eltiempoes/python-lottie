from .. import base
from lottie import NVector
from lottie.utils.color import ColorMode, Color


class ConvertTestCase(base.TestCase):
    color_mode = ColorMode.RGB

    def color(self, *a):
        return Color(*a, mode=self.color_mode)

    def _veq(self, v1, v2, msg):
        if len(v1) != len(v2):
            return False

        for a, b in zip(v1, v2):
            self.assertAlmostEqual(a, b, 5, msg)

    def assert_convert(self, comps, expect, mode, expect_rt=None):
        color = self.color(*comps)
        conv = color.converted(mode)
        self.assertEqual(
            conv.mode, mode,
            "%s -> %s has the wrong color space: %s" % (
                self.color_mode, mode, conv.mode
            )
        )
        self._veq(
            conv, NVector(*expect),
            "%s -> %s has the wrong result: %s (expected %s)" % (
                self.color_mode, mode, conv, expect
            )
        )

        conv.convert(self.color_mode)
        self.assertEqual(conv.mode, self.color_mode)
        if expect_rt is None:
            expect_rt = color

        self._veq(
            conv, expect_rt,
            "%s -> %s round trip failed: %s (expected %s)" % (
                self.color_mode, mode, conv, expect_rt
            )
        )


class TestRGB(ConvertTestCase):
    color_mode = ColorMode.RGB

    def test_to_rgb(self):
        mode = ColorMode.RGB
        self.assert_convert((1, 0.5, 0.2), (1, 0.5, 0.2), mode)

    def test_to_hsv(self):
        mode = ColorMode.HSV
        self.assert_convert((1, 0, 0), (0, 1, 1), mode)
        self.assert_convert((0, 1, 0), (1/3, 1, 1), mode)
        self.assert_convert((0, 0, 1), (2/3, 1, 1), mode)
        self.assert_convert((1, 1, 1), (0, 0, 1), mode)
        self.assert_convert((0, 0, 0), (0, 0, 0), mode)

    def test_to_hsl(self):
        mode = ColorMode.HSL
        self.assert_convert((1, 0, 0), (0, 1, .5), mode)
        self.assert_convert((0, 1, 0), (1/3, 1, .5), mode)
        self.assert_convert((0, 0, 1), (2/3, 1, .5), mode)
        self.assert_convert((1, 1, 1), (0, 0, 1), mode)
        self.assert_convert((0, 0, 0), (0, 0, 0), mode)

    # values from the conversions functions themselves,
    # valided from http://www.colormine.org/convert/rgb-to-xyz
    def test_to_xyz(self):
        mode = ColorMode.XYZ
        self.assert_convert((1, 0, 0), (0.4124564, 0.2126729, 0.0193339), mode)
        self.assert_convert((0, 1, 0), (0.3575761, 0.7151522, 0.119192), mode)
        self.assert_convert((0, 0, 1), (0.1804375, 0.072175, 0.9503041), mode)
        self.assert_convert((1, 1, 1), (0.95047, 1.0000001, 1.08883), mode)
        self.assert_convert((0, 0, 0), (0, 0, 0), mode)

    # luv, lch


class TestHSV(ConvertTestCase):
    color_mode = ColorMode.HSV

    def test_to_rgb(self):
        mode = ColorMode.RGB
        self.assert_convert((1/3, 1, 1), (0, 1, 0), mode)
        self.assert_convert((  0, 1, 1), (1, 0, 0), mode)
        self.assert_convert((  0, 0, 0), (0, 0, 0), mode)
        self.assert_convert((0.5, 0, 1), (1, 1, 1), mode, (0, 0, 1))
        self.assert_convert((0.5, 1, 1), (0, 1, 1), mode)
        self.assert_convert((0.5, 0, 0), (0, 0, 0), mode, (0, 0, 0))

    def test_to_hsv(self):
        mode = ColorMode.HSV
        self.assert_convert((1/3, 1, 1), (1/3, 1, 1), mode)
        self.assert_convert((0, 1, 1), (0, 1, 1), mode)
        self.assert_convert((0, 0, 0), (0, 0, 0), mode)
        self.assert_convert((0.5, 1, 1), (0.5, 1, 1), mode)
        self.assert_convert((0.5, 0, 0), (0.5, 0, 0), mode)

    def test_to_hsl(self):
        mode = ColorMode.HSL
        self.assert_convert((1/3, 1, 1), (1/3, 1.0, 0.5), mode)
        self.assert_convert((0, 1, 1), (0, 1.0, 0.5), mode)
        self.assert_convert((0, 0, 0), (0, 0, 0.0), mode)
        self.assert_convert((0.5, 1, 1), (0.5, 1.0, 0.5), mode)
        self.assert_convert((0.5, 0, 0), (0.5, 0, 0.0), mode)

    # xyz, luv, lch


class TestHSL(ConvertTestCase):
    color_mode = ColorMode.HSL

    def test_to_rgb(self):
        mode = ColorMode.RGB
        self.assert_convert((1/3, 1, 0.5), (0.0, 1.0, 0.0), mode)
        self.assert_convert((0, 1, 0.5), (1.0, 0.0, 0.0), mode)
        self.assert_convert((0, 1, 1), (1, 1.0, 1.0), mode, (0, 0, 1))
        self.assert_convert((0, 0, 0), (0, 0, 0), mode)
        self.assert_convert((0.5, 1, 1), (1.0, 1.0, 1), mode, (0, 0, 1))
        self.assert_convert((0.5, 0, 1), (1, 1, 1), mode, (0, 0, 1))
        self.assert_convert((0.5, 0, 0), (0, 0, 0), mode, (0, 0, 0))

    def test_to_hsv(self):
        mode = ColorMode.HSV
        self.assert_convert((1/3, 1, 0.5), (1/3, 1.0, 1.0), mode)
        self.assert_convert((0, 1, 0.5), (0, 1, 1), mode)
        self.assert_convert((0, 1, 1), (0, 0, 1), mode, (0, 0, 1))
        self.assert_convert((0, 0, 0), (0, 0, 0), mode)
        self.assert_convert((0.5, 1, 1), (0.5, 0, 1), mode, (0.5, 0, 1))
        self.assert_convert((0.5, 0, 1), (0.5, 0, 1), mode)
        self.assert_convert((0.5, 0, 0), (0.5, 0, 0), mode)

    def test_to_hsl(self):
        mode = ColorMode.HSL
        self.assert_convert((1/3, 1, 0.5), (1/3, 1, 0.5), mode)
        self.assert_convert((0, 1, 0.5), (0, 1, 0.5), mode)
        self.assert_convert((0, 1, 1), (0, 1, 1), mode)
        self.assert_convert((0, 0, 0), (0, 0, 0), mode)
        self.assert_convert((0.5, 1, 1), (0.5, 1, 1), mode)
        self.assert_convert((0.5, 0, 1), (0.5, 0, 1), mode)
        self.assert_convert((0.5, 0, 0), (0.5, 0, 0), mode)

    # xyz, luv, lch


class TestXYZ(ConvertTestCase):
    color_mode = ColorMode.XYZ
    # hsv hsl lch

    def test_to_rgb(self):
        mode = ColorMode.RGB
        self.assert_convert((0.95047, 1, 1.08883), (1, 1, 1), mode)
        self.assert_convert((0, 0, 0), (0, 0, 0), mode)
        self.assert_convert((0.4124564, 0.2126729, 0.0193339), (1, 0, 0), mode)
        self.assert_convert((0.2687201, 0.1176957, 0.9544423), (0.5, 0, 1), mode)

    def test_to_xyz(self):
        mode = ColorMode.XYZ
        self.assert_convert((0.95047, 1, 1.08883), (0.95047, 1, 1.08883), mode)
        self.assert_convert((0, 0, 0), (0, 0, 0), mode)
        self.assert_convert((0.4124564, 0.2126729, 0.0193339), (0.4124564, 0.2126729, 0.0193339), mode)
        self.assert_convert((0.2687201, 0.1176957, 0.9544423), (0.2687201, 0.1176957, 0.9544423), mode)
