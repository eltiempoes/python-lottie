from .base import TgsObject, TgsProp, PseudoBool, todo_func


##\ingroup Lottie
## \todo check
class Image(TgsObject):
    _props = [
        TgsProp("height", "h", float, False),
        TgsProp("width", "w", float, False),
        TgsProp("id", "id", str, False),
        TgsProp("image", "p", str, False),
        TgsProp("image_path", "u", str, False),
        TgsProp("embedded", "e", PseudoBool, False),
    ]

    def __init__(self, id=""):
        ## Image Height
        self.height = 0
        ## Image Width
        self.width = 0
        ## Image ID
        self.id = id
        ## Image name
        self.image = ""
        ## Image path
        self.image_path = ""
        ## Image data is stored as a data: url
        self.embedded = False

    def load(self, file, format="png"):
        """!
        \param file     Filename or file object to load
        \param format   Format to store the image data as
        """
        from PIL import Image
        from io import BytesIO
        import base64
        import os
        im = Image.open(file)
        self.width, self.height = im.size
        output = BytesIO()
        im.save(output, format=format)
        self.image = "data:image/%s;base64,%s" % (
            format,
            base64.b64encode(output.getvalue()).decode("ascii")
        )
        self.embedded = True
        if not self.id:
            if isinstance(file, str):
                self.id = os.path.basename(file)
            elif hasattr(file, "name"):
                self.id = os.path.basename(file.name)
            else:
                self.id = "image_%s" % id(self)
        return self


##\ingroup Lottie
## \todo check
class Chars(TgsObject):
    _props = [
        TgsProp("character", "ch", str, False),
        TgsProp("font_family", "fFamily", str, False),
        TgsProp("font_size", "size", str, False),
        TgsProp("font_style", "style", str, False),
        TgsProp("width", "w", float, False),
        TgsProp("character_data", "data", float, False),
    ]

    def __init__(self):
        ## Character Value
        self.character = ""
        ## Character Font Family
        self.font_family = ""
        ## Character Font Size
        self.font_size = ""
        ## Character Font Style
        self.font_style = ""
        ## Character Width
        self.width = 0
        ## Character Data
        self.character_data = None


##\ingroup Lottie
## \todo check
class Precomp(TgsObject):
    _props = [
        TgsProp("id", "id", str, False),
        TgsProp("layers", "layers", todo_func, True),
    ]

    def __init__(self):
        ## Precomp ID
        self.id = ""
        ## List of Precomp Layers
        self.layers = [] # ShapeLayer, SolidLayer, CompLayer, ImageLayer, NullLayer, TextLayer
