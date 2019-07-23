from .base import TgsObject, TgsProp, PseudoBool, todo_func, Index
from .layers import load_layer

##\defgroup Lottie Lottie
#
# Objects of the lottie file structure.


##\ingroup Lottie
class Animation(TgsObject):
    """!
    Top level object, describing the animation
    """
    _props = {
        TgsProp("in_point", "ip", float, False),
        TgsProp("out_point", "op", float, False),
        TgsProp("frame_rate", "fr", float, False),
        TgsProp("width", "w", int, False),
        TgsProp("threedimensional", "ddd", PseudoBool, False),
        TgsProp("height", "h", int, False),
        TgsProp("version", "v", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("layers", "layers", load_layer, True),
        TgsProp("assets", "assets", todo_func, True),
        #TgsProp("chars", "chars", Chars, True),
        TgsProp("tgs", "tgs", PseudoBool, False),
    }
    _version = "5.5.2"

    def __init__(self, n_frames=60, framerate=60):
        ## Marks as telegram sticker
        self.tgs = 1
        ## In Point of the Time Ruler. Sets the initial Frame of the animation.
        self.in_point = 0
        ## Out Point of the Time Ruler. Sets the final Frame of the animation
        self.out_point = n_frames
        ## Frame Rate
        self.frame_rate = framerate
        ## Composition Width
        self.width = 512
        ## Composition has 3-D layers
        self.threedimensional = False
        ## Composition Height
        self.height = 512
        ## Bodymovin Version
        self.version = self._version
        ## Composition name
        self.name = None
        ## List of Composition Layers
        self.layers = [] # ShapeLayer, SolidLayer, CompLayer, ImageLayer, NullLayer, TextLayer
        ## source items that can be used in multiple places. Comps and Images for now.
        self.assets = [] # Image, Precomp
        # source chars for text layers
        #self.chars = [] # Chars
        self._index_gen = Index()

    def add_layer(self, layer):
        """!
        \brief Appends a layer to the animation
        \see insert_layer
        """
        return self.insert_layer(len(self.layers), layer)

    def insert_layer(self, index, layer):
        """!
        \brief Inserts a layer to the animation
        \note Layers added first will be rendered on top of later layers
        """
        self.layers.insert(index, layer)
        if layer.index is None:
            layer.index = next(self._index_gen)
        if layer.in_point is None:
            layer.in_point = self.in_point
        if layer.out_point is None:
            layer.out_point = self.out_point
        return layer
