from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty
from bpy.types import Operator

from . import blender_export


_exporters = {
    "KeepStructure": blender_export.BlenderTgsExporterKeepStructure,
    "CameraView": blender_export.BlenderTgsExporterCameraView,
}

_exporter_choices = EnumProperty(
        name="Renderer",
        description="How to render the scene into an animation",
        items=(
            ("KeepStructure", "Keep Structure", "Preserve transformations and collections metadata.\n" +
             "seful for editing the output file but might yield incorrect results."),
            ("CameraView", "Baked", "Just render things the way the camera sees them as best as possible."),
        ),
        default="CameraView",
    )


class TgsExporterBase(Operator):
    def execute(self, context):
        animation = _exporters[self.exporter]()(context.scene)
        self._export_animation(animation)
        return {'FINISHED'}

    def _export_animation(self, animation):
        raise NotImplementedError()


class TgsExporterTgs(TgsExporterBase, ExportHelper):
    """
    Export Telegram animated sticker
    """
    format = "tgs"
    bl_label = "Telegram Sticker (*.tgs)"
    bl_idname = "tgs.export_" + format

    filename_ext = "." + format

    filter_glob: StringProperty(
        default="*." + format,
        options={'HIDDEN'},
        maxlen=255,
    )

    exporter: _exporter_choices

    def _export_animation(self, animation):
        blender_export.tgs.exporters.export_tgs(animation, self.filepath)


class TgsExporterLottie(TgsExporterBase, ExportHelper):
    """
    Export Lottie JSON
    """
    format = "json"
    bl_label = "Lottie (.json)"
    bl_idname = "tgs.export_" + format

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

    exporter: _exporter_choices

    def _export_animation(self, animation):
        blender_export.tgs.exporters.export_lottie(animation, self.filepath, self.pretty)


class TgsExporterHtml(TgsExporterBase, ExportHelper):
    """
    Export HTML with an embedded Lottie viewer
    """
    format = "html"
    bl_label = "Lottie HTML (.html)"
    bl_idname = "tgs.export_" + format

    filename_ext = "." + format

    filter_glob: StringProperty(
        default="*." + format,
        options={'HIDDEN'},
        maxlen=255,
    )

    exporter: _exporter_choices

    def _export_animation(self, animation):
        blender_export.tgs.exporters.export_embedded_html(animation, self.filepath)


registered_classes = [TgsExporterTgs, TgsExporterLottie, TgsExporterHtml]
