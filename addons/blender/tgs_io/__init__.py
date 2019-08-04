import bpy
from .operators import registered_classes


def menu_func_export(self, context):
    for cls in registered_classes:
        self.layout.operator(cls.bl_idname, text=cls.bl_label)


def register():
    for cls in registered_classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    for cls in registered_classes:
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

