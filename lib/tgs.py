import enum


class TgsObject:
    def to_dict(self):
        raise NotImplementedError


def _bool(v):
    return int(v)


class TgsAnimation(TgsObject):
    """
    https://github.com/airbnb/lottie-web/blob/master/docs/json/animation.json
    """
    def __init__(self, name="sticker", framerate=60):
        self.version = "5.5.2"
        self.width = self.height = 512
        self.name = name
        self.framerate = framerate
        self.initial_frame = 0
        self.final_frame = 0
        self.threedimensional = False
        self.layers = []
        self.assets = []
        #self.chars = []

    def to_dict(self):
        return {
            "tgs": 1,
            "v": self.version,
            "fr": self.framerate,
            "ip": self.initial_frame,
            "op": self.final_frame,
            "w": self.width,
            "h": self.height,
            "nm": self.name,
            "ddd": _bool(self.threedimensional),
            "layers": list(map(lambda l: l.to_dict(), self.layers)),
            "assets": list(map(lambda l: l.to_dict(), self.assets)),
            #"chars": list(map(lambda l: l.to_dict(), self.chars)),
        }


class Transform:
    # TODO
    pass


class BlendMode(enum.Enum):
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

    def to_dict(self):
        return self.value


class ShapeLayer(TgsObject):
    """
    https://github.com/airbnb/lottie-web/blob/master/docs/json/layers/shape.json
    """
    def __init__(self, name=None, index=0):
        self.name = name or "layer" + id(self)
        self.index = index
        self.transform = Transform()
        self.auto_orient = False
        self.blend_mode = BlendMode.Normal
        self.threedimensional = False
        self.initial_frame = 0
        self.final_frame = 0
        self.start_time = 0
        self.time_stretch = 1
        self.shapes = []
        self.parent = None

    def to_dict(self):
        d = {
            "ty": 4,
            "ks": self.transform.to_dict(),
            "ao": _bool(self.auto_orient),
            "bm": self.blend_mode.to_dict(),
            "ddd": _bool(self.threedimensional),
            "ind": self.index,
            "ip": self.initial_frame,
            "op": self.final_frame,
            "st": self.start_time,
            "nm": self.name,
            "sr": self.time_stretch,
            "shapes": list(map(lambda l: l.to_dict(), self.shapes)), # Called "it" in the schema
            # hasMask, masksProperties, ef (effects), sr (stretch), parent,
            # cl (css class name), ln (html layer id),
            # hd (boolean, not in the schema)
        }
        if self.parent:
            d["parent"] = self.parent.index

        return d
