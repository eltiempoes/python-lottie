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
    XYZ = enum.auto()


def _clamp(x):
    return max(0, min(1, x))


class Conversion:
    _conv_paths = {
        (ColorMode.RGB, ColorMode.RGB): [],
        (ColorMode.RGB, ColorMode.HSV): [],
        (ColorMode.RGB, ColorMode.HSL): [],
        (ColorMode.RGB, ColorMode.HCL): [],
        (ColorMode.RGB, ColorMode.XYZ): [],

        (ColorMode.HSV, ColorMode.RGB): [],
        (ColorMode.HSV, ColorMode.HSV): [],
        (ColorMode.HSV, ColorMode.HSL): [],
        (ColorMode.HSV, ColorMode.HCL): [ColorMode.RGB],
        (ColorMode.HSV, ColorMode.XYZ): [ColorMode.RGB],

        (ColorMode.HSL, ColorMode.RGB): [],
        (ColorMode.HSL, ColorMode.HSV): [],
        (ColorMode.HSL, ColorMode.HSL): [],
        (ColorMode.HSL, ColorMode.HCL): [ColorMode.RGB],
        (ColorMode.HSL, ColorMode.XYZ): [ColorMode.RGB],

        (ColorMode.HCL, ColorMode.RGB): [],
        (ColorMode.HCL, ColorMode.HSV): [ColorMode.RGB],
        (ColorMode.HCL, ColorMode.HSL): [ColorMode.RGB],
        (ColorMode.HCL, ColorMode.HCL): [],
        (ColorMode.HCL, ColorMode.XYZ): [ColorMode.RGB],

        (ColorMode.XYZ, ColorMode.RGB): [],
        (ColorMode.XYZ, ColorMode.HSV): [ColorMode.RGB],
        (ColorMode.XYZ, ColorMode.HSL): [ColorMode.RGB],
        (ColorMode.XYZ, ColorMode.HCL): [ColorMode.RGB],
        (ColorMode.XYZ, ColorMode.XYZ): [],
    }

    @staticmethod
    def rgb_to_hsv(r, g, b):
        return colorsys.rgb_to_hsv(r, g, b)

    @staticmethod
    def hsv_to_rgb(r, g, b):
        return colorsys.hsv_to_rgb(r, g, b)

    @staticmethod
    def hsl_to_hsv(h, s_hsl, l):
        v = l + s_hsl * min(l, 1 - l)
        s_hsv = 0 if v == 0 else 2 - 2 * l / v
        return (h, s_hsv, v)

    @staticmethod
    def hsv_to_hsl(h, s_hsv, v):
        l = v - v * s_hsv / 2
        s_hsl = 0 if l in (0, 1) else (v - l) / min(l, 1 - l)
        return (h, s_hsl, l)

    @staticmethod
    def rgb_to_hsl(r, g, b):
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return (h, s, l)

    @staticmethod
    def hsl_to_rgb(h, s, l):
        return colorsys.hls_to_rgb(h, l, s)

    # http://w3.uqo.ca/missaoui/Publications/TRColorSpace.zip
    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def rgb_to_xyz(r, g, b):
        def _gamma(v):
            return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
        rgb = (_gamma(r), _gamma(g), _gamma(b))
        matrix = [
            [0.4124564, 0.3575761, 0.1804375],
            [0.2126729, 0.7151522, 0.0721750],
            [0.0193339, 0.1191920, 0.9503041],
        ]
        return tuple(
            sum(rgb[i] * c for i, c in enumerate(row))
            for row in matrix
        )

    @staticmethod
    def xyz_to_rgb(x, y, z):
        def _gamma1(v):
            return v * 12.92 if v <= 0.0031308 else v ** (1/2.4) * 1.055 - 0.055
        matrix = [
            [+3.2404542, -1.5371385, -0.4985314],
            [-0.9692660, +1.8760108, +0.0415560],
            [+0.0556434, -0.2040259, +1.0572252],
        ]
        xyz = (x, y, z)
        return tuple(map(_gamma1, (
            sum(xyz[i] * c for i, c in enumerate(row))
            for row in matrix
        )))

    @staticmethod
    def conv_func(mode_from, mode_to):
        return getattr(Conversion, "%s_to_%s" % (mode_from.name.lower(), mode_to.name.lower()), None)

    @staticmethod
    def convert(tuple, mode_from, mode_to):
        if mode_from == mode_to:
            return tuple

        func = Conversion.conv_func(mode_from, mode_to)
        if func:
            return func(*tuple)

        if (mode_from, mode_to) in Conversion._conv_paths:
            steps = Conversion._conv_paths[(mode_from, mode_to)] + [mode_to]
            for step in steps:
                tuple = Conversion.conv_func(mode_from, step)(*tuple)
                mode_from = step
            return tuple

        raise ValueError("No conversion path from %s to %s" % (mode_from, mode_to))


class ManagedColor:
    Mode = ColorMode

    def __init__(self, c1, c2, c3, mode=ColorMode.RGB):
        self.vector = NVector(c1, c2, c3)
        self._mode = mode

    @property
    def mode(self):
        return self._mode

    def convert(self, v):
        if v == self._mode:
            return self

        self.vector = NVector(*Conversion.convert(self.vector, self._mode, v))

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
        elif self._mode == ColorMode.XYZ:
            comps = "xyz"

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
