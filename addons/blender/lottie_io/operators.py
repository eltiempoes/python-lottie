from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty
from bpy.types import Operator

from . import blender_export


class LottieExporterBase(Operator):
    def execute(self, context):
        animation = blender_export.context_to_tgs(context)
        self._export_animation(animation)
        return {'FINISHED'}

    def _export_animation(self, animation):
        raise NotImplementedError()


class LottieExporterTgs(LottieExporterBase, ExportHelper):
    """
    Export Telegram animated sticker
    """
    format = "tgs"
    bl_label = "Telegram Sticker (*.tgs)"
    bl_idname = "lottie.export_" + format

    filename_ext = "." + format

    filter_glob: StringProperty(
        default="*." + format,
        options={'HIDDEN'},
        maxlen=255,
    )

    def _export_animation(self, animation):
        blender_export.lottie.exporters.export_tgs(animation, self.filepath)


class LottieExporterLottie(LottieExporterBase, ExportHelper):
    """
    Export Lottie JSON
    """
    format = "json"
    bl_label = "Lottie (.json)"
    bl_idname = "lottie.export_" + format

    filename_ext = "." + format

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
        blender_export.lottie.exporters.export_lottie(animation, self.filepath, self.pretty)


class LottieExporterHtml(LottieExporterBase, ExportHelper):
    """
    Export HTML with an embedded Lottie viewer
    """
    format = "html"
    bl_label = "Lottie HTML (.html)"
    bl_idname = "lottie.export_" + format

    filename_ext = "." + format

    filter_glob: StringProperty(
        default="*." + format,
        options={'HIDDEN'},
        maxlen=255,
    )

    def _export_animation(self, animation):
        blender_export.lottie.exporters.export_embedded_html(animation, self.filepath)


registered_classes = [LottieExporterTgs, LottieExporterLottie, LottieExporterHtml]
