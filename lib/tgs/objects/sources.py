from .base import TgsObject, TgsProp, todo_func


class Image(TgsObject): # TODO check
    _props = [
        TgsProp("height", "h", float, False),
        TgsProp("width", "w", float, False),
        TgsProp("id", "id", str, False),
        TgsProp("image_name", "p", str, False),
        TgsProp("image_path", "u", str, False),
    ]

    def __init__(self):
        # Image Height
        self.height = 0
        # Image Width
        self.width = 0
        # Image ID
        self.id = ""
        # Image name
        self.image_name = ""
        # Image path
        self.image_path = ""


class Chars(TgsObject): # TODO check
    _props = [
        TgsProp("character", "ch", str, False),
        TgsProp("font_family", "fFamily", str, False),
        TgsProp("font_size", "size", str, False),
        TgsProp("font_style", "style", str, False),
        TgsProp("width", "w", float, False),
        TgsProp("character_data", "data", float, False),
    ]

    def __init__(self):
        # Character Value
        self.character = ""
        # Character Font Family
        self.font_family = ""
        # Character Font Size
        self.font_size = ""
        # Character Font Style
        self.font_style = ""
        # Character Width
        self.width = 0
        # Character Data
        self.character_data = None


class Precomp(TgsObject): # TODO check
    _props = [
        TgsProp("id", "id", str, False),
        TgsProp("layers", "layers", todo_func, True),
    ]

    def __init__(self):
        # Precomp ID
        self.id = ""
        # List of Precomp Layers
        self.layers = [] # ShapeLayer, SolidLayer, CompLayer, ImageLayer, NullLayer, TextLayer
