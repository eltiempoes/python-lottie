import os
import sys
sys.path.append("/home/melano/Documents/Python/tgs/lib")
import tgs
from tgs import NVector

import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty
from bpy.types import Operator


class ExportOptions:
    def __init__(self, scale=64, offx=0, offy=0):
        self.scale = scale
        self.offx = offx
        self.offy = offy


def object_to_shape(obj, parent, lt):
    if obj.type == "CURVE":
        g = parent.add_shape(tgs.objects.Group())
        g.name = obj.name

        for spline in obj.data.splines:
            sh = tgs.objects.Path()
            g.add_shape(sh)
            bez = sh.shape.value = tgs.objects.Bezier()
            bez.closed = spline.use_cyclic_u
            if spline.type == "BEZIER":
                for point in spline.bezier_points:
                    vert = point.co
                    in_t = point.handle_left - vert
                    out_t = point.handle_right - vert
                    bez.add_point(NVector(*vert[:]), NVector(*in_t[:]), NVector(*out_t[:]))
            else:
                for point in spline.points:
                    bez.add_point(NVector(*point.co[:]))

        if obj.data.fill_mode != "NONE":
            fillc = obj.active_material.diffuse_color
            fill = tgs.objects.Fill(NVector(*fillc[:-1]))
            fill.opacity.value = fillc[-1] * 100
            g.add_shape(fill)

        if lt > 0:
            strokec = obj.active_material.diffuse_color
            stroke = tgs.objects.Stroke(NVector(*strokec[:-1]), lt)
            stroke.opacity.value = fillc[-1] * 100
            g.add_shape(stroke)


def collection_to_group(collection, parent, lt):
    g = tgs.objects.Group()
    parent.add_shape(g)
    g.name = collection.name

    # TODO sort by z
    for obj in collection.children:
        collection_to_group(obj, g, lt)

    for obj in collection.objects:
        object_to_shape(obj, g, lt)

    return g


def scene_to_tgs(scene, eo=ExportOptions()):
    animation = tgs.objects.Animation()
    animation.in_point = scene.frame_start
    animation.out_point = scene.frame_end
    animation.framerate = scene.render.fps
    animation.width = scene.render.resolution_x
    animation.height = scene.render.resolution_y
    animation.name = scene.name
    layer = animation.add_layer(tgs.objects.ShapeLayer())

    if scene.render.use_freestyle:
        line_thickness = scene.render.line_thickness
    else:
        line_thickness = 0
    g = collection_to_group(scene.collection, layer, line_thickness)
    g.transform.scale.value *= eo.scale
    g.transform.scale.value.y *= -1
    g.transform.position.value.x += eo.offx
    g.transform.position.value.y += eo.offy + animation.height

    return animation


class TgsExporterBase(Operator):
    def execute(self, context):
        animation = scene_to_tgs(context.scene, ExportOptions(self.scale))
        self._export_animation(animation)
        return {'FINISHED'}

    def _export_animation(self, animation):
        raise NotImplementedError()


class TgsExporterTgs(TgsExporterBase, ExportHelper):
    """
    Export Telegram animated sticker
    """
    format = "tgs"
    bl_label = "Export TGS"
    bl_idname = "tgs.export_" + format

    filename_ext = "." + format

    scale: FloatProperty(
        name="Scale",
        description="Factor to scale the scene by",
        default=64,
    )

    filter_glob: StringProperty(
        default="*." + format,
        options={'HIDDEN'},
        maxlen=255,
    )

    def _export_animation(self, animation):
        tgs.exporters.export_tgs(animation, self.filepath)


class TgsExporterLottie(TgsExporterBase, ExportHelper):
    """
    Export Lottie JSON
    """
    format = "json"
    bl_label = "Export Lottie"
    bl_idname = "tgs.export_" + format

    filename_ext = "." + format

    scale: FloatProperty(
        name="Scale",
        description="Factor to scale the scene by",
        default=64,
    )

    filter_glob: StringProperty(
        default="*." + format,
        options={'HIDDEN'},
        maxlen=255,
    )

    pretty: BoolProperty(
        name="Pretty",
        description="Pretty print the resulting JSON",
        default=False,
    )

    def _export_animation(self, animation):
        tgs.exporters.export_lottie(animation, self.filepath, self.pretty)


class TgsExporterHtml(TgsExporterBase, ExportHelper):
    """
    Export HTML with an embedded Lottie viewer
    """
    format = "html"
    bl_label = "Export Lottie HTML"
    bl_idname = "tgs.export_" + format

    filename_ext = "." + format

    scale: FloatProperty(
        name="Scale",
        description="Factor to scale the scene by",
        default=64,
    )

    filter_glob: StringProperty(
        default="*." + format,
        options={'HIDDEN'},
        maxlen=255,
    )

    def _export_animation(self, animation):
        tgs.exporters.export_embedded_html(animation, self.filepath)


classes = [TgsExporterTgs, TgsExporterLottie, TgsExporterHtml]


def menu_func_export(self, context):
    for cls in classes:
        self.layout.operator(cls.bl_idname, text=cls.bl_label)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


bl_info = {
    "name": "Lottie/TGS export",
    "description": "Exports Lottie or Telegram animated stickers from blender",
    "author": "Mattia Basaglia",
    "version": (0, 3, 0),
    "blender": (2, 80, 0),
    "location": "File > Export",
    "wiki_url": "https://mattia.basaglia.gitlab.io/tgs/index.html",
    "tracker_url": "https://gitlab.com/mattia.basaglia/tgs/issues",
    "category": "Import-Export",
}
