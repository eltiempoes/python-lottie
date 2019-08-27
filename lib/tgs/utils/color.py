import enum
import math
import colorsys
from ..nvector import NVector, Color


def from_uint8(r, g, b):
    return Color(r, g, b) / 255


class ColorMode(enum.Enum):
    RGB = enum.auto()
    HSV = enum.auto()
    HSL = enum.auto()
    HCL = enum.auto()


def _rgb_to_hsl(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (h, s, l)


# http://w3.uqo.ca/missaoui/Publications/TRColorSpace.zip
def rgb_to_hcl(r, g, b, gamma=3, y0=100):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    if maxc > 0:
        alpha = 1/y0 * minc / maxc
    else:
        alpha = 0
    q = math.e ** (alpha * gamma)
    h = math.atan2(g - b, r - g)
    if h < 0:
        h += 2*math.pi
    h /= 2*math.pi
    c = q / 3 * (abs(r-g) + abs(g-b) + abs(b-r))
    l = (q * maxc + (q-1) * minc) / 2
    return (h, c, l)


def _clamp(x):
    return max(0, min(1, x))


def hcl_to_rgb(h, c, l, gamma=3, y0=100):
    h *= 2*math.pi

    q = math.e ** ((1 - 2*c / 4*l) * gamma / y0)
    minc = (4*l - 3*c) / (4*q - 2)
    maxc = minc + 3*c / 2*q

    if h <= math.pi * 1 / 3:
        tan = math.tan(3/2*h)
        r = maxc
        b = minc
        g = (r * tan + b) / (1 + tan)
    elif h <= math.pi * 2 / 3:
        tan = math.tan(3/4*(h-math.pi))
        g = maxc
        b = minc
        r = (g * (1+tan) - b) / tan
    elif h <= math.pi * 3 / 3:
        tan = math.tan(3/4*(h-math.pi))
        g = maxc
        r = minc
        b = g * (1+tan) - r * tan
    elif h <= math.pi * 4 / 3:
        tan = math.tan(3/2*(h+math.pi))
        b = maxc
        r = minc
        g = (r * tan + b) / (1 + tan)
    elif h <= math.pi * 5 / 3:
        tan = math.tan(3/4*h)
        b = maxc
        g = minc
        r = (g * (1+tan) - b) / tan
    else:
        tan = math.tan(3/4*h)
        r = maxc
        g = minc
        b = g * (1+tan) - r * tan

    return _clamp(r), _clamp(g), _clamp(b)


colorsys.hsl_to_rgb = lambda h, s, l: colorsys.hls_to_rgb(h, l, s)
colorsys.rgb_to_hsl = _rgb_to_hsl
colorsys.rgb_to_hcl = rgb_to_hcl
colorsys.hcl_to_rgb = hcl_to_rgb


class ManagedColor:
    Mode = ColorMode

    def __init__(self, c1, c2, c3, mode=ColorMode.RGB):
        self.vector = NVector(c1, c2, c3)
        self._mode = mode

    @property
    def mode(self):
        return self._mode

    def _convert(self, v):
        if self._mode == ColorMode.RGB or v == ColorMode.RGB:
            conv = getattr(colorsys, "%s_to_%s" % (self._mode.name.lower(), v.name.lower()))
            self.vector = NVector(*conv(*self.vector))
        elif self._mode == ColorMode.HSV and v == ColorMode.HSL:
            s_hsv = self.vector[1]
            v = self.vector[2]
            l = v - v * s_hsv / 2
            s_hsl = 0 if l in (0, 1) else (v - l) / min(l, 1 - l)
            self.vector[1] = s_hsl
            self.vector[2] = l
        elif self._mode == ColorMode.HSL and v == ColorMode.HSV:
            s_hsl = self.vector[1]
            l = self.vector[2]
            v = l + s_hsl * min(l, 1 - l)
            s_hsv = 0 if v == 0 else 2 - 2 * l / v
            self.vector[1] = s_hsv
            self.vector[2] = v
        else:
            raise ValueError

    def convert(self, v):
        if v == self._mode:
            return self

        self._convert(v)

        self._mode = v
        return self

    def clone(self):
        return ManagedColor(*self.vector, self._mode)

    def converted(self, mode):
        return self.clone().convert(mode)

    def to_color(self):
        return self.converted(ColorMode.RGB).vector

    @classmethod
    def from_color(cls, color):
        return cls(*color[:3], ColorMode.RGB)

    def __repr__(self):
        return "<%s %s [%.3f, %.3f, %.3f]>" % (
            (self.__class__.__name__, self.mode.name) + tuple(self.vector.components)
        )

    def _attrindex(self, name):
        comps = None

        if self._mode == ColorMode.RGB:
            comps = ({"r", "red"}, {"g", "green"}, {"b", "blue"})
        elif self._mode == ColorMode.HSV:
            comps = ({"h", "hue"}, {"s", "saturation"}, {"v", "value"})
        elif self._mode == ColorMode.HSL:
            comps = ({"h", "hue"}, {"s", "saturation"}, {"l", "lightness"})
        elif self._mode == ColorMode.HCL:
            comps = ({"h", "hue"}, {"c", "choma"}, {"l", "luma", "luminance"})

        if comps:
            for i, vals in enumerate(comps):
                if name in vals:
                    return i

        return None

    def __getattr__(self, name):
        if name not in vars(self) and name not in {"_mode", "vector"}:
            i = self._attrindex(name)
            if i is not None:
                return self.vector[i]
        return super().__getattr__(name)

    def __setattr__(self, name, value):
        if name not in vars(self) and name not in {"_mode", "vector"}:
            i = self._attrindex(name)
            if i is not None:
                self.vector[i] = value
                return
        return super().__setattr__(name, value)
