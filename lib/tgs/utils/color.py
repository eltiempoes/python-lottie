import enum
import colorsys
from ..nvector import NVector, Color


def from_uint8(r, g, b):
    return Color(r, g, b) / 255


class ColorMode(enum.Enum):
    RGB = enum.auto()
    HSV = enum.auto()
    HSL = enum.auto()


def _rgb_to_hsl(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (h, s, l)


colorsys.hsl_to_rgb = lambda h, s, l: colorsys.hls_to_rgb(h, l, s)
colorsys.rgb_to_hsl = _rgb_to_hsl


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
        return "<%s %s %s>" % (self.__class__.__name__, self.mode.name, self.vector.components)

    def _attrindex(self, name):
        if self._mode == ColorMode.RGB:
            if name in {"r", "red"}:
                return 0
            if name in {"g", "green"}:
                return 1
            if name in {"b", "blue"}:
                return 2
        elif self._mode == ColorMode.HSV:
            if name in {"h", "hue"}:
                return 0
            if name in {"s", "saturation"}:
                return 1
            if name in {"v", "value"}:
                return 2
        elif self._mode == ColorMode.HSL:
            if name in {"h", "hue"}:
                return 0
            if name in {"s", "saturation"}:
                return 1
            if name in {"l", "lightness"}:
                return 2
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
