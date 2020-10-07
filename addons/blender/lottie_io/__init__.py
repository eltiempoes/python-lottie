import importlib
import bpy
from . import blender_export, operators


def menu_func_export(self, context):
    for cls in operators.registered_classes:
        self.layout.operator(cls.bl_idname, text=cls.bl_label)


def register():
    # Ensure modules are refreshed when the addon is reloaded
    importlib.reload(blender_export)
    importlib.reload(operators)
    for cls in operators.registered_classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    for cls in operators.registered_classes:
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


bl_info = {
    "name": "Lottie/TGS export",
    "description": "Exports Lottie or Telegram animated stickers from blender",
    "author": "Mattia Basaglia",
    "version": (0, 6, 4),
    "blender": (2, 80, 0),
    "location": "File > Export",
    "wiki_url": "https://mattbas.gitlab.io/python-lottie/index.html",
    "tracker_url": "https://gitlab.com/mattbas/python-lottie/issues",
    "category": "Import-Export",
}

