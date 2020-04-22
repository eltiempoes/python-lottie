import unittest
from xml.etree import ElementTree
from .. import base
from lottie import objects
from lottie.parsers.svg import parse_svg_etree
from lottie.nvector import NVector


class PathTester(unittest.TestCase):
    def make_svg_paths(self, paths):
        svg = ElementTree.Element("svg")
        svg.attrib["viewBox"] = "0 0 512 512"
        for n, d in paths.items():
            path = ElementTree.SubElement(svg, "path")
            path.attrib["id"] = n
            path.attrib["stroke"] = "red"
            path.attrib["fill"] = "none"
            path.attrib["d"] = d
        return ElementTree.ElementTree(svg)

    def parse_svg_paths(self, paths):
        return parse_svg_etree(self.make_svg_paths(paths))

    def parse_svg_path(self, d):
        return self.parse_svg_paths({"path": d})

    def assert_path(self, path, vertices, in_tangents, out_tangents):
        anim = self.parse_svg_path(path)
        path = anim.find("path")
        self.assertIsInstance(path.shapes[0], objects.Path)
        self.assertIsInstance(path.shapes[1], objects.Stroke)
        bezier = path.shapes[0].shape.value
        self.assertListEqual(bezier.vertices, vertices)
        self.assertListEqual(bezier.in_tangents, in_tangents)
        self.assertListEqual(bezier.out_tangents, out_tangents)

    def assert_list_almost_equal(self, a, b):
        self.assertEqual(len(a), len(b))
        for aa, bb in zip(a, b):
            if isinstance(aa, list):
                self.assert_list_almost_equal(aa, bb)
            elif isinstance(aa, NVector):
                self.assert_list_almost_equal(aa.components, bb.components)
            else:
                self.assertAlmostEqual(aa, bb)


class TestMove(PathTester):
    def test_abs(self):
        self.assert_path(
            "M 20,20 M 10,10 h 10",
            [NVector(10, 10), NVector(20, 10)],
            [NVector( 0,  0), NVector( 0,  0)],
            [NVector( 0,  0), NVector( 0,  0)],
        )

    def test_rel(self):
        self.assert_path(
            "M 20,20 m 10,10 h 10",
            [NVector(30, 30), NVector(40, 30)],
            [NVector( 0,  0), NVector( 0,  0)],
            [NVector( 0,  0), NVector( 0,  0)],
        )

    def test_breaks_abs(self):
        anim = self.parse_svg_path("""
            M 10, 10 L 10, 20, 20, 20
            M 20, 10 L 10, 20 20, 20
        """)
        path = anim.find("path")
        bezier = path.shapes[0].shape.value
        self.assertListEqual(bezier.vertices, [
            NVector(10, 10), NVector(10, 20), NVector(20, 20),
        ])
        self.assertFalse(bezier.closed)

        bezier = path.shapes[1].shape.value
        self.assertListEqual(bezier.vertices, [
            NVector(20, 10), NVector(10, 20), NVector(20, 20),
        ])
        self.assertFalse(bezier.closed)

    def test_breaks_rel(self):
        anim = self.parse_svg_path("""
            M 10, 10 L 10, 20, 20, 20
            m 0,-10 L 10, 20 20, 20
        """)
        path = anim.find("path")
        bezier = path.shapes[0].shape.value
        self.assertListEqual(bezier.vertices, [
            NVector(10, 10), NVector(10, 20), NVector(20, 20),
        ])
        self.assertFalse(bezier.closed)

        bezier = path.shapes[1].shape.value
        self.assertListEqual(bezier.vertices, [
            NVector(20, 10), NVector(10, 20), NVector(20, 20),
        ])
        self.assertFalse(bezier.closed)


class TestLineTo(PathTester):
    def test_line_abs(self):
        self.assert_path(
            "M 10,10 L 90,90 V 10 H 50",
            [NVector(10, 10), NVector(90, 90), NVector(90, 10), NVector(50, 10)],
            [NVector( 0,  0), NVector( 0,  0), NVector( 0,  0), NVector( 0,  0)],
            [NVector( 0,  0), NVector( 0,  0), NVector( 0,  0), NVector( 0,  0)],
        )

    def test_line_rel(self):
        self.assert_path(
            "M 10,10 l 80,80, v -80 h -40",
            [NVector(10, 10), NVector(90, 90), NVector(90, 10), NVector(50, 10)],
            [NVector( 0,  0), NVector( 0,  0), NVector( 0,  0), NVector( 0,  0)],
            [NVector( 0,  0), NVector( 0,  0), NVector( 0,  0), NVector( 0,  0)],
        )


class TestCubic(PathTester):
    def test_cubic_abs(self):
        self.assert_path(
            """
            M 10,90
            C 30,90 25,10 50,10
            S 70,90 90,90
            """,
            [NVector(10, 90), NVector( 50, 10), NVector( 90, 90)],
            [NVector( 0,  0), NVector(-25,  0), NVector(-20,  0)],
            [NVector(20,  0), NVector( 25,  0), NVector(  0,  0)],
        )

    def test_cubic_rel(self):
        self.assert_path(
            """
            M 10,90
            c 20,0 15,-80 40,-80
            s 20,80 40,80
            """,
            [NVector(10, 90), NVector( 50, 10), NVector( 90, 90)],
            [NVector( 0,  0), NVector(-25,  0), NVector(-20,  0)],
            [NVector(20,  0), NVector( 25,  0), NVector(  0,  0)],
        )


class TestQuadratic(PathTester):
    def test_q_abs(self):
        self.assert_path(
            """
            M 10,50
            Q 25,25 40,50
            """,
            [NVector(10, 50), NVector( 40, 50)],
            [NVector( 0,  0), NVector(-15,-25)],
            [NVector( 0,  0), NVector(  0,  0)],
        )

    def test_q_rel(self):
        self.assert_path(
            """
            M 10,50
            q 15,-25 30,0
            """,
            [NVector(10, 50), NVector( 40, 50)],
            [NVector( 0,  0), NVector(-15,-25)],
            [NVector( 0,  0), NVector(  0,  0)],
        )

    def test_t_abs(self):
        self.assert_path(
            """
            M 10,50
            Q 25,25 40,50
            T 70,50 100,50 130,50
            """,
            [NVector(10, 50), NVector( 40, 50), NVector( 70, 50), NVector(100, 50), NVector(130, 50)],
            [NVector( 0,  0), NVector(-15,-25), NVector(-15, 25), NVector(-15,-25), NVector(-15, 25)],
            [NVector( 0,  0), NVector(  0,  0), NVector(  0,  0), NVector(  0,  0), NVector(  0,  0)],
        )

    def test_t_rel(self):
        self.assert_path(
            """
            M 10,50
            q 15,-25 30,0
            t 30,0 30,0 30,0
            """,
            [NVector(10, 50), NVector( 40, 50), NVector( 70, 50), NVector(100, 50), NVector(130, 50)],
            [NVector( 0,  0), NVector(-15,-25), NVector(-15, 25), NVector(-15,-25), NVector(-15, 25)],
            [NVector( 0,  0), NVector(  0,  0), NVector(  0,  0), NVector(  0,  0), NVector(  0,  0)],
        )


class TestArc(PathTester):
    def test_large_nosweep(self):
        anim = self.parse_svg_path("""
            M 6,10
            A 6 4 10 1 0 14,10
        """)
        path = anim.find("path")
        self.assertIsInstance(path.shapes[0], objects.Path)
        self.assertIsInstance(path.shapes[1], objects.Stroke)
        bezier = path.shapes[0].shape.value
        self.assert_list_almost_equal(bezier.vertices, [
            NVector(6, 10), NVector(6.8626965, 15.758131), NVector(15.2322608, 15.9819042), NVector(14, 10),
        ])
        self.assert_list_almost_equal(bezier.in_tangents, [
            NVector(0, 0), NVector(-2.5323342, -1.6407878), NVector(-2.0590729, 1.5180295), NVector(2.5323342, 1.6407878),
        ])
        self.assert_list_almost_equal(bezier.out_tangents, [
            NVector(-2.0590729, 1.5180295), NVector(2.5323342, 1.6407878), NVector(2.0590729, -1.5180295), NVector(0, 0)
        ])

    def test_large_sweep(self):
        anim = self.parse_svg_path("""
            M 6,10
            A 6 4 10 1 1 14,10
        """)
        path = anim.find("path")
        self.assertIsInstance(path.shapes[0], objects.Path)
        self.assertIsInstance(path.shapes[1], objects.Stroke)
        bezier = path.shapes[0].shape.value
        self.assert_list_almost_equal(bezier.vertices, [
            NVector(6, 10), NVector(4.4903685, 4.24186895), NVector(12.7677392, 4.0180958), NVector(14, 10),
        ])
        self.assert_list_almost_equal(bezier.in_tangents, [
            NVector(0, 0), NVector(-1.8563359, 1.6407878), NVector(-2.6844953, -1.51802947), NVector(1.8563359, -1.6407878),
        ])
        self.assert_list_almost_equal(bezier.out_tangents, [
            NVector(-2.6844953, -1.5180295), NVector(1.8563359, -1.6407878), NVector(2.6844953, 1.5180295), NVector(0, 0)
        ])

    def test_small_nosweep(self):
        anim = self.parse_svg_path("""
            M 6,10
            A 6 4 10 0 0 14,10
        """)
        path = anim.find("path")
        self.assertIsInstance(path.shapes[0], objects.Path)
        self.assertIsInstance(path.shapes[1], objects.Stroke)
        bezier = path.shapes[0].shape.value
        self.assert_list_almost_equal(bezier.vertices, [
            NVector(6, 10), NVector(14, 10),
        ])
        self.assert_list_almost_equal(bezier.in_tangents, [
            NVector(0, 0), NVector(-1.9493793, 1.43715898),
        ])
        self.assert_list_almost_equal(bezier.out_tangents, [
            NVector(2.54148326, 1.43715898), NVector(0, 0)
        ])

    def test_small_sweep(self):
        anim = self.parse_svg_path("""
            M 6,10
            A 6 4 10 0 1 14,10
        """)
        path = anim.find("path")
        self.assertIsInstance(path.shapes[0], objects.Path)
        self.assertIsInstance(path.shapes[1], objects.Stroke)
        bezier = path.shapes[0].shape.value
        self.assert_list_almost_equal(bezier.vertices, [
            NVector(6, 10), NVector(14, 10),
        ])
        self.assert_list_almost_equal(bezier.in_tangents, [
            NVector(0, 0), NVector(-2.54148326, -1.43715898),
        ])
        self.assert_list_almost_equal(bezier.out_tangents, [
            NVector(1.9493793, -1.43715898), NVector(0, 0)
        ])


class TestClosePath(PathTester):
    def test_noclose(self):
        anim = self.parse_svg_path("""
            M 10, 10 L 10, 20, 20, 20
        """)
        path = anim.find("path")
        bezier = path.shapes[0].shape.value
        self.assertListEqual(bezier.vertices, [
            NVector(10, 10), NVector(10, 20), NVector(20, 20),
        ])
        self.assertFalse(bezier.closed)

    def test_single_upper(self):
        anim = self.parse_svg_path("""
            M 10, 10 L 10, 20, 20, 20 Z
        """)
        path = anim.find("path")
        bezier = path.shapes[0].shape.value
        self.assertListEqual(bezier.vertices, [
            NVector(10, 10), NVector(10, 20), NVector(20, 20),
        ])
        self.assertTrue(bezier.closed)

    def test_single_lower(self):
        anim = self.parse_svg_path("""
            M 10, 10 L 10, 20, 20, 20 z
        """)
        path = anim.find("path")
        bezier = path.shapes[0].shape.value
        self.assertListEqual(bezier.vertices, [
            NVector(10, 10), NVector(10, 20), NVector(20, 20),
        ])
        self.assertTrue(bezier.closed)

    def test_multi(self):
        anim = self.parse_svg_path("""
            M 10, 10 L 10, 20, 20, 20 Z
            L 20, 10  20, 20 Z
        """)
        path = anim.find("path")
        bezier = path.shapes[0].shape.value
        self.assertListEqual(bezier.vertices, [
            NVector(10, 10), NVector(10, 20), NVector(20, 20),
        ])
        self.assertTrue(bezier.closed)

        bezier = path.shapes[1].shape.value
        self.assertListEqual(bezier.vertices, [
            NVector(10, 10), NVector(20, 10), NVector(20, 20),
        ])
        self.assertTrue(bezier.closed)


class TestIntegration(PathTester):
    def test_zero_values(self):
        self.assert_path(
            "M 10,10 L 90,90 0,0",
            [NVector(10, 10), NVector(90, 90), NVector(0, 0)],
            [NVector( 0,  0), NVector( 0,  0), NVector(0, 0)],
            [NVector( 0,  0), NVector( 0,  0), NVector(0, 0)],
        )
