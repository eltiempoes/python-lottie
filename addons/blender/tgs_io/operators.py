from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty
from bpy.types import Operator

from . import blender_export


class TgsExporterBase(Operator):
    def execute(self, context):
        options = blender_export.ExportOptions(self.scale)
        animation = blender_export.scene_to_tgs(context.scene, options)
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
        blender_export.tgs.exporters.export_tgs(animation, self.filepath)


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
        blender_export.tgs.exporters.export_lottie(animation, self.filepath, self.pretty)


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
        blender_export.tgs.exporters.export_embedded_html(animation, self.filepath)


registered_classes = [TgsExporterTgs, TgsExporterLottie, TgsExporterHtml]
