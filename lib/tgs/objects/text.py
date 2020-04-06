from .base import TgsObject, TgsProp, TgsEnum
from .properties import Value, MultiDimensional
from ..nvector import NVector


## \ingroup Lottie
## \ingroup LottieCheck
class MaskedPath(TgsObject):
    _props = [
        TgsProp("mask", "m", float),
        TgsProp("f", "f", Value),
        TgsProp("l", "l", Value),
        TgsProp("r", "r", float),
    ]

    def __init__(self):
        ## Type?
        self.mask = None
        ## First?
        self.f = None
        ## Last?
        self.l = None
        ## ??
        self.r = None


## \ingroup Lottie
## \ingroup LottieCheck
class TextAnimatorDataProperty(TgsObject):
    _props = [
        TgsProp("rotation", "r", Value),
        TgsProp("rx", "rx", Value),
        TgsProp("ry", "ry", Value),
        TgsProp("skew", "sk", Value),
        TgsProp("skew_axis", "sa", Value),
        TgsProp("scale", "s", MultiDimensional),
        TgsProp("anchor", "a", MultiDimensional),
        TgsProp("opacity", "o", Value),
        TgsProp("position", "p", MultiDimensional),
        TgsProp("stroke_width", "sw", Value),
        TgsProp("stroke_color", "sc", MultiDimensional),
        TgsProp("fill_color", "fc", MultiDimensional),
        TgsProp("fh", "fh", Value),
        TgsProp("fs", "fs", Value),
        TgsProp("fb", "fb", Value),
        TgsProp("tracking", "t", Value),
    ]

    def __init__(self):
        ## Rotation Angle: z?
        self.rotation = Value()
        ## Angle?
        self.rx = Value()
        ## Angle?
        self.ry = Value()
        ## Skew Angle
        self.skew = Value()
        ## Skew Axis
        self.skew_axis = Value()
        ## Scale 0-100?
        self.scale = MultiDimensional()
        self.anchor = MultiDimensional()
        ## Opacity 0-100?
        self.opacity = Value()
        ## Position
        self.position = MultiDimensional()
        ## Stroke width
        self.stroke_width = Value()
        ## Stroke color
        self.stroke_color = MultiDimensional()
        ## Fill color
        self.fill_color = MultiDimensional()
        self.fh = Value()
        ## 0-100?
        self.fs = Value()
        ## 0-100?
        self.fb = Value()
        ## Tracking
        self.tracking = Value()


## \ingroup Lottie
## \ingroup LottieCheck
class TextMoreOptions(TgsObject):
    _props = [
        TgsProp("alignment", "a", MultiDimensional),
        TgsProp("g", "g", float),
    ]

    def __init__(self):
        self.alignment = MultiDimensional(NVector(0, 0))
        self.g = None


## \ingroup Lottie
class TextJustify(TgsEnum):
    Left = 0
    Right = 1
    Center = 2


## \ingroup Lottie
class TextDocument(TgsObject):
    """!
    @see http://docs.aenhancers.com/other/textdocument/
    """
    _props = [
        TgsProp("font_family", "f", str),
        TgsProp("color", "fc", NVector),
        TgsProp("font_size", "s", float),
        TgsProp("line_height", "lh", float),
        TgsProp("wrap_size", "sz", NVector),
        TgsProp("text", "t", str),
        TgsProp("justify", "j", TextJustify),
        # ls?
    ]

    def __init__(self, text="", font_size=10, color=None, font_family=""):
        self.font_family = font_family
        ## Text color
        self.color = color or NVector(0, 0, 0)
        ## Line height when wrapping
        self.line_height = None
        ## Text alignment
        self.justify = TextJustify.Left
        ## Size of the box containing the text
        self.wrap_size = None
        ## Text
        self.text = text
        ## Font Size
        self.font_size = font_size


## \ingroup Lottie
class TextDataKeyframe(TgsObject):
    _props = [
        TgsProp("start", "s", TextDocument),
        TgsProp("time", "t", float),
    ]

    def __init__(self, time=0, start=None):
        ## Start value of keyframe segment.
        self.start = start
        ## Start time of keyframe segment.
        self.time = time


## \ingroup Lottie
class TextData(TgsObject):
    _props = [
        TgsProp("keyframes", "k", TextDataKeyframe, True),
    ]

    def __init__(self):
        self.keyframes = []


## \ingroup Lottie
class TextAnimatorData(TgsObject):
    _props = [
        TgsProp("properties", "a", TextAnimatorDataProperty, True),
        TgsProp("data", "d", TextData, False),
        TgsProp("more_options", "m", TextMoreOptions, False),
        TgsProp("masked_path", "p", MaskedPath),
    ]

    def __init__(self):
        self.properties = []
        self.data = TextData()
        self.more_options = TextMoreOptions()
        self.masked_path = MaskedPath()

    def add_keyframe(self, time, item):
        self.data.keyframes.append(TextDataKeyframe(time, item))


## \ingroup Lottie
class Font(TgsObject):
    _props = [
        TgsProp("ascent", "ascent", float),
        TgsProp("font_family", "fFamily", str),
        TgsProp("name", "fName", str),
        TgsProp("font_style", "fStyle", str),
    ]

    def __init__(self, font_family="sans", font_style="Regular", name=None):
        self.ascent = None
        self.font_family = font_family
        self.font_style = font_style
        self.name = name or "%s-%s" % (font_family, font_style)


## \ingroup Lottie
class FontList(TgsObject):
    _props = [
        TgsProp("list", "list", Font, True),
    ]

    def __init__(self):
        self.list = []

    def append(self, font):
        self.list.append(font)
