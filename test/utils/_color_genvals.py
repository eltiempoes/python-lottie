import sys
from tgs.utils.color import ColorMode, ManagedColor

colors = {
    "RGB": [
        ManagedColor(1, 0, 0, ColorMode.RGB),
        ManagedColor(0, 1, 0, ColorMode.RGB),
        ManagedColor(0, 0, 1, ColorMode.RGB),
        ManagedColor(1, 1, 1, ColorMode.RGB),
        ManagedColor(0, 0, 0, ColorMode.RGB),
    ],
    "HSV": [
        ManagedColor(1/3, 1, 1, ColorMode.HSV),
        ManagedColor(0, 1, 1, ColorMode.HSV),
        ManagedColor(0, 0, 0, ColorMode.HSV),
        ManagedColor(0.5, 0, 1, ColorMode.HSV),
        ManagedColor(0.5, 1, 1, ColorMode.HSV),
        ManagedColor(0.5, 0, 0, ColorMode.HSV),
    ],
    "HSL": [
        ManagedColor(1/3, 1, .5, ColorMode.HSL),
        ManagedColor(0, 1, .5, ColorMode.HSL),
        ManagedColor(0, 1, 1, ColorMode.HSL),
        ManagedColor(0, 0, 0, ColorMode.HSL),
        ManagedColor(0.5, 1, 1, ColorMode.HSL),
        ManagedColor(0.5, 0, 1, ColorMode.HSL),
        ManagedColor(0.5, 0, 0, ColorMode.HSL),
    ],
    "XYZ": [
        ManagedColor(0.95047, 1, 1.08883, ColorMode.XYZ),
        ManagedColor(0, 0, 0, ColorMode.XYZ),
        ManagedColor(0.4124564, 0.2126729, 0.0193339, ColorMode.XYZ),
        ManagedColor(0.2687201, 0.1176957, 0.9544423, ColorMode.XYZ),
        ManagedColor(0.25, 0.40, 0.10, ColorMode.XYZ),
    ],
}

from_mode = sys.argv[1].upper()
to_name = sys.argv[2].upper()
mode = getattr(ColorMode, to_name)

print("")
print("    def test_to_%s(self):" % mode.name.lower())
print("        mode = %s" % mode)
for color in colors[from_mode]:
    print("        self.assert_convert(%s, %s, mode)" % (
        tuple(color.vector),
        tuple(color.converted(mode).vector),
    ))
