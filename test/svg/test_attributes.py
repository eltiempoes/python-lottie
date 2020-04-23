from xml.etree import ElementTree
from unittest.mock import MagicMock
from .. import base
from lottie.parsers.svg.importer import SvgParser, parse_color
from lottie import NVector


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


class TestColor(base.TestCase):
    def test_hex_long(self):
        self.assert_nvector_equal(
            parse_color("#abcdef"),
            NVector(0xab/0xff, 0xcd/0xff, 0xef/0xff, 1)
        )
        self.assert_nvector_equal(
            parse_color("#ABCDEF"),
            NVector(0xab/0xff, 0xcd/0xff, 0xef/0xff, 1)
        )

    def test_hex_short(self):
        self.assert_nvector_equal(
            parse_color("#abc"),
            NVector(0xa/0xf, 0xb/0xf, 0xc/0xf, 1)
        )
        self.assert_nvector_equal(
            parse_color("#abc"),
            NVector(0xa/0xf, 0xb/0xf, 0xc/0xf, 1)
        )

    def test_rgb(self):
        self.assert_nvector_equal(
            parse_color("rgb(12, 34, 56)"),
            NVector(12/0xff, 34/0xff, 56/0xff, 1)
        );
        self.assert_nvector_equal(
            parse_color("rgb(12%, 34%, 56%)"),
            NVector(0.12, 0.34, 0.56, 1)
        );

    def test_rgba(self):
        self.assert_nvector_equal(
            parse_color("rgba(12, 34, 56, 0.7)"),
            NVector(12/0xff, 34/0xff, 56/0xff, 0.7)
        );
        self.assert_nvector_equal(
            parse_color("rgba(12%, 34%, 56%, 0.7)"),
            NVector(0.12, 0.34, 0.56, 0.7)
        );

    def test_named(self):
        self.assert_nvector_equal(
            parse_color("transparent"),
            NVector(0, 0, 0, 0)
        );
        self.assert_nvector_equal(
            parse_color("red"),
            NVector(1, 0, 0, 1)
        );
        self.assert_nvector_equal(
            parse_color("lime"),
            NVector(0, 1, 0, 1)
        );
        self.assert_nvector_equal(
            parse_color("blue"),
            NVector(0, 0, 1, 1)
        );

    def test_hsl(self):
        self.assert_nvector_equal(
            parse_color("hsl(0, 100%, 50%)"),
            NVector(1, 0, 0, 1)
        );
        self.assert_nvector_equal(
            parse_color("hsl(60, 100%, 50%)"),
            NVector(1, 1, 0, 1)
        );
        self.assert_nvector_equal(
            parse_color("hsl(120, 100%, 50%)"),
            NVector(0, 1, 0, 1)
        );
        self.assert_nvector_equal(
            parse_color("hsl(180, 100%, 50%)"),
            NVector(0, 1, 1, 1)
        );
        self.assert_nvector_equal(
            parse_color("hsl(240, 100%, 50%)"),
            NVector(0, 0, 1, 1)
        );
        self.assert_nvector_equal(
            parse_color("hsl(300, 100%, 50%)"),
            NVector(1, 0, 1, 1)
        );
        self.assert_nvector_equal(
            parse_color("hsl(360, 100%, 50%)"),
            NVector(1, 0, 0, 1)
        );

        self.assert_nvector_equal(
            parse_color("hsl(120, 100%, 0%)"),
            NVector(0, 0, 0, 1)
        );
        self.assert_nvector_equal(
            parse_color("hsl(120, 100%, 100%)"),
            NVector(1, 1, 1, 1)
        );
        self.assert_nvector_equal(
            parse_color("hsl(120, 100%, 25%)"),
            NVector(0, 0.5, 0, 1)
        );
        self.assert_nvector_equal(
            parse_color("hsl(120, 75%, 75%)"),
            NVector(0.5625, 0.9375, 0.5625, 1)
        );

    def test_hsla(self):
        self.assert_nvector_equal(
            parse_color("hsla(0, 100%, 50%, 0.7)"),
            NVector(1, 0, 0, 0.7)
        );
        self.assert_nvector_equal(
            parse_color("hsla(60, 100%, 50%, 0.7)"),
            NVector(1, 1, 0, 0.7)
        );
        self.assert_nvector_equal(
            parse_color("hsla(120, 100%, 50%, 0.7)"),
            NVector(0, 1, 0, 0.7)
        );
        self.assert_nvector_equal(
            parse_color("hsla(180, 100%, 50%, 0.7)"),
            NVector(0, 1, 1, 0.7)
        );
        self.assert_nvector_equal(
            parse_color("hsla(240, 100%, 50%, 0.7)"),
            NVector(0, 0, 1, 0.7)
        );
        self.assert_nvector_equal(
            parse_color("hsla(300, 100%, 50%, 0.7)"),
            NVector(1, 0, 1, 0.7)
        );
        self.assert_nvector_equal(
            parse_color("hsla(360, 100%, 50%, 0.7)"),
            NVector(1, 0, 0, 0.7)
        );

        self.assert_nvector_equal(
            parse_color("hsla(120, 100%, 0%, 0.7)"),
            NVector(0, 0, 0, 0.7)
        );
        self.assert_nvector_equal(
            parse_color("hsla(120, 100%, 100%, 0.7)"),
            NVector(1, 1, 1, 0.7)
        );
        self.assert_nvector_equal(
            parse_color("hsla(120, 100%, 25%, 0.7)"),
            NVector(0, 0.5, 0, 0.7)
        );
        self.assert_nvector_equal(
            parse_color("hsla(120, 75%, 75%, 0.7)"),
            NVector(0.5625, 0.9375, 0.5625, 0.7)
        );

    def test_current(self):
        self.assert_nvector_equal(
            parse_color("currentColor", NVector(0.1, 0.2, 0.3, 0.4)),
            NVector(0.1, 0.2, 0.3, 0.4)
        );
        self.assert_nvector_equal(
            parse_color("inherit", NVector(0.1, 0.2, 0.3, 0.4)),
            NVector(0.1, 0.2, 0.3, 0.4)
        );


class TestStyle(base.TestCase):
    def test_style(self):
        parser = SvgParser()
        et = ElementTree.Element("g")
        et.attrib["style"] = "fill: red; stroke:green;stroke-width:3px"
        self.assertDictEqual(
            parser.parse_style(et, {}),
            {
                "fill": "red",
                "stroke": "green",
                "stroke-width": "3px",
            }
        )

    def test_attrs(self):
        parser = SvgParser()
        et = ElementTree.Element("g")
        et.attrib["fill"] = "red"
        et.attrib["stroke"] = "green"
        et.attrib["stroke-width"] = "3px"
        self.assertDictEqual(
            parser.parse_style(et, {}),
            {
                "fill": "red",
                "stroke": "green",
                "stroke-width": "3px",
            }
        )

    def test_mixed(self):
        parser = SvgParser()
        et = ElementTree.Element("g")
        et.attrib["style"] = "stroke:green;stroke-width:3px"
        et.attrib["fill"] = "red"
        self.assertDictEqual(
            parser.parse_style(et, {}),
            {
                "fill": "red",
                "stroke": "green",
                "stroke-width": "3px",
            }
        )

    def test_inherit(self):
        parser = SvgParser()
        et = ElementTree.Element("g")
        et.attrib["style"] = "stroke:green;stroke-width:3px"
        base = { "fill": "red" }
        self.assertDictEqual(
            parser.parse_style(et, base),
            {
                "fill": "red",
                "stroke": "green",
                "stroke-width": "3px",
            }
        )
        self.assertDictEqual(base, { "fill": "red" })

    def test_apply_common_style(self):
        parser = SvgParser()
        transform = MagicMock()
        parser.apply_common_style({"fill": "red"}, transform)
        self.assertEqual(transform.opacity.value, 100)
        parser.apply_common_style({"fill": "red", "opacity": "0.7"}, transform)
        self.assertEqual(transform.opacity.value, 70)


    def test_apply_visibility(self):
        parser = SvgParser()
        object = MagicMock()
        object.hidden = False
        parser.apply_visibility({"fill": "red"}, object)
        self.assertFalse(object.hidden)
        parser.apply_visibility({"fill": "red", "display": "block"}, object)
        self.assertFalse(object.hidden)
        parser.apply_visibility({"fill": "red", "display": "inline"}, object)
        self.assertFalse(object.hidden)
        parser.apply_visibility({"fill": "red", "visibility": "visible"}, object)
        self.assertFalse(object.hidden)
        parser.apply_visibility({"fill": "red", "display": "none"}, object)
        self.assertTrue(object.hidden)
        parser.apply_visibility({"fill": "red", "visibility": "hidden"}, object)
        self.assertTrue(object.hidden)
