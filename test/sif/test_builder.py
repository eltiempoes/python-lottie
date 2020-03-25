import math
from tgs.parsers.sif import api, builder
from tgs import objects
from tgs.nvector import NVector, Color
from .. import base


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
        from tgs.exporters.core import export_embedded_html
        sif = builder.to_sif(lot)
        export_embedded_html(lot, "/tmp/testout.html")
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
