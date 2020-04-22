import os
import math

from lottie.parsers.sif import api, ast
from lottie.nvector import NVector, PolarVector
from .. import base


class TestParseFile(base.TestCase):
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "baseline.sif")

    def assert_strong_equal(self, a, b):
        ta = type(a)
        tb = type(b)
        if ta == tb or issubclass(tb, ta):
            if ta is float:
                self.assertAlmostEqual(a, b)
            elif ta is NVector:
                self.assertEqual(len(a), len(b))
                for ia, ib in zip(a, b):
                    self.assertAlmostEqual(ia, ib)
            else:
                self.assertEqual(a, b)
        else:
            self.fail("%s and %s have different types: %s, %s" % (a, b, ta, tb))

    def test_from_xml(self):
        canvas = api.Canvas.from_xml_file(self.file)
        self._check_file(canvas)

    def _check_file(self, canvas):
        self.canvas = canvas
        self._check_canvas(canvas)
        self._check_layer_polygon(canvas.layers[0])
        self._check_layer_zoom(canvas.layers[1])
        self._check_layer_group(canvas.layers[2])
        self._check_layer_circle_outline(canvas.layers[3])
        self._check_layer_region(canvas.layers[5])
        self._check_layer_gradient(canvas.layers[6])
        self._check_layer_text(canvas.layers[7])

    def _check_canvas(self, canvas):
        self.assertIsInstance(canvas, api.Canvas)
        self.assertEqual(len(canvas.layers), 8)
        self.assert_strong_equal(canvas.version, "1.2")
        self.assert_strong_equal(canvas.width, 512.)
        self.assert_strong_equal(canvas.height, 512.)
        self.assert_strong_equal(canvas.xres, 2834.645752)
        self.assert_strong_equal(canvas.yres, 2834.645752)
        self.assert_strong_equal(canvas.gamma_r, 2.2)
        self.assert_strong_equal(canvas.gamma_g, 2.2)
        self.assert_strong_equal(canvas.gamma_b, 2.2)
        self.assert_strong_equal(canvas.view_box, NVector(-4.266667, 4.266667, 4.266667, -4.266667))
        self.assert_strong_equal(canvas.antialias, True)
        self.assert_strong_equal(canvas.fps, 60.)
        self.assert_strong_equal(canvas.begin_time, api.FrameTime(0, api.FrameTime.Unit.Frame))
        self.assert_strong_equal(canvas.end_time, api.FrameTime(3., api.FrameTime.Unit.Seconds))
        self.assert_strong_equal(canvas.bgcolor, NVector(.5, .5, .5, 1.))
        self.assertEqual(len(canvas.keyframes), 1)
        kf = canvas.keyframes[0]
        self.assert_strong_equal(kf.time, api.FrameTime.frame(0))
        self.assert_strong_equal(kf.active, True)

    def _check_layer_polygon(self, layer):
        self.assertIsInstance(layer, api.PolygonLayer)
        self.assert_strong_equal(layer.type, "polygon")
        self.assert_strong_equal(layer.desc, "Polygon008")

        self.assert_strong_equal(layer.active, True)
        self.assert_strong_equal(layer.exclude_from_rendering, False)
        self.assert_strong_equal(layer.version, "0.1")

        self.assert_strong_equal(layer.z_depth.value, 0.)
        self.assert_strong_equal(layer.amount.value, 1.)
        self.assert_strong_equal(layer.blend_method, api.BlendMethod.Composite)
        self.assert_strong_equal(layer.origin.value, NVector(0., 0.))
        self.assert_strong_equal(layer.color.value, NVector(1., 1., 1., 1.))
        self.assert_strong_equal(layer.origin.value, NVector(0, 0))

        self.assert_strong_equal(layer.invert.value, False)
        self.assert_strong_equal(layer.antialias.value, True)
        self.assert_strong_equal(layer.feather.value, 0.)
        self.assert_strong_equal(layer.blurtype.value, api.BlurType.FastGaussian)
        self.assert_strong_equal(layer.winding_style.value, api.WindingStyle.NonZero)

        self.assertIsInstance(layer.points, list)
        self.assertEqual(len(layer.points), 5)
        self.assert_strong_equal(layer.points[0].value, NVector(-3.4468984604, 0.6007212400))
        self.assert_strong_equal(layer.points[4].value, NVector(-2.7399964333, -0.2140279114))

    def _check_layer_zoom(self, layer):
        self.assertIsInstance(layer, api.ScaleLayer)
        self.assert_strong_equal(layer.type, "zoom")
        self.assert_strong_equal(layer.amount.value, 0.4479692780)
        self.assert_strong_equal(layer.center.value, NVector(-2.9516866207, 0.7527821660))

    def _check_layer_group(self, layer):
        self.assertIsInstance(layer, api.GroupLayer)
        self.assert_strong_equal(layer.type, "group")
        self.assert_strong_equal(layer.desc, "Group")

        self.assert_strong_equal(layer.origin.value, NVector(0., 0.))
        self.assert_strong_equal(layer.time_dilation.value, 1.)
        self.assert_strong_equal(layer.time_offset.value, api.FrameTime(0, api.FrameTime.Unit.Seconds))
        self.assert_strong_equal(layer.children_lock, False)
        self.assert_strong_equal(layer.outline_grow.value, 0.)
        self.assert_strong_equal(layer.z_range, False)
        self.assert_strong_equal(layer.z_range_position.value, 0.)
        self.assert_strong_equal(layer.z_range_depth.value, 0.)
        self.assert_strong_equal(layer.z_range_blur.value, 0.)

        trans = layer.transformation
        self.assertIsInstance(trans, api.SifTransform)
        self.assert_strong_equal(trans.offset.value, NVector(0, 0))
        self.assert_strong_equal(trans.angle.value, -89.798615)
        self.assert_strong_equal(trans.skew_angle.value, 0.)
        self.assert_strong_equal(trans.scale.value, NVector(1, 1))

        canvas = layer.layers
        self.assertEqual(len(canvas), 3)
        self._check_layer_circle(canvas[0])
        self._check_layer_rectangle(canvas[1])
        self._check_layer_star(canvas[2])

    def _check_layer_circle(self, layer):
        self.assertIsInstance(layer, api.CircleLayer)
        self.assert_strong_equal(layer.type, "circle")
        self.assert_strong_equal(layer.radius.value, 0.5332824707)
        self.assert_strong_equal(layer.feather.value, 0.)
        self.assert_strong_equal(layer.origin.value, NVector(-2.7097899914, 2.6285450459))
        self.assert_strong_equal(layer.color.value, NVector(1., 0., 0., 1.))
        guid = "735D9D04C276A32CAE9D9F045DFF318B"
        self.assert_strong_equal(layer.origin.value, self.canvas.get_object(guid))
        self.assertIs(layer.origin.value, self.canvas.get_object(guid))

    def _check_layer_rectangle(self, layer):
        self.assertIsInstance(layer, api.RectangleLayer)
        self.assert_strong_equal(layer.type, "rectangle")
        self.assert_strong_equal(layer.color.value, NVector(1., 1., 1., 1.))
        self.assert_strong_equal(layer.point1.value, NVector(-1.4219197035, 2.7379217148))
        self.assert_strong_equal(layer.point2.value, NVector(-0.2791198790, 1.7953078747))
        self.assert_strong_equal(layer.expand.value, 0.)
        self.assert_strong_equal(layer.feather_x.value, 0.)
        self.assert_strong_equal(layer.feather_y.value, 0.)
        self.assert_strong_equal(layer.bevel.value, 0.1666666797)
        self.assert_strong_equal(layer.bevCircle.value, True)

    def _check_layer_star(self, layer):
        self.assertIsInstance(layer, api.StarLayer)
        self.assert_strong_equal(layer.type, "star")
        self.assert_strong_equal(layer.feather.value, 0.)
        self.assert_strong_equal(layer.radius1.value, 0.9195922852)
        self.assert_strong_equal(layer.radius2.value, 0.4597961426)
        self.assert_strong_equal(layer.angle.value, 90.)
        self.assert_strong_equal(layer.points.value, 5)
        self.assert_strong_equal(layer.regular_polygon.value, False)

    def _check_layer_circle_outline(self, layer):
        self.assertIsInstance(layer, api.OutlineLayer)
        self.assert_strong_equal(layer.type, "outline")
        self.assert_strong_equal(layer.desc, "Circle017 Outline")
        self.assert_strong_equal(layer.origin.value, NVector(-2.7097899914, 2.6285450459))
        self.assertIsInstance(layer.bline, api.Bline)
        self.assertEqual(len(layer.bline.points), 4)
        self.assert_strong_equal(layer.bline.loop, True)

        guid = "735D9D04C276A32CAE9D9F045DFF318B"
        self.assert_strong_equal(layer.origin.value, self.canvas.get_object(guid))
        self.assertIs(layer.origin.value, self.canvas.get_object(guid))

        point = layer.bline.points[0]
        self.assertIsInstance(point, api.BlinePoint)
        self.assert_strong_equal(point.point.value, NVector(0.5332824588, 0))
        self.assert_strong_equal(point.width.value, 1.)
        self.assert_strong_equal(point.origin.value, 0.5)
        self.assert_strong_equal(point.split.value, False)
        self.assert_strong_equal(point.split_radius.value, True)
        self.assert_strong_equal(point.split_angle.value, False)
        self.assert_strong_equal(point.t1.radius.value, 0.8835712761)
        self.assert_strong_equal(point.t1.theta.value, 90.)
        self.assert_strong_equal(point.t2.radius.value, 0.8835712761)
        self.assert_strong_equal(point.t2.theta.value, 90.)

    def _check_layer_region(self, layer):
        self.assertIsInstance(layer, api.RegionLayer)
        self.assert_strong_equal(layer.type, "region")
        self.assertIsInstance(layer.bline, api.Bline)
        self.assertEqual(len(layer.bline.points), 3)
        self.assert_strong_equal(layer.bline.loop, True)

        point = layer.bline.points[0]
        self.assertIsInstance(point, api.BlinePoint)
        self.assert_strong_equal(point.point.value, NVector(-0.7645721436, 0.4090138674))
        self.assert_strong_equal(point.width.value, 1.)
        self.assert_strong_equal(point.origin.value, 0.5)
        self.assert_strong_equal(point.split.value, False)
        self.assert_strong_equal(point.split_radius.value, False)
        self.assert_strong_equal(point.split_angle.value, False)
        self.assert_strong_equal(point.t1.radius.value, 1.7138580473)
        self.assert_strong_equal(point.t1.theta.value, 53.468349)
        self.assert_strong_equal(point.t2.radius.value, 1.7138580473)
        self.assert_strong_equal(point.t2.theta.value, 53.468349)

        point = layer.bline.points[1]
        self.assertIsInstance(point, api.BlinePoint)
        self.assert_strong_equal(point.point.value, NVector(0.7732625604, -0.0648742691))
        self.assertIsInstance(point.t1.radius, ast.SifAnimated)
        self.assertEqual(len(point.t1.radius.keyframes), 2)
        kf = point.t1.radius.keyframes[0]
        self.assertIsInstance(kf, api.SifKeyframe)
        self.assert_strong_equal(kf.time, api.FrameTime(0, api.FrameTime.Unit.Seconds))
        self.assert_strong_equal(kf.before, ast.Interpolation.Clamped)
        self.assert_strong_equal(kf.after, ast.Interpolation.Clamped)
        self.assert_strong_equal(kf.value, 2.2314351749)
        kf = point.t1.radius.keyframes[1]
        self.assertIsInstance(kf, api.SifKeyframe)
        self.assert_strong_equal(kf.time, api.FrameTime(2, api.FrameTime.Unit.Seconds))
        self.assert_strong_equal(kf.before, ast.Interpolation.Clamped)
        self.assert_strong_equal(kf.after, ast.Interpolation.Clamped)
        self.assert_strong_equal(kf.value, 2.6981012388)

        kf = point.t1.theta.keyframes[0]
        self.assertIsInstance(kf, api.SifKeyframe)
        self.assert_strong_equal(kf.time, api.FrameTime(0, api.FrameTime.Unit.Seconds))
        self.assert_strong_equal(kf.before, ast.Interpolation.Clamped)
        self.assert_strong_equal(kf.after, ast.Interpolation.Clamped)
        self.assert_strong_equal(kf.value, 19.593754)
        kf = point.t1.theta.keyframes[1]
        self.assertIsInstance(kf, api.SifKeyframe)
        self.assert_strong_equal(kf.time, api.FrameTime(2, api.FrameTime.Unit.Seconds))
        self.assert_strong_equal(kf.before, ast.Interpolation.Clamped)
        self.assert_strong_equal(kf.after, ast.Interpolation.Clamped)
        self.assert_strong_equal(kf.value, -57.534264)

    def _check_layer_gradient(self, layer):
        self.assert_strong_equal(layer.desc, "Gradient Group")
        gradient = layer.layers[0]
        self.assertIsInstance(gradient, api.RadialGradient)
        self.assertEqual(len(gradient.gradient.value), 2)
        self.assert_strong_equal(gradient.gradient.value[0].pos, 0.)
        self.assert_strong_equal(gradient.gradient.value[0].color, NVector(1, 1, 1, 1))
        self.assert_strong_equal(gradient.gradient.value[1].pos, 1.)
        self.assert_strong_equal(gradient.gradient.value[1].color, NVector(0, 0, 0, 1))
        self.assert_strong_equal(layer.layers[1].blend_method, api.BlendMethod.Alpha)

    def _check_layer_text(self, layer):
        self.assertIsInstance(layer, api.TextLayer)
        self.assert_strong_equal(layer.type, "text")
        self.assert_strong_equal(layer.desc, "Foobar")

        self.assert_strong_equal(layer.text.value, "Foobar")
        self.assert_strong_equal(layer.family.value, "Sans Serif")
        self.assert_strong_equal(layer.style.value, api.FontStyle.Normal)
        self.assert_strong_equal(layer.weight.value, 400)
        self.assert_strong_equal(layer.compress.value, 1.)
        self.assert_strong_equal(layer.size.value, NVector(1., 1.))
        self.assert_strong_equal(layer.orient.value, NVector(.5, .5))
        self.assert_strong_equal(layer.origin.value, NVector(0.9813190699, -2.9089243412))
        self.assert_strong_equal(layer.use_kerning.value, True)
        self.assert_strong_equal(layer.grid_fit.value, False)

    def test_round_trip(self):
        canvas1 = api.Canvas.from_xml_file(self.file)
        canvas2 = api.Canvas.from_xml(canvas1.to_xml())
        self._check_file(canvas2)
