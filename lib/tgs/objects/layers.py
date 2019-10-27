from .base import TgsObject, TgsProp, PseudoBool, TgsEnum
from .effects import Effect
from .helpers import Transform, Mask
from .shapes import ShapeElement
from .text import TextAnimatorData
from .properties import Value


## \ingroup Lottie
class BlendMode(TgsEnum):
    Normal = 0
    Multiply = 1
    Screen = 2
    Overlay = 3
    Darken = 4
    Lighten = 5
    ColorDodge = 6
    ColorBurn = 7
    HardLight = 8
    SoftLight = 9
    Difference = 10
    Exclusion = 11
    Hue = 12
    Saturation = 13
    Color = 14
    Luminosity = 15


## \ingroup Lottie
## \todo SVG masks, transparent gradients
class MatteMode(TgsEnum):
    Normal = 0
    Alpha = 1
    InvertedAlpha = 2
    Luma = 3
    InvertedLuma = 4


## \ingroup Lottie
class Layer(TgsObject):
    _props = [
        TgsProp("type", "ty", int, False),
        TgsProp("transform", "ks", Transform, False),
        TgsProp("auto_orient", "ao", PseudoBool, False),
        TgsProp("blend_mode", "bm", BlendMode, False),
        TgsProp("matte_mode", "tt", MatteMode, False),
        TgsProp("threedimensional", "ddd", PseudoBool, False),
        TgsProp("hidden", "hd", bool, False),
        TgsProp("index", "ind", int, False),
        #TgsProp("css_class", "cl", str, False),
        #TgsProp("layer_html_id", "ln", str, False),
        TgsProp("in_point", "ip", float, False),
        TgsProp("out_point", "op", float, False),
        TgsProp("start_time", "st", float, False),
        TgsProp("name", "nm", str, False),
        TgsProp("has_masks", "hasMask", bool, False),
        TgsProp("masks", "masksProperties", Mask, True),
        TgsProp("effects", "ef", Effect, True),
        TgsProp("stretch", "sr", float, False),
        TgsProp("parent", "parent", int, False),
    ]
    ## %Layer type.
    ## @see https://github.com/bodymovin/bodymovin-extension/blob/master/bundle/jsx/enums/layerTypes.jsx
    type = None
    _classses = {}

    @property
    def has_masks(self):
        """!
        Whether the layer has some masks applied
        """
        return bool(self.masks) if getattr(self, "masks") is not None else None

    def __init__(self):
        ## Transform properties
        self.transform = Transform()
        ## Auto-Orient along path AE property.
        self.auto_orient = False
        ## 3d layer flag
        self.threedimensional = False
        ## Hidden layer
        self.hidden = None
        ## Layer index in AE. Used for parenting and expressions.
        self.index = None

        """
        # Parsed layer name used as html class on SVG/HTML renderer
        #self.css_class = ""
        # Parsed layer name used as html id on SVG/HTML renderer
        #self.layer_html_id = ""
        """
        ## In Point of layer. Sets the initial frame of the layer.
        self.in_point = None
        ## Out Point of layer. Sets the final frame of the layer.
        self.out_point = None
        ## Start Time of layer. Sets the start time of the layer.
        self.start_time = 0
        ## After Effects Layer Name. Used for expressions.
        self.name = None
        ## List of Effects
        self.effects = None
        ## Layer Time Stretching
        self.stretch = 1
        ## Layer Parent. Uses ind of parent.
        self.parent = None
        ## List of Masks
        self.masks = None
        ## Blend Mode
        self.blend_mode = BlendMode.Normal
        ## Matte mode, the layer will inherit the transparency from the layer above
        self.matte_mode = None

    @classmethod
    def _load_get_class(cls, lottiedict):
        if not Layer._classses:
            Layer._classses = {
                sc.type: sc
                for sc in Layer.__subclasses__()
            }
        return Layer._classses[lottiedict["ty"]]

    def __repr__(self):
        return "<%s %s %s>" % (type(self).__name__, self.index, self.name)


## \ingroup Lottie
class NullLayer(Layer):
    """!
    Layer with no data, useful to group layers together
    """
    ## %Layer type.
    type = 3

    def __init__(self):
        Layer.__init__(self)


## \ingroup Lottie
class TextLayer(Layer):
    _props = [
        TgsProp("data", "t", TextAnimatorData, False),
    ]
    ## %Layer type.
    type = 5

    def __init__(self):
        Layer.__init__(self)
        ## Text Data
        self.data = TextAnimatorData()


## \ingroup Lottie
class ShapeLayer(Layer):
    """!
    Layer containing ShapeElement objects
    """
    _props = [
        TgsProp("shapes", "shapes", ShapeElement, True),
    ]
    ## %Layer type.
    type = 4

    def __init__(self):
        Layer.__init__(self)
        ## Shape list of items
        self.shapes = [] # ShapeElement

    def add_shape(self, shape):
        self.shapes.append(shape)
        return shape

    def insert_shape(self, index, shape):
        self.shapes.insert(index, shape)
        return shape


## \ingroup Lottie
## \todo SVG/SIF I/O
## \todo importers for raster images without vectorization
class ImageLayer(Layer):
    _props = [
        TgsProp("image_id", "refId", str, False),
    ]
    ## %Layer type.
    type = 2

    def __init__(self, image_id=""):
        Layer.__init__(self)
        ## id pointing to the source image defined on 'assets' object
        self.image_id = image_id


## \ingroup Lottie
## \ingroup LottieCheck
class PreCompLayer(Layer):
    _props = [
        TgsProp("reference_id", "refId", str, False),
        TgsProp("time_remapping", "tm", float, False),
    ]
    ## %Layer type.
    type = 0

    def __init__(self):
        Layer.__init__(self)
        ## id pointing to the source composition defined on 'assets' object
        self.reference_id = ""
        ## Comp's Time remapping
        self.time_remapping = Value()


## \ingroup Lottie
class SolidColorLayer(Layer):
    """!
    Layer with a solid color rectangle
    """
    _props = [
        TgsProp("color", "sc", str, False),
        TgsProp("height", "sh", float, False),
        TgsProp("width", "sw", float, False),
    ]
    ## %Layer type.
    type = 1

    def __init__(self, color="", width=0, height=0):
        Layer.__init__(self)
        ## Color of the layer as a \c \#rrggbb hex
        # \todo Convert NVector to string
        self.color = color
        ## Height of the layer.
        self.height = height
        ## Width of the layer.
        self.width = width
