from .base import TgsObject, TgsProp, PseudoBool, Index
from .layers import Layer
from .assets import Asset, Chars
from .text import FontList

##\defgroup Lottie Lottie
#
# Objects of the lottie file structure.

## \defgroup LottieCheck Lottie (to check)
#
# Lottie objects that have not been tested


## \ingroup Lottie
class Animation(TgsObject):
    """!
    Top level object, describing the animation

    @see http://docs.aenhancers.com/items/compitem/
    @todo rename to Composition?
    """
    _props = [
        TgsProp("version", "v", str, False),
        TgsProp("frame_rate", "fr", float, False),
        TgsProp("in_point", "ip", float, False),
        TgsProp("out_point", "op", float, False),
        TgsProp("width", "w", int, False),
        TgsProp("height", "h", int, False),
        TgsProp("name", "nm", str, False),
        TgsProp("threedimensional", "ddd", PseudoBool, False),
        TgsProp("assets", "assets", Asset, True),
        #TgsProp("comps", "comps", Animation, True),
        TgsProp("fonts", "fonts", FontList),
        TgsProp("layers", "layers", Layer, True),
        TgsProp("chars", "chars", Chars, True),
        #TgsProp("markers", "markers", Marker, True),
        TgsProp("tgs", "tgs", PseudoBool, False),
        #TgsProp("motion_blur", "mb", MotionBlur, False),
    ]
    _version = "5.5.2"

    def __init__(self, n_frames=60, framerate=60):
        ## Marks as telegram sticker
        self.tgs = 1
        ## The time when the composition work area begins, in frames.
        self.in_point = 0
        ## The time when the composition work area ends.
        ## Sets the final Frame of the animation
        self.out_point = n_frames
        ## Frames per second
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
        ## source chars for text layers
        self.chars = None
        ## Available fonts
        self.fonts = None
        self._index_gen = Index()

    def add_layer(self, layer):
        """!
        @brief Appends a layer to the animation
        \see insert_layer
        """
        return self.insert_layer(len(self.layers), layer)

    def insert_layer(self, index, layer):
        """!
        @brief Inserts a layer to the animation
        @note Layers added first will be rendered on top of later layers
        """
        self.layers.insert(index, layer)
        if layer.index is None:
            layer.index = next(self._index_gen)
        if layer.in_point is None:
            layer.in_point = self.in_point
        if layer.out_point is None:
            layer.out_point = self.out_point
        return layer

    def clone(self):
        c = super().clone()
        c._index_gen._i = self._index_gen._i
        return c

    def tgs_sanitize(self):
        """!
        Cleans up some things to ensure it works as a telegram sticker
        """
        if self.width != 512 or self.height != 512:
            scale = min(512/self.width, 512/self.height)
            self.width = self.height = 512

            for layer in self.layers:
                if layer.transform.scale.animated:
                    for kf in layer.transform.scale.keyframes:
                        if kf.start is not None:
                            kf.start *= scale
                        if kf.end is not None:
                            kf.end *= scale
                else:
                    layer.transform.scale.value *= scale

        if self.frame_rate < 45:
            self.frame_rate = 30
        else:
            self.frame_rate = 60
