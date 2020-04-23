from unittest.mock import MagicMock
from .. import base
from lottie.parsers.svg.importer import SvgParser


class TestUnit(base.TestCase):
    def test_naked(self):
        parser = SvgParser()
        parser.dpi = 96

        self.assertEqual(parser._parse_unit(123), 123)
        self.assertEqual(parser._parse_unit(12.3), 12.3)
        self.assertEqual(parser._parse_unit("123"), 123)
        self.assertEqual(parser._parse_unit("12.3"), 12.3)

    def test_px(self):
        parser = SvgParser()
        parser.dpi = 96

        self.assertEqual(parser._parse_unit("123px"), 123)
        self.assertEqual(parser._parse_unit("12.3px"), 12.3)

    def test_in(self):
        parser = SvgParser()
        parser.dpi = 96

        self.assertEqual(parser._parse_unit("1in"), 96)
        self.assertEqual(parser._parse_unit("1.5in"), 96*1.5)

        parser.dpi = 100
        self.assertEqual(parser._parse_unit("1in"), 100)

    def test_pc(self):
        parser = SvgParser()
        parser.dpi = 96

        self.assertAlmostEqual(parser._parse_unit("1pc"), 96/6)
        self.assertAlmostEqual(parser._parse_unit("1.5pc"), 96*1.5/6)

        parser.dpi = 100
        self.assertAlmostEqual(parser._parse_unit("1pc"), 100/6)

    def test_pt(self):
        parser = SvgParser()
        parser.dpi = 96

        self.assertAlmostEqual(parser._parse_unit("1pt"), 96/72)
        self.assertAlmostEqual(parser._parse_unit("1.5pt"), 96*1.5/72)

        parser.dpi = 100
        self.assertAlmostEqual(parser._parse_unit("1pt"), 100/72)

    def test_cm(self):
        parser = SvgParser()
        parser.dpi = 96

        self.assertAlmostEqual(parser._parse_unit("1cm"), 96/2.54)
        self.assertAlmostEqual(parser._parse_unit("1.5cm"), 96*1.5/2.54)

        parser.dpi = 100
        self.assertAlmostEqual(parser._parse_unit("1cm"), 100/2.54)

    def test_mm(self):
        parser = SvgParser()
        parser.dpi = 96

        self.assertAlmostEqual(parser._parse_unit("1mm"), 96/25.4)
        self.assertAlmostEqual(parser._parse_unit("1.5mm"), 96*1.5/25.4)

        parser.dpi = 100
        self.assertAlmostEqual(parser._parse_unit("1mm"), 100/25.4)

    def test_Q(self):
        parser = SvgParser()
        parser.dpi = 96

        self.assertAlmostEqual(parser._parse_unit("1Q"), 96/25.4/4)
        self.assertAlmostEqual(parser._parse_unit("1.5Q"), 96*1.5/25.4/4)

        parser.dpi = 100
        self.assertAlmostEqual(parser._parse_unit("1Q"), 100/25.4/4)

    def test_vw(self):
        parser = SvgParser()
        parser.animation = MagicMock()
        parser.animation.width = 512
        parser.animation.height = 256

        self.assertAlmostEqual(parser._parse_unit("1vw"), 5.12)
        self.assertAlmostEqual(parser._parse_unit("1.5vw"), 5.12*1.5)

    def test_vh(self):
        parser = SvgParser()
        parser.animation = MagicMock()
        parser.animation.width = 512
        parser.animation.height = 256

        self.assertAlmostEqual(parser._parse_unit("1vh"), 2.56)
        self.assertAlmostEqual(parser._parse_unit("1.5vh"), 2.56*1.5)

    def test_vmax(self):
        parser = SvgParser()
        parser.animation = MagicMock()
        parser.animation.width = 512
        parser.animation.height = 256

        self.assertAlmostEqual(parser._parse_unit("1vmax"), 5.12)
        self.assertAlmostEqual(parser._parse_unit("1.5vmax"), 5.12*1.5)

    def test_vmin(self):
        parser = SvgParser()
        parser.animation = MagicMock()
        parser.animation.width = 512
        parser.animation.height = 256

        self.assertAlmostEqual(parser._parse_unit("1vmin"), 2.56)
        self.assertAlmostEqual(parser._parse_unit("1.5vmin"), 2.56*1.5)
