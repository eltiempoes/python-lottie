import math
from .. import base
from lottie.parsers.sif import api, builder, ast
from lottie import objects
from lottie.nvector import NVector
from lottie.utils.color import Color


class TestSifBuilder(base.TestCase):
    def test_empty(self):
        lot = objects.Animation()
        lot.width = 123
        lot.height = 456
        lot.frame_rate = 69
        lot.in_point = 3
        lot.out_point = 7
        lot.name = "test"
        sif = builder.to_sif(lot)
        self.assertEqual(sif.width, lot.width)
        self.assertEqual(sif.height, lot.height)
        self.assertEqual(sif.fps, lot.frame_rate)
        self.assertEqual(sif.begin_time, api.FrameTime.frame(3))
        self.assertEqual(sif.end_time, api.FrameTime.frame(7))
        self.assertEqual(sif.name, lot.name)

    def _visualize_test(self, lot):
        from lottie.exporters.core import export_embedded_html
        export_embedded_html(lot, "/tmp/testout.html")
        sif = builder.to_sif(lot)
        with open("/tmp/testout.sif", "w") as sifile:
            sif.to_xml().writexml(sifile, "", "  ", "\n")

    def test_star_fill(self):
        lot = objects.Animation()
        sl = lot.add_layer(objects.ShapeLayer())

        star = sl.add_shape(objects.Star())
        star.name = "Star"
        star.rotation.value = 20
        star.inner_radius.value = 64
        star.outer_radius.value = 128
        star.position.value = NVector(256, 256)
        sl.add_shape(objects.Fill(Color(1, 1, 0)))

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 1)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)

        grp = sif.layers[0]
        self.assertEqual(len(grp.layers), 1)
        self.assertIsInstance(grp.layers[0], api.RegionLayer)
        self.assertTrue(grp.active)

        rgl = grp.layers[0]
        self.assertEqual(rgl.desc, "Star")
        self.assertEqual(len(rgl.bline.points), 10)
        self.assert_nvector_equal(rgl.origin.value, star.position.value)
        self.assert_nvector_equal(rgl.color.value, sif.make_color(1, 1, 0, 1))
        self.assertTrue(rgl.active)

        # TODO check points?

    def test_star_hidden_parent(self):
        lot = objects.Animation()
        sl = lot.add_layer(objects.ShapeLayer())
        sl.hidden = True

        star = sl.add_shape(objects.Star())
        star.name = "Star"
        star.rotation.value = 20
        star.inner_radius.value = 64
        star.outer_radius.value = 128
        star.position.value = NVector(256, 256)
        sl.add_shape(objects.Fill(Color(1, 1, 0)))

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 1)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)

        grp = sif.layers[0]
        self.assertEqual(len(grp.layers), 1)
        self.assertIsInstance(grp.layers[0], api.RegionLayer)
        self.assertFalse(grp.active)

        rgl = grp.layers[0]
        self.assertEqual(rgl.desc, "Star")
        self.assertEqual(len(rgl.bline.points), 10)
        self.assert_nvector_equal(rgl.origin.value, star.position.value)
        self.assert_nvector_equal(rgl.color.value, sif.make_color(1, 1, 0, 1))
        self.assertTrue(rgl.active)

    def test_star_hidden(self):
        lot = objects.Animation()
        sl = lot.add_layer(objects.ShapeLayer())

        star = sl.add_shape(objects.Star())
        star.hidden = True
        star.name = "Star"
        star.rotation.value = 20
        star.inner_radius.value = 64
        star.outer_radius.value = 128
        star.position.value = NVector(256, 256)
        sl.add_shape(objects.Fill(Color(1, 1, 0)))

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 1)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)

        grp = sif.layers[0]
        self.assertEqual(len(grp.layers), 1)
        self.assertIsInstance(grp.layers[0], api.RegionLayer)
        self.assertTrue(grp.active)

        rgl = grp.layers[0]
        self.assertEqual(rgl.desc, "Star")
        self.assertEqual(len(rgl.bline.points), 10)
        self.assert_nvector_equal(rgl.origin.value, star.position.value)
        self.assert_nvector_equal(rgl.color.value, sif.make_color(1, 1, 0, 1))
        self.assertFalse(rgl.active)

    def test_star_outline(self):
        lot = objects.Animation()
        sl = lot.add_layer(objects.ShapeLayer())

        star = sl.add_shape(objects.Star())
        star.name = "Star"
        star.rotation.value = 20
        star.inner_radius.value = 64
        star.outer_radius.value = 128
        star.position.value = NVector(256, 256)
        sl.add_shape(objects.Stroke(Color(1, 1, 0), 10))

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 1)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)

        grp = sif.layers[0]
        self.assertEqual(len(grp.layers), 1)
        self.assertIsInstance(grp.layers[0], api.OutlineLayer)
        self.assertTrue(grp.active)

        rgl = grp.layers[0]
        self.assertEqual(rgl.desc, "Star")
        self.assertEqual(len(rgl.bline.points), 10)
        self.assert_nvector_equal(rgl.origin.value, star.position.value)
        self.assert_nvector_equal(rgl.color.value, sif.make_color(1, 1, 0, 1))
        self.assertTrue(rgl.active)
        self.assertTrue(rgl.bline.loop)
        self.assertEqual(rgl.width.value, 5)

    def test_star_outfill(self):
        lot = objects.Animation()
        sl = lot.add_layer(objects.ShapeLayer())

        star = sl.add_shape(objects.Star())
        star.name = "Star"
        star.rotation.value = 20
        star.inner_radius.value = 64
        star.outer_radius.value = 128
        star.position.value = NVector(256, 256)
        sl.add_shape(objects.Fill(Color(1, 1, 0)))
        sl.add_shape(objects.Stroke(Color(1, 0, 0), 10))

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 1)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)

        grp = sif.layers[0]
        self.assertEqual(len(grp.layers), 2)
        self.assertTrue(grp.active)

        rgl = grp.layers[1]
        self.assertIsInstance(rgl, api.RegionLayer)
        self.assertEqual(rgl.desc, "Star")
        self.assertEqual(len(rgl.bline.points), 10)
        self.assert_nvector_equal(rgl.origin.value, star.position.value)
        self.assert_nvector_equal(rgl.color.value, sif.make_color(1, 1, 0, 1))
        self.assertTrue(rgl.active)
        self.assertTrue(rgl.bline.loop)

        out = grp.layers[0]
        self.assertIsInstance(out, api.OutlineLayer)
        self.assertEqual(out.desc, "Star")
        self.assertEqual(len(out.bline.points), 10)
        self.assert_nvector_equal(out.origin.value, star.position.value)
        self.assert_nvector_equal(out.color.value, sif.make_color(1, 0, 0, 1))
        self.assertTrue(out.active)
        self.assertTrue(out.bline.loop)

    def test_rect(self):
        lot = objects.Animation()
        sl = lot.add_layer(objects.ShapeLayer())

        rect = sl.add_shape(objects.Rect())
        rect.position.value = NVector(256, 256)
        rect.size.value = NVector(128, 256)
        sl.add_shape(objects.Fill(Color(1, .25, 0)))

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 1)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)

        grp = sif.layers[0]
        self.assertEqual(len(grp.layers), 1)
        self.assertIsInstance(grp.layers[0], api.RegionLayer)
        self.assertTrue(grp.active)

        rgl = grp.layers[0]
        self.assertEqual(len(rgl.bline.points), 4)
        self.assert_nvector_equal(rgl.origin.value, rect.position.value)
        self.assert_nvector_equal(rgl.color.value, sif.make_color(1, .25, 0))
        self.assertTrue(rgl.active)

        self.assert_nvector_equal(rgl.bline.points[0].point.value, NVector(-64, -128))
        self.assert_nvector_equal(rgl.bline.points[1].point.value, NVector(+64, -128))
        self.assert_nvector_equal(rgl.bline.points[2].point.value, NVector(+64, +128))
        self.assert_nvector_equal(rgl.bline.points[3].point.value, NVector(-64, +128))

        self.assert_nvector_equal(rgl.bline.points[0].t1.value, NVector(0, 0))
        self.assert_nvector_equal(rgl.bline.points[1].t1.value, NVector(0, 0))
        self.assert_nvector_equal(rgl.bline.points[2].t1.value, NVector(0, 0))
        self.assert_nvector_equal(rgl.bline.points[3].t1.value, NVector(0, 0))

        self.assert_nvector_equal(rgl.bline.points[0].t2.value, NVector(0, 0))
        self.assert_nvector_equal(rgl.bline.points[1].t2.value, NVector(0, 0))
        self.assert_nvector_equal(rgl.bline.points[2].t2.value, NVector(0, 0))
        self.assert_nvector_equal(rgl.bline.points[3].t2.value, NVector(0, 0))

    def test_circle(self):
        lot = objects.Animation()
        sl = lot.add_layer(objects.ShapeLayer())

        ellipse = sl.add_shape(objects.Ellipse())
        ellipse.position.value = NVector(256, 256)
        ellipse.size.value = NVector(512, 512)
        sl.add_shape(objects.Fill(Color(.25, .25, .25)))

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 1)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)

        grp = sif.layers[0]
        self.assertEqual(len(grp.layers), 1)
        self.assertIsInstance(grp.layers[0], api.RegionLayer)
        self.assertTrue(grp.active)

        rgl = grp.layers[0]
        self.assertEqual(len(rgl.bline.points), 4)
        self.assert_nvector_equal(rgl.origin.value, ellipse.position.value)
        self.assert_nvector_equal(rgl.color.value, sif.make_color(.25, .25, .25))
        self.assertTrue(rgl.active)

        self.assert_nvector_equal(rgl.bline.points[0].point.value, NVector(0, 256))
        self.assert_nvector_equal(rgl.bline.points[1].point.value, NVector(-256, 0))
        self.assert_nvector_equal(rgl.bline.points[2].point.value, NVector(0, -256))
        self.assert_nvector_equal(rgl.bline.points[3].point.value, NVector(256, 0))

        self.assertNotAlmostEqual(rgl.bline.points[0].t1.value.x, 0)
        self.assertAlmostEqual(rgl.bline.points[0].t1.value.y, 0)

        self.assertNotAlmostEqual(rgl.bline.points[1].t1.value.y, 0)
        self.assertAlmostEqual(rgl.bline.points[1].t1.value.x, 0)

        self.assertNotAlmostEqual(rgl.bline.points[2].t1.value.x, 0)
        self.assertAlmostEqual(rgl.bline.points[2].t1.value.y, 0)

        self.assertNotAlmostEqual(rgl.bline.points[3].t1.value.y, 0)
        self.assertAlmostEqual(rgl.bline.points[3].t1.value.x, 0)

        for i in range(4):
            self.assert_nvector_equal(rgl.bline.points[i].t1.value,  rgl.bline.points[i].t2.value)

    def test_bezier(self):
        lot = objects.Animation()
        sl = lot.add_layer(objects.ShapeLayer())

        shape = sl.add_shape(objects.Path())
        sl.add_shape(objects.Fill(Color(0, .25, 1)))
        shape.shape.value.closed = True
        shape.shape.value.add_point(NVector(256, 0))
        shape.shape.value.add_point(NVector(256+128, 256), NVector(0, 0), NVector(64, 128))
        shape.shape.value.add_smooth_point(NVector(256, 512), NVector(128, 0))
        shape.shape.value.add_point(NVector(256-128, 256), NVector(-64, 128), NVector(0, 0))

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 1)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)

        grp = sif.layers[0]
        self.assertEqual(len(grp.layers), 1)
        self.assertIsInstance(grp.layers[0], api.RegionLayer)
        self.assertTrue(grp.active)

        rgl = grp.layers[0]
        self.assertEqual(len(rgl.bline.points), 4)
        self.assert_nvector_equal(rgl.color.value, sif.make_color(0, .25, 1))
        self.assertTrue(rgl.active)
        self.assertTrue(rgl.bline.loop)

        for i in range(len(rgl.bline.points)):
            sp = rgl.bline.points[i]
            lp = shape.shape.value.vertices[i] - NVector(256, 256)
            self.assert_nvector_equal(
                sp.point.value, lp,
                msg="Point %s mismatch %s != %s" % (i, sp.point.value, lp)
            )

            lt1 = shape.shape.value.in_tangents[i] * -3
            self.assert_nvector_equal(
                sp.t1.value, lt1,
                msg="In Tangent %s mismatch %s != %s" % (i, sp.t1.value, lt1)
            )

            lt2 = shape.shape.value.out_tangents[i] * 3
            self.assert_nvector_equal(
                sp.t2.value, lt2,
                msg="Out Tangent %s mismatch %s != %s" % (i, sp.t2.value, lt2)
            )

    def test_group_opacity(self):
        lot = objects.Animation()

        ref_sl = lot.add_layer(objects.ShapeLayer())
        ref_rect = ref_sl.add_shape(objects.Rect())
        ref_rect.position.value = NVector(128, 128)
        ref_rect.size.value = NVector(256, 256)
        ref_sl.add_shape(objects.Fill(Color(1, 0, 0)))
        ref_sl.transform.opacity.value = 80

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 1)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)
        self.assertAlmostEqual(sif.layers[0].amount.value, 0.8)

    def test_group_translate(self):
        lot = objects.Animation()

        ref_sl = lot.add_layer(objects.ShapeLayer())
        ref_rect = ref_sl.add_shape(objects.Rect())
        ref_rect.position.value = NVector(128, 128)
        ref_rect.size.value = NVector(256, 256)
        ref_sl.add_shape(objects.Fill(Color(1, 0, 0)))
        ref_sl.transform.opacity.value = 80

        sl = lot.add_layer(objects.ShapeLayer())
        rect = sl.add_shape(objects.Rect())
        rect.position.value = NVector(128, 128)
        rect.size.value = NVector(256, 256)
        sl.add_shape(objects.Fill(Color(1, 1, 0)))

        sl.transform.position.value = NVector(128, 128)

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 2)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)
        self.assertIsInstance(sif.layers[1], api.GroupLayer)
        self.assertAlmostEqual(sif.layers[0].amount.value, 1)
        self.assertAlmostEqual(sif.layers[1].amount.value, 0.8)

        self.assert_nvector_equal(sif.layers[0].transformation.offset.value, NVector(128, 128))
        self.assert_nvector_equal(sif.layers[1].transformation.offset.value, NVector(0, 0))

    def test_group_translate_anchor(self):
        lot = objects.Animation()

        ref_sl = lot.add_layer(objects.ShapeLayer())
        ref_rect = ref_sl.add_shape(objects.Rect())
        ref_rect.position.value = NVector(128, 128)
        ref_rect.size.value = NVector(256, 256)
        ref_sl.add_shape(objects.Fill(Color(1, 0, 0)))
        ref_sl.transform.opacity.value = 80

        sl = lot.add_layer(objects.ShapeLayer())
        rect = sl.add_shape(objects.Rect())
        rect.position.value = NVector(128, 128)
        rect.size.value = NVector(256, 256)
        sl.add_shape(objects.Fill(Color(1, 1, 0)))

        sl.transform.position.value = NVector(128, 128)
        sl.transform.anchor_point.value = NVector(128, 128)

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 2)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)
        self.assertIsInstance(sif.layers[1], api.GroupLayer)
        self.assertAlmostEqual(sif.layers[0].amount.value, 1)
        self.assertAlmostEqual(sif.layers[1].amount.value, 0.8)

        self.assert_nvector_equal(sif.layers[0].transformation.offset.value, NVector(128, 128))
        self.assert_nvector_equal(sif.layers[0].origin.value, NVector(128, 128))

        self.assert_nvector_equal(sif.layers[1].transformation.offset.value, NVector(0, 0))
        self.assert_nvector_equal(sif.layers[1].origin.value, NVector(0, 0))

    def test_group_rotate(self):
        lot = objects.Animation()

        ref_sl = lot.add_layer(objects.ShapeLayer())
        ref_rect = ref_sl.add_shape(objects.Rect())
        ref_rect.position.value = NVector(128, 128)
        ref_rect.size.value = NVector(256, 256)
        ref_sl.add_shape(objects.Fill(Color(1, 0, 0)))
        ref_sl.transform.opacity.value = 80

        sl = lot.add_layer(objects.ShapeLayer())
        rect = sl.add_shape(objects.Rect())
        rect.position.value = NVector(128, 128)
        rect.size.value = NVector(256, 256)
        sl.add_shape(objects.Fill(Color(1, 1, 0)))

        sl.transform.rotation.value = 20

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 2)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)
        self.assertIsInstance(sif.layers[1], api.GroupLayer)
        self.assertAlmostEqual(sif.layers[0].amount.value, 1)
        self.assertAlmostEqual(sif.layers[1].amount.value, 0.8)

        self.assertAlmostEqual(sif.layers[0].transformation.angle.value, 20)
        self.assertAlmostEqual(sif.layers[1].transformation.angle.value, 0)

    def test_group_rotate_anchor(self):
        lot = objects.Animation()

        ref_sl = lot.add_layer(objects.ShapeLayer())
        ref_rect = ref_sl.add_shape(objects.Rect())
        ref_rect.position.value = NVector(128, 128)
        ref_rect.size.value = NVector(256, 256)
        ref_sl.add_shape(objects.Fill(Color(1, 0, 0)))
        ref_sl.transform.opacity.value = 80

        sl = lot.add_layer(objects.ShapeLayer())
        rect = sl.add_shape(objects.Rect())
        rect.position.value = NVector(128, 128)
        rect.size.value = NVector(256, 256)
        sl.add_shape(objects.Fill(Color(1, 1, 0)))

        sl.transform.rotation.value = 20
        sl.transform.position.value = NVector(128, 128)
        sl.transform.anchor_point.value = NVector(128, 128)

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 2)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)
        self.assertIsInstance(sif.layers[1], api.GroupLayer)
        self.assertAlmostEqual(sif.layers[0].amount.value, 1)
        self.assertAlmostEqual(sif.layers[1].amount.value, 0.8)

        self.assertAlmostEqual(sif.layers[0].transformation.angle.value, 20)
        self.assertAlmostEqual(sif.layers[1].transformation.angle.value, 0)

        self.assert_nvector_equal(sif.layers[0].transformation.offset.value, NVector(128, 128))
        self.assert_nvector_equal(sif.layers[0].origin.value, NVector(128, 128))

        self.assert_nvector_equal(sif.layers[1].transformation.offset.value, NVector(0, 0))
        self.assert_nvector_equal(sif.layers[1].origin.value, NVector(0, 0))

    def test_group_scale(self):
        lot = objects.Animation()

        ref_sl = lot.add_layer(objects.ShapeLayer())
        ref_rect = ref_sl.add_shape(objects.Rect())
        ref_rect.position.value = NVector(128, 128)
        ref_rect.size.value = NVector(256, 256)
        ref_sl.add_shape(objects.Fill(Color(1, 0, 0)))
        ref_sl.transform.opacity.value = 80

        sl = lot.add_layer(objects.ShapeLayer())
        rect = sl.add_shape(objects.Rect())
        rect.position.value = NVector(128, 128)
        rect.size.value = NVector(256, 256)
        sl.add_shape(objects.Fill(Color(1, 1, 0)))

        sl.transform.scale.value = NVector(180, 50)
        sl.transform.position.value = NVector(256, 256)
        sl.transform.anchor_point.value = NVector(128, 128)

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 2)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)
        self.assertIsInstance(sif.layers[1], api.GroupLayer)
        self.assertAlmostEqual(sif.layers[0].amount.value, 1)
        self.assertAlmostEqual(sif.layers[1].amount.value, 0.8)

        self.assert_nvector_equal(sif.layers[0].transformation.offset.value, NVector(256, 256))
        self.assert_nvector_equal(sif.layers[0].origin.value, NVector(128, 128))
        self.assert_nvector_equal(sif.layers[0].transformation.scale.value, NVector(1.8, .5))

        self.assert_nvector_equal(sif.layers[1].transformation.offset.value, NVector(0, 0))
        self.assert_nvector_equal(sif.layers[1].origin.value, NVector(0, 0))
        self.assert_nvector_equal(sif.layers[1].transformation.scale.value, NVector(1, 1))

    def test_animated_vector(self):
        lot = objects.Animation()

        ref_sl = lot.add_layer(objects.ShapeLayer())
        ref_rect = ref_sl.add_shape(objects.Rect())
        ref_rect.position.value = NVector(128, 128)
        ref_rect.size.value = NVector(256, 256)
        ref_sl.add_shape(objects.Fill(Color(1, 0, 0)))
        ref_sl.transform.opacity.value = 80

        sl = lot.add_layer(objects.ShapeLayer())
        rect = sl.add_shape(objects.Rect())
        rect.position.value = NVector(128, 128)
        rect.size.value = NVector(256, 256)
        sl.add_shape(objects.Fill(Color(1, 1, 0)))

        sl.transform.position.add_keyframe(0, NVector(0, 0))
        sl.transform.position.add_keyframe(30, NVector(256, 256))
        sl.transform.position.add_keyframe(60, NVector(0, 0))

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 2)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)
        self.assertIsInstance(sif.layers[1], api.GroupLayer)
        self.assertAlmostEqual(sif.layers[0].amount.value, 1)
        self.assertAlmostEqual(sif.layers[1].amount.value, 0.8)

        self.assert_nvector_equal(sif.layers[1].transformation.offset.value, NVector(0, 0))

        off = sif.layers[0].transformation.offset

        self.assert_nvector_equal(off.keyframes[0].value, NVector(0, 0))
        self.assert_nvector_equal(off.keyframes[1].value, NVector(256, 256))
        self.assert_nvector_equal(off.keyframes[2].value, NVector(0, 0))

        self.assertEqual(off.keyframes[0].time, api.FrameTime.frame(0))
        self.assertEqual(off.keyframes[1].time, api.FrameTime.frame(30))
        self.assertEqual(off.keyframes[2].time, api.FrameTime.frame(60))

        self.assertEqual(off.keyframes[0].before, api.Interpolation.Linear)
        self.assertEqual(off.keyframes[1].before, api.Interpolation.Linear)
        self.assertEqual(off.keyframes[2].before, api.Interpolation.Linear)

        self.assertEqual(off.keyframes[0].after, api.Interpolation.Linear)
        self.assertEqual(off.keyframes[1].after, api.Interpolation.Linear)
        self.assertEqual(off.keyframes[2].after, api.Interpolation.Linear)

    def test_animated_vector_ease(self):
        lot = objects.Animation()

        ref_sl = lot.add_layer(objects.ShapeLayer())
        ref_rect = ref_sl.add_shape(objects.Rect())
        ref_rect.position.value = NVector(128, 128)
        ref_rect.size.value = NVector(256, 256)
        ref_sl.add_shape(objects.Fill(Color(1, 0, 0)))
        ref_sl.transform.opacity.value = 80

        sl = lot.add_layer(objects.ShapeLayer())
        rect = sl.add_shape(objects.Rect())
        rect.position.value = NVector(128, 128)
        rect.size.value = NVector(256, 256)
        sl.add_shape(objects.Fill(Color(1, 1, 0)))

        sl.transform.position.add_keyframe(0, NVector(0, 0), objects.easing.Sigmoid())
        sl.transform.position.add_keyframe(30, NVector(256, 256), objects.easing.Sigmoid())
        sl.transform.position.add_keyframe(60, NVector(0, 0), objects.easing.Sigmoid())

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 2)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)
        self.assertIsInstance(sif.layers[1], api.GroupLayer)
        self.assertAlmostEqual(sif.layers[0].amount.value, 1)
        self.assertAlmostEqual(sif.layers[1].amount.value, 0.8)

        self.assert_nvector_equal(sif.layers[1].transformation.offset.value, NVector(0, 0))

        off = sif.layers[0].transformation.offset

        self.assert_nvector_equal(off.keyframes[0].value, NVector(0, 0))
        self.assert_nvector_equal(off.keyframes[1].value, NVector(256, 256))
        self.assert_nvector_equal(off.keyframes[2].value, NVector(0, 0))

        self.assertEqual(off.keyframes[0].time, api.FrameTime.frame(0))
        self.assertEqual(off.keyframes[1].time, api.FrameTime.frame(30))
        self.assertEqual(off.keyframes[2].time, api.FrameTime.frame(60))

        #self.assertEqual(off.keyframes[0].before, api.Interpolation.Ease)
        self.assertEqual(off.keyframes[1].before, api.Interpolation.Ease)
        self.assertEqual(off.keyframes[2].before, api.Interpolation.Ease)

        self.assertEqual(off.keyframes[0].after, api.Interpolation.Ease)
        self.assertEqual(off.keyframes[1].after, api.Interpolation.Ease)
        #self.assertEqual(off.keyframes[2].after, api.Interpolation.Ease)

    def test_animated_vector_jump(self):
        lot = objects.Animation()

        ref_sl = lot.add_layer(objects.ShapeLayer())
        ref_rect = ref_sl.add_shape(objects.Rect())
        ref_rect.position.value = NVector(128, 128)
        ref_rect.size.value = NVector(256, 256)
        ref_sl.add_shape(objects.Fill(Color(1, 0, 0)))
        ref_sl.transform.opacity.value = 80

        sl = lot.add_layer(objects.ShapeLayer())
        rect = sl.add_shape(objects.Rect())
        rect.position.value = NVector(128, 128)
        rect.size.value = NVector(256, 256)
        sl.add_shape(objects.Fill(Color(1, 1, 0)))

        sl.transform.position.add_keyframe(0, NVector(0, 0), objects.easing.Jump())
        sl.transform.position.add_keyframe(30, NVector(256, 256), objects.easing.Jump())
        sl.transform.position.add_keyframe(60, NVector(0, 0), objects.easing.Jump())

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 2)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)
        self.assertIsInstance(sif.layers[1], api.GroupLayer)
        self.assertAlmostEqual(sif.layers[0].amount.value, 1)
        self.assertAlmostEqual(sif.layers[1].amount.value, 0.8)

        self.assert_nvector_equal(sif.layers[1].transformation.offset.value, NVector(0, 0))

        off = sif.layers[0].transformation.offset

        self.assert_nvector_equal(off.keyframes[0].value, NVector(0, 0))
        self.assert_nvector_equal(off.keyframes[1].value, NVector(256, 256))
        self.assert_nvector_equal(off.keyframes[2].value, NVector(0, 0))

        self.assertEqual(off.keyframes[0].time, api.FrameTime.frame(0))
        self.assertEqual(off.keyframes[1].time, api.FrameTime.frame(30))
        self.assertEqual(off.keyframes[2].time, api.FrameTime.frame(60))

        self.assertEqual(off.keyframes[1].before, api.Interpolation.Constant)
        self.assertEqual(off.keyframes[2].before, api.Interpolation.Constant)

        self.assertEqual(off.keyframes[0].after, api.Interpolation.Constant)
        self.assertEqual(off.keyframes[1].after, api.Interpolation.Constant)

    def test_animated_real(self):
        lot = objects.Animation()

        ref_sl = lot.add_layer(objects.ShapeLayer())
        ref_rect = ref_sl.add_shape(objects.Rect())
        ref_rect.position.value = NVector(128, 128)
        ref_rect.size.value = NVector(256, 256)
        ref_sl.add_shape(objects.Fill(Color(1, 0, 0)))

        ref_sl.transform.opacity.add_keyframe(0, 100)
        ref_sl.transform.opacity.add_keyframe(30, 0)
        ref_sl.transform.opacity.add_keyframe(60, 100)

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 1)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)

        amount = sif.layers[0].amount

        self.assertAlmostEqual(amount.keyframes[0].value, 1)
        self.assertAlmostEqual(amount.keyframes[1].value, 0)
        self.assertAlmostEqual(amount.keyframes[2].value, 1)

        self.assertEqual(amount.keyframes[0].time, api.FrameTime.frame(0))
        self.assertEqual(amount.keyframes[1].time, api.FrameTime.frame(30))
        self.assertEqual(amount.keyframes[2].time, api.FrameTime.frame(60))

    def test_animated_fill(self):
        lot = objects.Animation()

        ref_sl = lot.add_layer(objects.ShapeLayer())
        ref_rect = ref_sl.add_shape(objects.Rect())
        ref_rect.position.value = NVector(128, 128)
        ref_rect.size.value = NVector(256, 256)
        fill = ref_sl.add_shape(objects.Fill())

        fill.opacity.add_keyframe(0, 100)
        fill.opacity.add_keyframe(30, 50)
        fill.opacity.add_keyframe(60, 100)
        fill.color.add_keyframe(0, NVector(1, 0, 0))
        fill.color.add_keyframe(30, NVector(0, 1, 0))
        fill.color.add_keyframe(60, NVector(1, 0, 0))

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 1)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)

        amount = sif.layers[0].layers[0].amount

        self.assertAlmostEqual(amount.keyframes[0].value, 1)
        self.assertAlmostEqual(amount.keyframes[1].value, 0.5)
        self.assertAlmostEqual(amount.keyframes[2].value, 1)

        self.assertEqual(amount.keyframes[0].time, api.FrameTime.frame(0))
        self.assertEqual(amount.keyframes[1].time, api.FrameTime.frame(30))
        self.assertEqual(amount.keyframes[2].time, api.FrameTime.frame(60))

        color = sif.layers[0].layers[0].color

        self.assert_nvector_equal(color.keyframes[0].value, sif.make_color(1, 0, 0))
        self.assert_nvector_equal(color.keyframes[1].value, sif.make_color(0, 1, 0))
        self.assert_nvector_equal(color.keyframes[2].value, sif.make_color(1, 0, 0))

        self.assertEqual(color.keyframes[0].time, api.FrameTime.frame(0))
        self.assertEqual(color.keyframes[1].time, api.FrameTime.frame(30))
        self.assertEqual(color.keyframes[2].time, api.FrameTime.frame(60))

    def test_animated_bezier(self):
        lot = objects.Animation()
        sl = lot.add_layer(objects.ShapeLayer())

        shape = sl.add_shape(objects.Path())
        sl.add_shape(objects.Fill(Color(0, .25, 1)))

        bez = objects.Bezier()
        bez.closed = True
        bez.add_point(NVector(256, 0))
        bez.add_point(NVector(256+128, 256), NVector(0, 0), NVector(64, 128))
        bez.add_smooth_point(NVector(256, 512), NVector(128, 0))
        bez.add_point(NVector(256-128, 256), NVector(-64, 128), NVector(0, 0))

        new_bez = bez.clone()
        new_bez.vertices[2] = NVector(256, 256+128)
        new_bez.in_tangents[2] = NVector(64, 64)
        new_bez.out_tangents[2] = NVector(-64, 64)

        shape.shape.add_keyframe(0, bez)
        shape.shape.add_keyframe(30, new_bez)
        shape.shape.add_keyframe(60, bez)

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 1)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)

        grp = sif.layers[0]
        self.assertEqual(len(grp.layers), 1)
        self.assertIsInstance(grp.layers[0], api.RegionLayer)
        self.assertTrue(grp.active)

        rgl = grp.layers[0]
        self.assertEqual(len(rgl.bline.points), 4)
        self.assert_nvector_equal(rgl.color.value, sif.make_color(0, .25, 1))
        self.assertTrue(rgl.active)
        self.assertTrue(rgl.bline.loop)

        for i in range(4):
            sp = rgl.bline.points[i]
            lp = bez.vertices[i] - NVector(256, 256)
            lt1 = bez.in_tangents[i] * -3
            lt2 = bez.out_tangents[i] * 3

            new_lp = new_bez.vertices[i] - NVector(256, 256)
            new_lt1 = new_bez.in_tangents[i] * -3
            new_lt2 = new_bez.out_tangents[i] * 3

            self.assertEqual(sp.point.keyframes[0].time, api.FrameTime.frame(0))
            self.assert_nvector_equal(sp.point.keyframes[0].value, lp)
            self.assert_nvector_equal(sp.t1.keyframes[0].value, lt1)
            self.assert_nvector_equal(sp.t2.keyframes[0].value, lt2)

            self.assertEqual(sp.point.keyframes[1].time, api.FrameTime.frame(30))
            self.assert_nvector_equal(sp.point.keyframes[1].value, new_lp)
            self.assert_nvector_equal(sp.t1.keyframes[1].value, new_lt1)
            self.assert_nvector_equal(sp.t2.keyframes[1].value, new_lt2)

            self.assertEqual(sp.point.keyframes[2].time, api.FrameTime.frame(60))
            self.assert_nvector_equal(sp.point.keyframes[2].value, lp)
            self.assert_nvector_equal(sp.t1.keyframes[2].value, lt1)
            self.assert_nvector_equal(sp.t2.keyframes[2].value, lt2)

    def test_shape_group(self):
        lot = objects.Animation()
        sl = lot.add_layer(objects.ShapeLayer())

        gr1 = sl.add_shape(objects.Group())
        gr1.name = "Group Shape 1"

        rect = gr1.add_shape(objects.Rect())
        rect.position.value = NVector(128, 256)
        rect.size.value = NVector(128, 256)
        gr1.add_shape(objects.Fill(Color(1, .25, 0)))

        gr2 = sl.add_shape(objects.Group())
        gr2.name = "Group Shape 2"
        rect = gr2.add_shape(objects.Rect())
        rect.position.value = NVector(256+128, 256)
        rect.size.value = NVector(128, 256)
        gr2.add_shape(objects.Fill(Color(.25, 0, 1)))

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 1)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)

        grp = sif.layers[0]
        self.assertEqual(len(grp.layers), 2)
        sg1 = grp.layers[1]
        sg2 = grp.layers[0]
        self.assertIsInstance(sg1, api.GroupLayer)
        self.assertIsInstance(sg2, api.GroupLayer)
        self.assertEqual(sg1.desc, "Group Shape 1")
        self.assertEqual(sg2.desc, "Group Shape 2")
        self.assertEqual(len(sg1.layers), 1)
        self.assertEqual(len(sg2.layers), 1)
        self.assertIsInstance(sg1.layers[0], api.RegionLayer)
        self.assertIsInstance(sg2.layers[0], api.RegionLayer)
        self.assert_nvector_equal(sg1.layers[0].color.value, sif.make_color(1, .25, 0))
        self.assert_nvector_equal(sg2.layers[0].color.value, sif.make_color(.25, 0, 1))

    def test_repeater(self):
        lot = objects.Animation()
        sl = lot.add_layer(objects.ShapeLayer())

        group = sl.add_shape(objects.Group())

        star = group.add_shape(objects.Star())
        star.inner_radius.value = 16
        star.outer_radius.value = 32
        star.position.value = NVector(256, 40)

        group.add_shape(objects.Fill(Color(1, 1, 0)))
        group.add_shape(objects.Stroke(Color(0, 0, 0), 3))
        group.name = "Star"

        rep = sl.add_shape(objects.Repeater(4))
        rep.name = "Repeater"
        rep.transform.position.value = NVector(20, 80)
        rep.transform.end_opacity.value = 20

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 1)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)
        self.assertEqual(len(sif.layers[0].layers), 1)
        self.assertIsInstance(sif.layers[0].layers[0], api.GroupLayer)
        self.assertEqual(sif.layers[0].layers[0].desc, "Repeater")
        self.assertEqual(len(sif.layers[0].layers[0].layers), 2)

        duplicate_lay = sif.layers[0].layers[0].layers[1]
        self.assertIsInstance(duplicate_lay, api.DuplicateLayer)
        self.assertEqual(duplicate_lay.desc, "Repeater")
        duplicate = sif.get_object(duplicate_lay.index.id)
        self.assertIsInstance(duplicate, api.Duplicate)
        self.assertEqual(duplicate.from_.value, 3)
        self.assertEqual(duplicate.to.value, 0)
        self.assertEqual(duplicate.step.value, -1)

        dup_trans = sif.layers[0].layers[0].layers[0]
        self.assertIsInstance(dup_trans, api.GroupLayer)
        self.assertEqual(dup_trans.desc, "Transformation for Repeater")
        dup_origin = sif.get_object(dup_trans.origin.id)
        self.assert_nvector_equal(dup_origin.value.value, NVector(0, 0))
        trans = dup_trans.transformation
        self.assertIsInstance(trans.offset, ast.SifAdd)
        self.assertEqual(trans.offset.rhs.value.id, dup_origin.id)
        self.assertIsInstance(trans.offset.lhs, ast.SifScale)
        self.assert_nvector_equal(trans.offset.lhs.link.value, NVector(20, 80))
        self.assertEqual(trans.offset.lhs.scalar.value.id, duplicate.id)
        self.assertIsInstance(trans.angle, ast.SifScale)
        self.assertEqual(trans.angle.link.value, 0)
        self.assertEqual(trans.angle.scalar.value.id, duplicate.id)
        self.assertIsInstance(dup_trans.amount, ast.SifSubtract)
        self.assertEqual(dup_trans.amount.lhs.value, 1)
        self.assertIsInstance(dup_trans.amount.rhs, ast.SifScale)
        self.assertAlmostEqual(dup_trans.amount.rhs.link.value, 0.266666666)
        self.assertEqual(dup_trans.amount.rhs.scalar.value.id, duplicate.id)
        self.assertEqual(len(dup_trans.layers), 1)
        self.assertEqual(dup_trans.layers[0].desc, "Star")

    def test_repeater_rot(self):
        lot = objects.Animation()
        sl = lot.add_layer(objects.ShapeLayer())

        group = sl.add_shape(objects.Group())

        star = group.add_shape(objects.Star())
        star.inner_radius.value = 16
        star.outer_radius.value = 32
        star.position.value = NVector(256, 40)

        group.add_shape(objects.Fill(Color(1, 1, 0)))
        group.name = "Star"

        rep = sl.add_shape(objects.Repeater(12))
        rep.name = "Repeater"
        rep.transform.anchor_point.value = NVector(256, 256)
        rep.transform.rotation.value = 30

        sif = builder.to_sif(lot)
        self.assertEqual(len(sif.layers), 1)
        self.assertIsInstance(sif.layers[0], api.GroupLayer)
        self.assertEqual(len(sif.layers[0].layers), 1)
        self.assertIsInstance(sif.layers[0].layers[0], api.GroupLayer)
        self.assertEqual(sif.layers[0].layers[0].desc, "Repeater")
        self.assertEqual(len(sif.layers[0].layers[0].layers), 2)

        duplicate_lay = sif.layers[0].layers[0].layers[1]
        self.assertIsInstance(duplicate_lay, api.DuplicateLayer)
        self.assertEqual(duplicate_lay.desc, "Repeater")
        duplicate = sif.get_object(duplicate_lay.index.id)
        self.assertIsInstance(duplicate, api.Duplicate)
        self.assertEqual(duplicate.from_.value, 11)
        self.assertEqual(duplicate.to.value, 0)
        self.assertEqual(duplicate.step.value, -1)

        dup_trans = sif.layers[0].layers[0].layers[0]
        self.assertIsInstance(dup_trans, api.GroupLayer)
        self.assertEqual(dup_trans.desc, "Transformation for Repeater")
        dup_origin = sif.get_object(dup_trans.origin.id)
        self.assert_nvector_equal(dup_origin.value.value, NVector(256, 256))
        trans = dup_trans.transformation
        self.assertIsInstance(trans.offset, ast.SifAdd)
        self.assertEqual(trans.offset.rhs.value.id, dup_origin.id)
        self.assertIsInstance(trans.offset.lhs, ast.SifScale)
        self.assert_nvector_equal(trans.offset.lhs.link.value, NVector(0, 0))
        self.assertEqual(trans.offset.lhs.scalar.value.id, duplicate.id)
        self.assertIsInstance(trans.angle, ast.SifScale)
        self.assertEqual(trans.angle.link.value, 30)
        self.assertEqual(trans.angle.scalar.value.id, duplicate.id)
        self.assertIsInstance(dup_trans.amount, ast.SifSubtract)
        self.assertEqual(dup_trans.amount.lhs.value, 1)
        self.assertIsInstance(dup_trans.amount.rhs, ast.SifScale)
        self.assertAlmostEqual(dup_trans.amount.rhs.link.value, 0.)
        self.assertEqual(dup_trans.amount.rhs.scalar.value.id, duplicate.id)
        self.assertEqual(len(dup_trans.layers), 1)
        self.assertEqual(dup_trans.layers[0].desc, "Star")
