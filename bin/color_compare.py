#!/usr/bin/env python3

import sys
import os
from functools import reduce
import argparse
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.parsers.svg.importer import parse_color
from tgs.parsers.svg.svgdata import color_table
from tgs import NVector
from tgs.utils.color import ColorMode, ManagedColor


class ColorCompare:
    def __init__(self, name):
        self.name = name
        rgb = ManagedColor(*parse_color(name)[:3])
        xyz = rgb.converted(ColorMode.XYZ)
        self.representations = {
            "RGB": rgb,
            "HSV": rgb.converted(ColorMode.HSV),
            "XYZ": xyz,
            "LAB": xyz.converted(ColorMode.LAB),
            "LUV": xyz.converted(ColorMode.LUV),
            "LCH_uv": xyz.converted(ColorMode.LCH_uv),
        }

    def __repr__(self):
        return "<ColorCompare %s>" % self.name

    def dist(self, oth, space):
        return (self.representations[space].vector - oth.representations[space].vector).length

    def rep(self, space):
        return self.representations[space].vector


def table_row(name, items=[""], pad=" "):
    print("|".join([name.ljust(titlepad, pad)]+[item.center(itempad, pad) for item in items])+"|")


def table_sep(length):
    table_row("", [""]*length, "-")


def vfmt(vec):
    return "%6.2f %6.2f %6.2f" % tuple(vec)


spaces = ["RGB", "HSV", "XYZ", "LAB", "LUV", "LCH_uv"]

parser = argparse.ArgumentParser(
    description="Compares colors in different spaces"
)
parser.add_argument(
    "colors",
    help="Colors to inspect (in one of the CSS color formats)",
    nargs="+",
    type=ColorCompare,
)
parser.add_argument(
    "--space", "-s",
    choices=spaces,
    default="LAB",
    help="Color space for the distance"
)


if __name__ == "__main__":
    ns = parser.parse_args()

    namepad = max(len(c.name) for c in ns.colors)
    titlepad = max(namepad, 6)
    itempad = max(namepad, 6*3+2)
    linelen = titlepad + (itempad + 1) * len(ns.colors) + 1

    print("=" * linelen)
    print("Colors".center(linelen))
    print("-" * linelen)
    table_row("Color", (c.name for c in ns.colors))
    table_sep(len(ns.colors))
    for cs in ["RGB", "HSV", "XYZ", "LAB", "LUV", "LCH_uv"]:
        table_row(cs, (vfmt(c.representations[cs].vector) for c in ns.colors))
    table_sep(len(ns.colors))

    print("=" * linelen)
    print("Distances".center(linelen))
    print("-" * linelen)
    table_row("", (c.name for c in ns.colors))
    table_sep(len(ns.colors))

    for color in ns.colors:
        table_row(color.name, ("%10.8f" % color.dist(c2, ns.space) if c2 is not color else "-" for c2 in ns.colors))

    print("=" * linelen)
    print("Nearest CSS Name".center(linelen))
    print("-" * linelen)
    table_row("", (c.name for c in ns.colors))
    table_sep(len(ns.colors))

    csscolors = {
        name: ManagedColor(*vec[:3]).converted(ColorMode[ns.space]).vector
        for name, vec in color_table.items()
    }

    for color in ns.colors:
        color.match, color.match_dist = reduce(
            lambda a, b: a if a[1] <= b[1] else b,
            ((cn, (color.rep(ns.space) - cv).length) for cn, cv in csscolors.items())
        )

    table_row("", (c.match for c in ns.colors))
    table_row("", ("%10.8f" % c.match_dist for c in ns.colors))

    print("=" * linelen)
