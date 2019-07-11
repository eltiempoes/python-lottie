import re
import math
import enum
from xml.etree import ElementTree
from .. import objects
from ..utils.nvector import NVector


color_table = {
    "black": [0.0, 0.0, 0.0, 1],
    "silver": [0.7529411764705882, 0.7529411764705882, 0.7529411764705882, 1],
    "gray": [0.5019607843137255, 0.5019607843137255, 0.5019607843137255, 1],
    "white": [1.0, 1.0, 1.0, 1],
    "maroon": [0.5019607843137255, 0.0, 0.0, 1],
    "red": [1.0, 0.0, 0.0, 1],
    "purple": [0.5019607843137255, 0.0, 0.5019607843137255, 1],
    "fuchsia": [1.0, 0.0, 1.0, 1],
    "green": [0.0, 0.5019607843137255, 0.0, 1],
    "lime": [0.0, 1.0, 0.0, 1],
    "olive": [0.5019607843137255, 0.5019607843137255, 0.0, 1],
    "yellow": [1.0, 1.0, 0.0, 1],
    "navy": [0.0, 0.0, 0.5019607843137255, 1],
    "blue": [0.0, 0.0, 1.0, 1],
    "teal": [0.0, 0.5019607843137255, 0.5019607843137255, 1],
    "aqua": [0.0, 1.0, 1.0, 1],
    "aliceblue": [0.9411764705882353, 0.9725490196078431, 1.0, 1],
    "antiquewhite": [0.9803921568627451, 0.9215686274509803, 0.8431372549019608, 1],
    "aqua": [0.0, 1.0, 1.0, 1],
    "aquamarine": [0.4980392156862745, 1.0, 0.8313725490196079, 1],
    "azure": [0.9411764705882353, 1.0, 1.0, 1],
    "beige": [0.9607843137254902, 0.9607843137254902, 0.8627450980392157, 1],
    "bisque": [1.0, 0.8941176470588236, 0.7686274509803922, 1],
    "black": [0.0, 0.0, 0.0, 1],
    "blanchedalmond": [1.0, 0.9215686274509803, 0.803921568627451, 1],
    "blue": [0.0, 0.0, 1.0, 1],
    "blueviolet": [0.5411764705882353, 0.16862745098039217, 0.8862745098039215, 1],
    "brown": [0.6470588235294118, 0.16470588235294117, 0.16470588235294117, 1],
    "burlywood": [0.8705882352941177, 0.7215686274509804, 0.5294117647058824, 1],
    "cadetblue": [0.37254901960784315, 0.6196078431372549, 0.6274509803921569, 1],
    "chartreuse": [0.4980392156862745, 1.0, 0.0, 1],
    "chocolate": [0.8235294117647058, 0.4117647058823529, 0.11764705882352941, 1],
    "coral": [1.0, 0.4980392156862745, 0.3137254901960784, 1],
    "cornflowerblue": [0.39215686274509803, 0.5843137254901961, 0.9294117647058824, 1],
    "cornsilk": [1.0, 0.9725490196078431, 0.8627450980392157, 1],
    "crimson": [0.8627450980392157, 0.0784313725490196, 0.23529411764705882, 1],
    "cyan": [0.0, 1.0, 1.0, 1],
    "darkblue": [0.0, 0.0, 0.5450980392156862, 1],
    "darkcyan": [0.0, 0.5450980392156862, 0.5450980392156862, 1],
    "darkgoldenrod": [0.7215686274509804, 0.5254901960784314, 0.043137254901960784, 1],
    "darkgray": [0.6627450980392157, 0.6627450980392157, 0.6627450980392157, 1],
    "darkgreen": [0.0, 0.39215686274509803, 0.0, 1],
    "darkgrey": [0.6627450980392157, 0.6627450980392157, 0.6627450980392157, 1],
    "darkkhaki": [0.7411764705882353, 0.7176470588235294, 0.4196078431372549, 1],
    "darkmagenta": [0.5450980392156862, 0.0, 0.5450980392156862, 1],
    "darkolivegreen": [0.3333333333333333, 0.4196078431372549, 0.1843137254901961, 1],
    "darkorange": [1.0, 0.5490196078431373, 0.0, 1],
    "darkorchid": [0.6, 0.19607843137254902, 0.8, 1],
    "darkred": [0.5450980392156862, 0.0, 0.0, 1],
    "darksalmon": [0.9137254901960784, 0.5882352941176471, 0.47843137254901963, 1],
    "darkseagreen": [0.5607843137254902, 0.7372549019607844, 0.5607843137254902, 1],
    "darkslateblue": [0.2823529411764706, 0.23921568627450981, 0.5450980392156862, 1],
    "darkslategray": [0.1843137254901961, 0.30980392156862746, 0.30980392156862746, 1],
    "darkslategrey": [0.1843137254901961, 0.30980392156862746, 0.30980392156862746, 1],
    "darkturquoise": [0.0, 0.807843137254902, 0.8196078431372549, 1],
    "darkviolet": [0.5803921568627451, 0.0, 0.8274509803921568, 1],
    "deeppink": [1.0, 0.0784313725490196, 0.5764705882352941, 1],
    "deepskyblue": [0.0, 0.7490196078431373, 1.0, 1],
    "dimgray": [0.4117647058823529, 0.4117647058823529, 0.4117647058823529, 1],
    "dimgrey": [0.4117647058823529, 0.4117647058823529, 0.4117647058823529, 1],
    "dodgerblue": [0.11764705882352941, 0.5647058823529412, 1.0, 1],
    "firebrick": [0.6980392156862745, 0.13333333333333333, 0.13333333333333333, 1],
    "floralwhite": [1.0, 0.9803921568627451, 0.9411764705882353, 1],
    "forestgreen": [0.13333333333333333, 0.5450980392156862, 0.13333333333333333, 1],
    "fuchsia": [1.0, 0.0, 1.0, 1],
    "gainsboro": [0.8627450980392157, 0.8627450980392157, 0.8627450980392157, 1],
    "ghostwhite": [0.9725490196078431, 0.9725490196078431, 1.0, 1],
    "gold": [1.0, 0.8431372549019608, 0.0, 1],
    "goldenrod": [0.8549019607843137, 0.6470588235294118, 0.12549019607843137, 1],
    "gray": [0.5019607843137255, 0.5019607843137255, 0.5019607843137255, 1],
    "green": [0.0, 0.5019607843137255, 0.0, 1],
    "greenyellow": [0.6784313725490196, 1.0, 0.1843137254901961, 1],
    "grey": [0.5019607843137255, 0.5019607843137255, 0.5019607843137255, 1],
    "honeydew": [0.9411764705882353, 1.0, 0.9411764705882353, 1],
    "hotpink": [1.0, 0.4117647058823529, 0.7058823529411765, 1],
    "indianred": [0.803921568627451, 0.3607843137254902, 0.3607843137254902, 1],
    "indigo": [0.29411764705882354, 0.0, 0.5098039215686274, 1],
    "ivory": [1.0, 1.0, 0.9411764705882353, 1],
    "khaki": [0.9411764705882353, 0.9019607843137255, 0.5490196078431373, 1],
    "lavender": [0.9019607843137255, 0.9019607843137255, 0.9803921568627451, 1],
    "lavenderblush": [1.0, 0.9411764705882353, 0.9607843137254902, 1],
    "lawngreen": [0.48627450980392156, 0.9882352941176471, 0.0, 1],
    "lemonchiffon": [1.0, 0.9803921568627451, 0.803921568627451, 1],
    "lightblue": [0.6784313725490196, 0.8470588235294118, 0.9019607843137255, 1],
    "lightcoral": [0.9411764705882353, 0.5019607843137255, 0.5019607843137255, 1],
    "lightcyan": [0.8784313725490196, 1.0, 1.0, 1],
    "lightgoldenrodyellow": [0.9803921568627451, 0.9803921568627451, 0.8235294117647058, 1],
    "lightgray": [0.8274509803921568, 0.8274509803921568, 0.8274509803921568, 1],
    "lightgreen": [0.5647058823529412, 0.9333333333333333, 0.5647058823529412, 1],
    "lightgrey": [0.8274509803921568, 0.8274509803921568, 0.8274509803921568, 1],
    "lightpink": [1.0, 0.7137254901960784, 0.7568627450980392, 1],
    "lightsalmon": [1.0, 0.6274509803921569, 0.47843137254901963, 1],
    "lightseagreen": [0.12549019607843137, 0.6980392156862745, 0.6666666666666666, 1],
    "lightskyblue": [0.5294117647058824, 0.807843137254902, 0.9803921568627451, 1],
    "lightslategray": [0.4666666666666667, 0.5333333333333333, 0.6, 1],
    "lightslategrey": [0.4666666666666667, 0.5333333333333333, 0.6, 1],
    "lightsteelblue": [0.6901960784313725, 0.7686274509803922, 0.8705882352941177, 1],
    "lightyellow": [1.0, 1.0, 0.8784313725490196, 1],
    "lime": [0.0, 1.0, 0.0, 1],
    "limegreen": [0.19607843137254902, 0.803921568627451, 0.19607843137254902, 1],
    "linen": [0.9803921568627451, 0.9411764705882353, 0.9019607843137255, 1],
    "magenta": [1.0, 0.0, 1.0, 1],
    "maroon": [0.5019607843137255, 0.0, 0.0, 1],
    "mediumaquamarine": [0.4, 0.803921568627451, 0.6666666666666666, 1],
    "mediumblue": [0.0, 0.0, 0.803921568627451, 1],
    "mediumorchid": [0.7294117647058823, 0.3333333333333333, 0.8274509803921568, 1],
    "mediumpurple": [0.5764705882352941, 0.4392156862745098, 0.8588235294117647, 1],
    "mediumseagreen": [0.23529411764705882, 0.7019607843137254, 0.44313725490196076, 1],
    "mediumslateblue": [0.4823529411764706, 0.40784313725490196, 0.9333333333333333, 1],
    "mediumspringgreen": [0.0, 0.9803921568627451, 0.6039215686274509, 1],
    "mediumturquoise": [0.2823529411764706, 0.8196078431372549, 0.8, 1],
    "mediumvioletred": [0.7803921568627451, 0.08235294117647059, 0.5215686274509804, 1],
    "midnightblue": [0.09803921568627451, 0.09803921568627451, 0.4392156862745098, 1],
    "mintcream": [0.9607843137254902, 1.0, 0.9803921568627451, 1],
    "mistyrose": [1.0, 0.8941176470588236, 0.8823529411764706, 1],
    "moccasin": [1.0, 0.8941176470588236, 0.7098039215686275, 1],
    "navajowhite": [1.0, 0.8705882352941177, 0.6784313725490196, 1],
    "navy": [0.0, 0.0, 0.5019607843137255, 1],
    "oldlace": [0.9921568627450981, 0.9607843137254902, 0.9019607843137255, 1],
    "olive": [0.5019607843137255, 0.5019607843137255, 0.0, 1],
    "olivedrab": [0.4196078431372549, 0.5568627450980392, 0.13725490196078433, 1],
    "orange": [1.0, 0.6470588235294118, 0.0, 1],
    "orangered": [1.0, 0.27058823529411763, 0.0, 1],
    "orchid": [0.8549019607843137, 0.4392156862745098, 0.8392156862745098, 1],
    "palegoldenrod": [0.9333333333333333, 0.9098039215686274, 0.6666666666666666, 1],
    "palegreen": [0.596078431372549, 0.984313725490196, 0.596078431372549, 1],
    "paleturquoise": [0.6862745098039216, 0.9333333333333333, 0.9333333333333333, 1],
    "palevioletred": [0.8588235294117647, 0.4392156862745098, 0.5764705882352941, 1],
    "papayawhip": [1.0, 0.9372549019607843, 0.8352941176470589, 1],
    "peachpuff": [1.0, 0.8549019607843137, 0.7254901960784313, 1],
    "peru": [0.803921568627451, 0.5215686274509804, 0.24705882352941178, 1],
    "pink": [1.0, 0.7529411764705882, 0.796078431372549, 1],
    "plum": [0.8666666666666667, 0.6274509803921569, 0.8666666666666667, 1],
    "powderblue": [0.6901960784313725, 0.8784313725490196, 0.9019607843137255, 1],
    "purple": [0.5019607843137255, 0.0, 0.5019607843137255, 1],
    "red": [1.0, 0.0, 0.0, 1],
    "rosybrown": [0.7372549019607844, 0.5607843137254902, 0.5607843137254902, 1],
    "royalblue": [0.2549019607843137, 0.4117647058823529, 0.8823529411764706, 1],
    "saddlebrown": [0.5450980392156862, 0.27058823529411763, 0.07450980392156863, 1],
    "salmon": [0.9803921568627451, 0.5019607843137255, 0.4470588235294118, 1],
    "sandybrown": [0.9568627450980393, 0.6431372549019608, 0.3764705882352941, 1],
    "seagreen": [0.1803921568627451, 0.5450980392156862, 0.3411764705882353, 1],
    "seashell": [1.0, 0.9607843137254902, 0.9333333333333333, 1],
    "sienna": [0.6274509803921569, 0.3215686274509804, 0.17647058823529413, 1],
    "silver": [0.7529411764705882, 0.7529411764705882, 0.7529411764705882, 1],
    "skyblue": [0.5294117647058824, 0.807843137254902, 0.9215686274509803, 1],
    "slateblue": [0.41568627450980394, 0.35294117647058826, 0.803921568627451, 1],
    "slategray": [0.4392156862745098, 0.5019607843137255, 0.5647058823529412, 1],
    "slategrey": [0.4392156862745098, 0.5019607843137255, 0.5647058823529412, 1],
    "snow": [1.0, 0.9803921568627451, 0.9803921568627451, 1],
    "springgreen": [0.0, 1.0, 0.4980392156862745, 1],
    "steelblue": [0.27450980392156865, 0.5098039215686274, 0.7058823529411765, 1],
    "tan": [0.8235294117647058, 0.7058823529411765, 0.5490196078431373, 1],
    "teal": [0.0, 0.5019607843137255, 0.5019607843137255, 1],
    "thistle": [0.8470588235294118, 0.7490196078431373, 0.8470588235294118, 1],
    "tomato": [1.0, 0.38823529411764707, 0.2784313725490196, 1],
    "turquoise": [0.25098039215686274, 0.8784313725490196, 0.8156862745098039, 1],
    "violet": [0.9333333333333333, 0.5098039215686274, 0.9333333333333333, 1],
    "wheat": [0.9607843137254902, 0.8705882352941177, 0.7019607843137254, 1],
    "white": [1.0, 1.0, 1.0, 1],
    "whitesmoke": [0.9607843137254902, 0.9607843137254902, 0.9607843137254902, 1],
    "yellow": [1.0, 1.0, 0.0, 1],
    "yellowgreen": [0.6039215686274509, 0.803921568627451, 0.19607843137254902, 1],
}

css_atrrs = {
    "fill",
    "alignment-baseline",
    "baseline-shift",
    "clip-path",
    "clip-rule",
    "color",
    "color-interpolation",
    "color-interpolation-filters",
    "color-rendering",
    "cursor",
    "direction",
    "display",
    "dominant-baseline",
    "fill-opacity",
    "fill-rule",
    "filter",
    "flood-color",
    "flood-opacity",
    "font-family",
    "font-size",
    "font-size-adjust",
    "font-stretch",
    "font-style",
    "font-variant",
    "font-weight",
    "glyph-orientation-horizontal",
    "glyph-orientation-vertical",
    "image-rendering",
    "letter-spacing",
    "lighting-color",
    "marker-end",
    "marker-mid",
    "marker-start",
    "mask",
    "opacity",
    "overflow",
    "paint-order",
    "pointer-events",
    "shape-rendering",
    "stop-color",
    "stop-opacity",
    "stroke",
    "stroke-dasharray",
    "stroke-dashoffset",
    "stroke-linecap",
    "stroke-linejoin",
    "stroke-miterlimit",
    "stroke-opacity",
    "stroke-width",
    "text-anchor",
    "text-decoration",
    "text-overflow",
    "text-rendering",
    "unicode-bidi",
    "vector-effect",
    "visibility",
    "white-space",
    "word-spacing",
    "writing-mode"
}

nocolor = {"none"}


def hsl_to_rgb(h, s, l):
    if l < 0.5:
        m2 = l * (s + 1)
    else:
        m2 = l + s - l * s
    m1 = l*2 - m2
    r = hue_to_rgb(m1, m2, h+1/3)
    g = hue_to_rgb(m1, m2, h)
    b = hue_to_rgb(m1, m2, h-1/3)
    return [r, g, b]


def hue_to_rgb(m1, m2, h):
    if h < 0:
        h += 1
    elif h > 1:
        h -= 1
    if h*6 < 1:
        return m1+(m2-m1)*h*6
    elif h*2 < 1:
        return m2
    elif h*3 < 2:
        return m1+(m2-m1)*(2/3-h)*6
    return m1


class SvgHandler:
    ns_map = {
        "dc": "http://purl.org/dc/elements/1.1/",
        "cc": "http://creativecommons.org/ns#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "svg": "http://www.w3.org/2000/svg",
        "sodipodi": "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
        "inkscape": "http://www.inkscape.org/namespaces/inkscape",
    }

    def init_etree(self):
        for n, u in self.ns_map.items():
            ElementTree.register_namespace(n, u)

    def qualified(self, ns, name):
        return "{%s}%s" % (self.ns_map[ns], name)

    def simplified(self, name):
        for k, v in self.ns_map.items():
            name = name.replace("{%s}" % v, k+":")
        return name

    def unqualified(self, name):
        return name.split("}")[-1]

    def __init__(self):
        self.init_etree()


class NameMode(enum.Enum):
    NoName = 0
    Id = 1
    Inkscape = 2


class SvgGradientCoord:
    def __init__(self, comp, value, percent):
        self.comp = comp
        self.value = value
        self.percent = percent

    def to_value(self, bbox):
        if not self.percent:
            return self.value

        if self.comp == "x":
            return bbox.x1 + (bbox.x2 - bbox.x1) * self.value
        return bbox.y1 + (bbox.y2 - bbox.y1) * self.value

    def parse(self, attr, default_percent):
        if attr is None:
            return
        if attr.endswith("%"):
            self.percent = True
            self.value = float(attr[:-1])/100
        else:
            self.percent = default_percent
            self.value = float(attr)


class SvgLinearGradient:
    def __init__(self):
        self.x1 = SvgGradientCoord("x", 0, True)
        self.y1 = SvgGradientCoord("y", 0, True)
        self.x2 = SvgGradientCoord("x", 1, True)
        self.y2 = SvgGradientCoord("y", 0, True)
        self.colors = []

    def add_color(self, offset, color):
        self.colors.append((offset, color[:3]))

    def to_lottie(self, gradient_shape, shape, time=0):
        """
        gradient_shape should be a GradientFill or GradientStroke
        """
        bbox = shape.bounding_box(time)
        gradient_shape.start_point.value = [
            self.x1.to_value(bbox),
            self.y1.to_value(bbox),
        ]
        gradient_shape.end_point.value = [
            self.x2.to_value(bbox),
            self.y2.to_value(bbox),
        ]
        gradient_shape.gradient_type = objects.GradientType.Linear
        for off, col in self.colors:
            gradient_shape.colors.add_color(off, col)


class SvgParser(SvgHandler):
    def __init__(self, name_mode=NameMode.Inkscape):
        self.init_etree()
        self.name_mode = name_mode
        self.current_color = [0, 0, 0, 1]
        self.gradients ={}

    def _get_name(self, element, inkscapequal):
        if self.name_mode == NameMode.Inkscape:
            return element.attrib.get(inkscapequal, element.attrib.get("id"))
        return self._get_id(element)

    def _get_id(self, element):
        if self.name_mode != NameMode.NoName:
            return element.attrib.get("id")
        return None

    def parse_color(self, color):
        # #fff
        if re.match(r"^#[0-9a-fA-F]{6}$", color):
            return [int(color[1:3], 16) / 0xff, int(color[3:5], 16) / 0xff, int(color[5:7], 16) / 0xff, 1]
        # #112233
        if re.match(r"^#[0-9a-fA-F]{3}$", color):
            return [int(color[1], 16) / 0xf, int(color[2], 16) / 0xf, int(color[3], 16) / 0xf, 1]
        # rgba(123, 123, 123, 0.7)
        match = re.match(r"^rgba\s*\(\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9.eE]+)\s*\)$", color)
        if match:
            return [int(match[1])/255, int(match[2])/255, int(match[3])/255, float(match[4])]
        # rgb(123, 123, 123)
        match = re.match(r"^rgb\s*\(\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\s*\)$", color)
        if match:
            return [int(match[1])/255, int(match[2])/255, int(match[3])/255, 1]
        # rgb(60%, 30%, 20%)
        match = re.match(r"^rgb\s*\(\s*([0-9]+)%\s*,\s*([0-9]+)%\s*,\s*([0-9]+)%\s*\)$", color)
        if match:
            return [int(match[1])/100, int(match[2])/100, int(match[3])/100, 1]
        # rgba(60%, 30%, 20%, 0.7)
        match = re.match(r"^rgb\s*\(\s*([0-9]+)%\s*,\s*([0-9]+)%\s*,\s*([0-9]+)%\s*,\s*([0-9.eE]+)\s*\)$", color)
        if match:
            return [int(match[1])/100, int(match[2])/100, int(match[3])/100, float(match[4])]
        # transparent
        if color == "transparent":
            return [0, 0, 0, 0]
        # hsl(60, 30%, 20%)
        match = re.match(r"^hsl\s*\(\s*([0-9]+)\s*,\s*([0-9]+)%\s*,\s*([0-9]+)%\s*\)$", color)
        if match:
            return hsl_to_rgb(int(match[1])/360, int(match[2])/100, int(match[3])/100) + [1]
        # hsla(60, 30%, 20%, 0.7)
        match = re.match(r"^hsl\s*\(\s*([0-9]+)\s*,\s*([0-9]+)%\s*,\s*([0-9]+)%\s*,\s*([0-9.eE]+)\s*\)$", color)
        if match:
            return hsl_to_rgb(int(match[1])/360, int(match[2])/100, int(match[3])/100) + [float(match[4])]
        # currentColor
        if color in {"currentColor", "inherit"}:
            return self.current_color
        # red
        return color_table[color]

    def parse_transform(self, element, group, dest_trans):
        itcx = self.qualified("inkscape", "transform-center-x")
        if itcx in element.attrib:
            cx = float(element.attrib[itcx])
            cy = float(element.attrib[self.qualified("inkscape", "transform-center-y")])
            bbx, bby = group.bounding_box().center()
            cx += bbx
            cy = bby - cy
            dest_trans.anchor_point.value = [cx, cy]
            dest_trans.position.value = [cx, cy]

        if "transform" not in element.attrib:
            return

        for t in re.finditer(r"([a-zA-Z]+)\s*\(([^\)]*)\)", element.attrib["transform"]):
            name = t[1]
            params = list(map(float, t[2].strip().replace(",", " ").split()))
            if name == "translate":
                dest_trans.position.value = [
                    dest_trans.position.value[0] + params[0],
                    dest_trans.position.value[1] + (params[1] if len(params) > 1 else 0),
                ]
            elif name == "scale":
                xfac = params[0]
                dest_trans.scale.value[0] = (dest_trans.scale.value[0] / 100 * xfac) * 100
                yfac = params[1] if len(params) > 1 else xfac
                dest_trans.scale.value[1] = (dest_trans.scale.value[1] / 100 * yfac) * 100
            elif name == "rotate":
                ang = params[0]
                x = y = 0
                if len(params) > 2:
                    x = params[1]
                    y = params[2]
                    dest_trans.position.value = [
                        dest_trans.position.value[0] + x,
                        dest_trans.position.value[1] + y
                    ]
                dest_trans.anchor_point.value = [x, y]
                dest_trans.rotation.value = ang
            elif name == "skewX":
                dest_trans.skew.value = -params[0]
                dest_trans.skew_axis.value = 0
            elif name == "skewY":
                dest_trans.skew.value = params[0]
                dest_trans.skew_axis.value = 90
            elif name == "matrix":
                dest_trans.position.value = params[-2:]
                v1 = NVector(*params[0:2])
                v2 = NVector(*params[2:4])
                dest_trans.scale.value = [v1.length * 100, v2.length * 100]
                v1 /= v1.length
                #v2 /= v2.length
                angle = math.atan2(v1[1], v1[0])
                #angle1 = math.atan2(v2[1], v2[0])
                dest_trans.rotation.value = angle / math.pi * 180

    def parse_style(self, element):
        style = {}
        for att in css_atrrs & set(element.attrib.keys()):
            if att in element.attrib:
                style[att] = element.attrib[att]
        if "style" in element.attrib:
            style.update(**dict(map(
                lambda x: map(lambda y: y.strip(), x.split(":")),
                element.attrib["style"].split(";")
            )))
        return style

    def apply_common_style(self, style, transform):
        opacity = float(style.get("opacity", 1))
        if style.get("display", "inline") == "none":
            opacity = 0
        if style.get("visibility", "visible") == "hidden":
            opacity = 0
        transform.opacity.value = opacity * 100

    def add_shapes(self, element, shapes, shape_parent):
        # TODO inherit style
        style = self.parse_style(element)

        group = objects.Group()
        self.apply_common_style(style, group.transform)
        group.name = self._get_id(element)

        shape_parent.shapes.insert(0, group)
        for shape in shapes:
            group.add_shape(shape)

        stroke_color = style.get("stroke", "none")
        if stroke_color not in nocolor:
            if stroke_color.startswith("url"):
                stroke = self.get_color_url(stroke_color, objects.GradientStroke, group)
            else:
                stroke = objects.Stroke()
                color = self.parse_color(stroke_color)
                stroke.color.value = color[:3]
                stroke.opacity.value = color[3] * 100
            group.add_shape(stroke)
            stroke.width.value = float(style.get("stroke-width", 1))
            linecap = style.get("stroke-linecap")
            if linecap == "round":
                stroke.line_cap = objects.shapes.LineCap.Round
            elif linecap == "butt":
                stroke.line_cap = objects.shapes.LineCap.Butt
            elif linecap == "square":
                stroke.line_cap = objects.shapes.LineCap.Square
            linejoin = style.get("stroke-linejoin")
            if linejoin == "round":
                stroke.line_cap = objects.shapes.LineJoin.Round
            elif linejoin == "bevel":
                stroke.line_cap = objects.shapes.LineJoin.Bevel
            elif linejoin in {"miter", "arcs", "miter-clip"}:
                stroke.line_cap = objects.shapes.LineJoin.Miter
            stroke.miter_limit = float(style.get("stroke-miterlimit", 0))

        fill_color = style.get("fill", "inherit")
        if fill_color not in nocolor:
            if fill_color.startswith("url"):
                fill = self.get_color_url(fill_color, objects.GradientFill, group)
            else:
                color = self.parse_color(fill_color)
                fill = objects.Fill(color[:3])
                fill.opacity.value = color[3] * 100
            group.add_shape(fill)

        self.parse_transform(element, group, group.transform)

        return group

    def _parseshape_g(self, element, shape_parent):
        group = objects.Group()
        shape_parent.shapes.insert(0, group)
        style = self.parse_style(element)
        self.apply_common_style(style, group.transform)
        group.name = self._get_name(element, self.qualified("inkscape", "label"))
        self.parse_children(element, group)
        self.parse_transform(element, group, group.transform)

    def _parseshape_ellipse(self, element, shape_parent):
        ellipse = objects.Ellipse()
        ellipse.position.value = [
            float(element.attrib["cx"]),
            float(element.attrib["cy"])
        ]
        ellipse.size.value = [
            float(element.attrib["rx"]) * 2,
            float(element.attrib["ry"]) * 2
        ]
        self.add_shapes(element, [ellipse], shape_parent)

    def _parseshape_circle(self, element, shape_parent):
        ellipse = objects.Ellipse()
        ellipse.position.value = [
            float(element.attrib["cx"]),
            float(element.attrib["cy"])
        ]
        r = float(element.attrib["r"]) * 2
        ellipse.size.value = [r, r]
        self.add_shapes(element, [ellipse], shape_parent)

    def _parseshape_rect(self, element, shape_parent):
        rect = objects.Rect()
        w = float(element.attrib["width"])
        h = float(element.attrib["height"])
        rect.position.value = [
            float(element.attrib["x"]) + w / 2,
            float(element.attrib["y"]) + h / 2
        ]
        rect.size.value = [w, h]
        rx = float(element.attrib.get("rx", 0))
        ry = float(element.attrib.get("ry", 0))
        rect.rounded.value = (rx + ry) / 2
        self.add_shapes(element, [rect], shape_parent)

    def _parseshape_line(self, element, shape_parent):
        line = objects.Shape()
        line.vertices.value.add_point([
            float(element.attrib["x1"]),
            float(element.attrib["y1"])
        ])
        line.vertices.value.add_point([
            float(element.attrib["x2"]) * 2,
            float(element.attrib["y2"]) * 2
        ])
        self.add_shapes(element, [line], shape_parent)

    def _handle_poly(self, element):
        line = objects.Shape()
        coords = list(map(float, element.attrib["points"].replace(",", " ").split()))
        for i in range(0, len(coords), 2):
            line.vertices.value.add_point(coords[i:i+2])
        return line

    def _parseshape_polyline(self, element, shape_parent):
        line = self._handle_poly(element)
        self.add_shapes(element, [line], shape_parent)

    def _parseshape_polygon(self, element, shape_parent):
        line = self._handle_poly(element)
        line.vertices.value.close()
        self.add_shapes(element, [line], shape_parent)

    def _parseshape_path(self, element, shape_parent):
        d_parser = PathDParser(element.attrib.get("d", ""))
        d_parser.parse()
        paths = []
        for path in d_parser.paths:
            p = objects.Shape()
            p.vertices.value = path
            paths.append(p)
        #if len(d_parser.paths) > 1:
            #paths.append(objects.shapes.Merge())
        self.add_shapes(element, paths, shape_parent)

    def parse_children(self, element, shape_parent, limit=None):
        for child in element:
            tag = self.unqualified(child.tag)
            if limit and tag not in limit:
                continue
            handler = getattr(self, "_parseshape_" + tag, None)
            if handler:
                handler(child, shape_parent)
            else:
                handler = getattr(self, "_parse_" + tag, None)
                if handler:
                    handler(child)

    def parse_etree(self, etree, *args, **kwargs):
        animation = objects.Animation(*args, **kwargs)
        svg = etree.getroot()
        if "width" in svg.attrib and "height" in svg.attrib:
            animation.width = int(svg.attrib["width"])
            animation.height = int(svg.attrib["height"])
        else:
            _, _, animation.width, animation.height = map(int, svg.attrib["viewBox"].split(" "))
        animation.name = self._get_name(svg, self.qualified("sodipodi", "docname"))
        layer = objects.ShapeLayer()
        animation.add_layer(layer)
        self.parse_children(svg, layer)
        return animation

    def _parse_defs(self, element):
        self.parse_children(element, None, {"linearGradient"})

    def _parse_linearGradient(self, element):
        id = element.attrib["id"]
        grad = SvgLinearGradient()
        relunits = element.attrib.get("gradientUnits", "") != "userSpaceOnUse"
        grad.x1.parse(element.attrib.get("x1", None), relunits)
        grad.y1.parse(element.attrib.get("y1", None), relunits)
        grad.x2.parse(element.attrib.get("x2", None), relunits)
        grad.y2.parse(element.attrib.get("y2", None), relunits)
        for stop in element.findall("./%s" % self.qualified("svg", "stop")):
            off = float(stop.attrib["offset"].strip("%")) / 100
            grad.add_color(off, self.parse_color(stop.attrib["stop-color"]))
        self.gradients[id] = grad

    def get_color_url(self, color, gradientclass, shape):
        match = re.match(r"url\(#([^)]+)\)", color)
        if not match:
            return None
        id = match[1]
        if id not in self.gradients:
            return None
        grad = self.gradients[id]
        outgrad = gradientclass()
        grad.to_lottie(outgrad, shape)
        if self.name_mode != NameMode.NoName:
            grad.name = id
        return outgrad


class PathDParser:
    def __init__(self, d_string):
        self.path = objects.properties.Bezier()
        self.paths = []
        self.p = NVector(0, 0)
        self.la = None
        self.la_type = None
        self.tokens = list(map(self.d_subsplit, re.findall("[a-zA-Z]|[-+.0-9eE,]+", d_string)))
        self.add_p = True
        self.implicit = "M"

    def d_subsplit(self, tok):
        if tok.isalpha():
            return tok
        if "," in tok:
            return NVector(*map(float, tok.split(",")))
        return float(tok)

    def next_token(self):
        if self.tokens:
            self.la = self.tokens.pop(0)
            if isinstance(self.la, str):
                self.la_type = 0
            elif isinstance(self.la, NVector):
                self.la_type = 2
            else:
                self.la_type = 1
        else:
            self.la = None
        return self.la

    def parse(self):
        self.next_token()
        while self.la:
            if self.la_type == 0:
                parser = "_parse_" + self.la
                self.next_token()
                getattr(self, parser)()
            else:
                parser = "_parse_" + self.implicit
                getattr(self, parser)()

    def _push_path(self):
        self.path = objects.properties.Bezier()

    def _parse_M(self):
        if self.la_type != 2:
            self.next_token()
            return
        self.p = self.la
        self.implicit = "L"
        if not self.add_p:
            self._push_path()
        self.add_p = True
        self.next_token()

    def _parse_m(self):
        if self.la_type != 2:
            self.next_token()
            return
        self.p += self.la
        self.implicit = "l"
        if not self.add_p:
            self._push_path()
        self.add_p = True
        self.next_token()

    def _rpoint(self, point, rel=None):
        return (point - (rel or self.p)).to_list() if point is not None else [0, 0]

    def _do_add_p(self, outp=None):
        if self.add_p:
            self.paths.append(self.path)
            self.path.add_point(self.p.to_list(), [0, 0], self._rpoint(outp))
            self.add_p = False
        elif outp:
            rp = NVector(*self.path.vertices[-1])
            self.path.out_point[-1] = self._rpoint(outp, rp)

    def _parse_L(self):
        if self.la_type != 2:
            self.next_token()
            return
        self._do_add_p()
        self.p = self.la
        self.path.add_point(self.p.to_list(), NVector(0, 0), NVector(0, 0))
        self.implicit = "L"
        self.next_token()

    def _parse_l(self):
        if self.la_type != 2:
            self.next_token()
            return
        self._do_add_p()
        self.p += self.la
        self.path.add_point(self.p.to_list(), [0, 0], [0, 0])
        self.implicit = "l"
        self.next_token()

    def _parse_H(self):
        if self.la_type != 1:
            self.next_token()
            return
        self._do_add_p()
        self.p[0] = self.la
        self.path.add_point(self.p.to_list(), [0, 0], [0, 0])
        self.implicit = "H"
        self.next_token()

    def _parse_h(self):
        if self.la_type != 1:
            self.next_token()
            return
        self._do_add_p()
        self.p[0] += self.la
        self.path.add_point(self.p.to_list(), [0, 0], [0, 0])
        self.implicit = "h"
        self.next_token()

    def _parse_V(self):
        if self.la_type != 1:
            self.next_token()
            return
        self._do_add_p()
        self.p[1] = self.la
        self.path.add_point(self.p.to_list(), [0, 0], [0, 0])
        self.implicit = "V"
        self.next_token()

    def _parse_v(self):
        if self.la_type != 1:
            self.next_token()
            return
        self._do_add_p()
        self.p[1] += self.la
        self.path.add_point(self.p.to_list(), [0, 0], [0, 0])
        self.implicit = "v"
        self.next_token()

    def _parse_C(self):
        if self.la_type != 2:
            self.next_token()
            return
        pout = self.la
        self._do_add_p(pout)
        pin = self.next_token()
        self.p = self.next_token()
        self.path.add_point(
            self.p.to_list(),
            (pin - self.p).to_list(),
            [0, 0]
        )
        self.implicit = "C"
        self.next_token()

    def _parse_c(self):
        if self.la_type != 2:
            self.next_token()
            return
        pout = self.p + self.la
        self._do_add_p(pout)
        pin = self.p + self.next_token()
        self.p += self.next_token()
        self.path.add_point(
            self.p.to_list(),
            (pin - self.p).to_list(),
            [0, 0]
        )
        self.implicit = "c"
        self.next_token()

    def _parse_S(self):
        if self.la_type != 2:
            self.next_token()
            return
        pin = self.la
        self._do_add_p()
        handle = NVector(*self.path.in_point[-1])
        self.path.out_point[-1] = (-handle).to_list()
        self.p = self.next_token()
        self.path.add_point(
            self.p.to_list(),
            (pin - self.p).to_list(),
            [0, 0]
        )
        self.implicit = "S"
        self.next_token()

    def _parse_s(self):
        if self.la_type != 2:
            self.next_token()
            return
        pin = self.la + self.p
        self._do_add_p()
        handle = NVector(*self.path.in_point[-1])
        self.path.out_point[-1] = (-handle).to_list()
        self.p += self.next_token()
        self.path.add_point(
            self.p.to_list(),
            (pin - self.p).to_list(),
            [0, 0]
        )
        self.implicit = "s"
        self.next_token()

    def _parse_Q(self):
        if self.la_type != 2:
            self.next_token()
            return
        self._do_add_p()
        pin = self.la
        self.p = self.next_token()
        self.path.add_point(
            self.p.to_list(),
            (pin - self.p).to_list(),
            [0, 0]
        )
        self.implicit = "Q"
        self.next_token()

    def _parse_q(self):
        if self.la_type != 2:
            self.next_token()
            return
        self._do_add_p()
        pin = self.p + self.la
        self.p += self.next_token()
        self.path.add_point(
            self.p.to_list(),
            (pin - self.p).to_list(),
            [0, 0]
        )
        self.implicit = "q"
        self.next_token()

    def _parse_T(self):
        if self.la_type != 2:
            self.next_token()
            return
        self._do_add_p()
        handle = -(NVector(*self.path.in_point[-1]) - self.p) + self.p
        self.p = self.la
        self.path.add_point(
            self.p.to_list(),
            (handle - self.p).to_list(),
            [0, 0]
        )
        self.implicit = "T"
        self.next_token()

    def _parse_t(self):
        if self.la_type != 2:
            self.next_token()
            return
        self._do_add_p()
        handle = -NVector(*self.path.in_point[-1]) + self.p
        self.p += self.la
        self.path.add_point(
            self.p.to_list(),
            (handle - self.p).to_list(),
            [0, 0]
        )
        self.implicit = "t"
        self.next_token()

    def _parse_A(self):
        if self.la_type != 2:
            self.next_token()
            return
        r = self.la
        xrot = self.next_token()
        large = self.next_token()
        sweep = self.next_token()
        dest = self.next_token()
        self._do_arc(r[0], r[1], xrot, large, sweep, dest)
        self.implicit = "A"
        self.next_token()

    def _arc_matrix_mul(self, phi, x, y, sin_mul=1):
        c = math.cos(phi)
        s = math.sin(phi) * sin_mul

        xr = c * x - s * y
        yr = s * x + c * y
        return xr, yr

    def _arc_angle(self, u, v):
        arg = math.acos(max(-1, min(1, u.dot(v) / (u.length * v.length))))
        if u[0] * v[1] - u[1] * v[0] < 0:
            return -arg
        return arg

    def _arc_point(self, c, r, xangle, t):
        return NVector(
            c[0] + r[0] * math.cos(xangle) * math.cos(t) - r[1] * math.sin(xangle) * math.sin(t),
            c[1] + r[0] * math.sin(xangle) * math.cos(t) + r[1] * math.cos(xangle) * math.sin(t)
        )

    def _arc_derivative(self, c, r, xangle, t):
        return NVector(
            -r[0] * math.cos(xangle) * math.sin(t) - r[1] * math.sin(xangle) * math.cos(t),
            -r[0] * math.sin(xangle) * math.sin(t) + r[1] * math.cos(xangle) * math.cos(t)
        )

    def _arc_alpha(self, step):
        return math.sin(step) * (math.sqrt(4+3*math.tan(step/2)**2) - 1) / 3

    def _do_arc(self, rx, ry, xrot, large, sweep, dest):
        self._do_add_p()
        if self.p == dest:
            return
        rx = abs(rx)
        ry = abs(ry)

        if rx == 0 or ry == 0:
            # Straight line
            self.p = dest
            self.path.add_point(
                self.p.to_list(),
                [0, 0],
                [0, 0]
            )
            return

        x1 = self.p[0]
        y1 = self.p[1]
        x2 = dest[0]
        y2 = dest[1]
        phi = math.pi * xrot / 180

        tx = (x1 - x2) / 2
        ty = (y1 - y2) / 2
        x1p, y1p = self._arc_matrix_mul(phi, tx, ty, -1)

        cr = x1p ** 2 / rx**2 + y1p**2 / ry**2
        if cr > 1:
            s = math.sqrt(cr)
            rx *= s
            ry *= s

        dq = rx**2 * y1p**2 + ry**2 * x1p**2
        pq = (rx**2 * ry**2 - dq) / dq
        cpm = math.sqrt(max(0, pq))
        if large == sweep:
            cpm = -cpm
        cp = NVector(cpm * rx * y1p / ry, -cpm * ry * x1p / rx)
        c = NVector(*self._arc_matrix_mul(phi, cp[0], cp[1])) + NVector((x1+x2)/2, (y1+y2)/2)
        theta1 = self._arc_angle(NVector(1, 0), NVector((x1p - cp[0]) / rx, (y1p - cp[1]) / ry))
        deltatheta = self._arc_angle(
            NVector((x1p - cp[0]) / rx, (y1p - cp[1]) / ry),
            NVector((-x1p - cp[0]) / rx, (-y1p - cp[1]) / ry)
        ) % (2*math.pi)

        if not sweep and deltatheta > 0:
            deltatheta -= 2*math.pi
        elif sweep and deltatheta < 0:
            deltatheta += 2*math.pi

        r = NVector(rx, ry)
        angle1 = theta1
        angle_left = deltatheta
        step = math.pi / 2
        sign = -1 if theta1+deltatheta < angle1 else 1

        self._do_add_p()
        # We need to fix the first handle
        firststep = min(angle_left, step) * sign
        alpha = self._arc_alpha(firststep)
        q1 = self._arc_derivative(c, r, phi, angle1) * alpha
        self.path.out_point[-1] = q1.to_list()
        # Then we iterate until the angle has been completed
        while abs(angle_left) > step / 2:
            lstep = min(angle_left, step)
            step_sign = lstep * sign
            angle2 = angle1 + step_sign

            alpha = self._arc_alpha(step_sign)
            p2 = self._arc_point(c, r, phi, angle2)
            q2 = -self._arc_derivative(c, r, phi, angle2) * alpha

            self.path.add_smooth_point(
                p2.to_list(),
                q2.to_list(),
            )
            angle1 = angle2
            angle_left -= lstep

        self.p = dest

    def _parse_a(self):
        if self.la_type != 2:
            self.next_token()
            return
        r = self.la
        xrot = self.next_token()
        large = self.next_token()
        sweep = self.next_token()
        dest = self.p + self.next_token()
        self._do_arc(r[0], r[1], xrot, large, sweep, dest)
        self.implicit = "a"
        self.next_token()

    def _parse_Z(self):
        if self.path.vertices:
            self.p = NVector(*self.path.vertices[0])
        self.path.close()
        self._push_path()

    def _parse_z(self):
        self._parse_Z()


def parse_svg_etree(etree, *args, **kwargs):
    parser = SvgParser()
    return parser.parse_etree(etree, *args, **kwargs)


def parse_svg_file(file, *args, **kwargs):
    return parse_svg_etree(ElementTree.parse(file), *args, **kwargs)
