#!/usr/bin/env python3

import os
import sys
import math
import argparse
from PIL import Image
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.utils.color import Color, ColorMode
from lottie.parsers.svg.importer import parse_color


parser = argparse.ArgumentParser(
    description="Visualizes color spaces",
    conflict_handler="resolve",
)
parser.add_argument(
    "--width", "-w",
    default=512,
    type=int,
    help="Width of the output image",
)
parser.add_argument(
    "--height",
    "-h",
    default=512,
    type=int,
    help="Height of the output image",
)

g = parser.add_mutually_exclusive_group()
g.add_argument(
    "--base",
    "-b",
    type=parse_color,
    default=Color(1, 0, 0),
    help="Base color",
)
g.add_argument(
    "--other",
    type=float,
    default=None,
    help="Value of the other component",
)

parser.add_argument(
    "--radial",
    action="store_true",
    help="Whether to draw a circle rather than a square"
)
parser.add_argument(
    "space",
    choices=list(ColorMode.__members__.keys()),
    help="Color space"
)

parser.add_argument(
    "--min",
    "-m",
    default=None,
    type=float,
    help="Minimum value to show for `component`"
)
parser.add_argument(
    "--max",
    "-M",
    default=None,
    type=float,
    help="Maximum value to show for `component`"
)
parser.add_argument("component", help="Component to show")


parser.add_argument(
    "--min2",
    "-m2",
    default=None,
    type=float,
    help="Minimum value to show for `component2`"
)
parser.add_argument(
    "--max2",
    "-M2",
    default=None,
    type=float,
    help="Maximum value to show for `component2`"
)
parser.add_argument("component2", help="Optional secondary component to show")


class CompChanger:
    def __init__(self, min_v, max_v, component, space):
        self.component = component.lower()

        self.min_v = min_v
        if self.min_v is None:
            self.min_v = 0
            if space == ColorMode.LAB or space == ColorMode.LUV:
                self.min_v = -100

        self.max_v = max_v
        if self.max_v is None:
            self.max_v = 1
            if space == ColorMode.LCH_uv and self.component == 'h':
                self.max_v = math.tau
            elif space == ColorMode.LAB or space == ColorMode.LUV:
                self.max_v = 100

    def apply(self, color, factor):
        comp_v = factor * (self.max_v - self.min_v) + self.min_v
        setattr(color, self.component, comp_v)


def color_tuple(color):
    return tuple(int(round(c*255)) for c in color.to_rgb())


if __name__ == "__main__":
    ns = parser.parse_args()

    space = ColorMode[ns.space]
    base_color = ns.base.converted(space)
    width = ns.width
    height = ns.height

    if ns.other is not None and ns.component2:
        comps = base_color.component_names()
        for comp in comps:
            if ns.component.lower() not in comp and ns.component2.lower() not in comp:
                break

        setattr(base_color, list(comp)[0], ns.other)

    comp1 = CompChanger(ns.min, ns.max, ns.component, space)
    comp2 = None
    if ns.component2:
        comp2 = CompChanger(ns.min2, ns.max2, ns.component2, space)

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = img.load()

    for x in range(width):
        ix = x / (width-1)
        sys.stdout.write("\r%d%%" % (ix * 100))

        if not ns.radial:
            color_x = base_color.clone()
            comp1.apply(color_x, ix)
            color_t = color_tuple(color_x)

        for y in range(height):
            iy = y / (height-1)

            if not ns.radial:
                if comp2:
                    color = color_x.clone()
                    comp2.apply(color, iy)
                    color_t = color_tuple(color)
            else:
                xnorm = ix * 2 - 1
                ynorm = iy * 2 - 1
                angle = math.atan2(ynorm, xnorm) % math.tau / math.tau
                distance = math.hypot(xnorm, ynorm)
                if distance > 1:
                    continue

                color = base_color.clone()
                comp1.apply(color, angle)
                if comp2:
                    comp2.apply(color, distance)
                color_t = color_tuple(color)

            pixels[x, y] = color_t

    img.show()
    img.save("/tmp/out.png")

