from .base import TgsObject, TgsProp, PseudoBool
from .layers import Layer
from .shapes import ShapeElement


## \ingroup Lottie
class Asset(TgsObject):
    @classmethod
    def _load_get_class(cls, lottiedict):
        if "p" in lottiedict or "u" in lottiedict:
            return Image
        if "layers" in lottiedict:
            return Precomp


## \ingroup Lottie
class Image(Asset):
    """!
        External image

        \see http://docs.aenhancers.com/sources/filesource/
    """
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


## \ingroup Lottie
class CharacterData(TgsObject):
    """!
    Character shapes
    """
    _props = [
        TgsProp("shapes", "shapes", ShapeElement, True),
    ]

    def __init__(self):
        self.shapes = []


## \ingroup Lottie
class Chars(TgsObject):
    """!
    Defines character shapes to avoid loading system fonts
    """
    _props = [
        TgsProp("character", "ch", str, False),
        TgsProp("font_family", "fFamily", str, False),
        TgsProp("font_size", "size", float, False),
        TgsProp("font_style", "style", str, False),
        TgsProp("width", "w", float, False),
        TgsProp("data", "data", CharacterData, False),
    ]

    def __init__(self):
        ## Character Value
        self.character = ""
        ## Character Font Family
        self.font_family = ""
        ## Character Font Size
        self.font_size = 0
        ## Character Font Style
        self.font_style = "" # Regular
        ## Character Width
        self.width = 0
        ## Character Data
        self.data = CharacterData()

    @property
    def shapes(self):
        return self.data.shapes


## \ingroup Lottie
## \ingroup LottieCheck
class Precomp(Asset):
    _props = [
        TgsProp("id", "id", str, False),
        TgsProp("layers", "layers", Layer, True),
    ]

    def __init__(self):
        ## Precomp ID
        self.id = ""
        ## List of Precomp Layers
        self.layers = []
