#!/usr/bin/env python3

import sys
import os
from functools import reduce
import argparse
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.parsers.svg.importer import parse_color
from lottie.parsers.svg.svgdata import color_table
from lottie import NVector
from lottie.utils.color import ColorMode, Color


class ColorCompare:
    def __init__(self, name):
        self.name = name
        rgb = Color(*parse_color(name)[:3])
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
        return (self.representations[space] - oth.representations[space]).length

    def rep(self, space):
        return self.representations[space]

    def ansi_str(self, length):
        return color_str(self.rep("RGB"), length)


class SimilarColor:
    def __init__(self, name, rgbvec, space):
        self.name = name
        self.rgb = Color(*rgbvec[:3])
        self.vec = self.rgb.converted(ColorMode[space])
        self.space = space

    def dist(self, colorcompare):
        return (self.vec - colorcompare.rep(self.space)).length

    def ansi_str(self, length):
        return color_str(self.rgb, length)


def color_str(rgbvec, length):
    comps = [
        str(int(round(c * 255)))
        for c in rgbvec[:3]
    ]
    return "\x1b[48;2;%sm%s\x1b[m" % (";".join(comps), " " * length)


def table_row(name, items=[""], pad=" "):
    print("|".join([name.ljust(titlepad, pad)]+[item.center(itempad, pad) for item in items])+"|")


def table_sep(length):
    table_row("", [""]*length, "-")


def vfmt(vec):
    return "%6.2f %6.2f %6.2f" % tuple(vec[:3])


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
    choices=spaces+["all"],
    default="LCH_uv",
    help="Color space for the distance"
)
parser.add_argument(
    "--count", "-c",
    type=int,
    default=1,
    help="Number of similar colors to get"
)
parser.add_argument(
    "--colors",
    action="store_true",
    default=os.environ.get("COLORTERM", "") in {"truecolor", "24bit"},
    dest="term_colors",
    help="Enables color previews",
)
parser.add_argument(
    "--no-colors",
    action="store_false",
    dest="term_colors",
    help="Disables color previews",
)


def compare(colors, space, similar_count):
    print("=" * linelen)
    print(("Distances [%s]" % space).center(linelen))
    print("-" * linelen)
    table_row("", (c.name for c in colors))
    table_sep(len(colors))

    for color in colors:
        table_row(color.name, ("%10.8f" % color.dist(c2, space) if c2 is not color else "-" for c2 in colors))

    if similar_count:
        print("=" * linelen)
        print(("Nearest CSS Name [%s]" % space).center(linelen))
        print("-" * linelen)
        table_row(space, (c.name for c in colors))
        if term_colors:
            table_row("", (c.ansi_str(itempad) for c in colors))
        table_sep(len(colors))

        csscolors = [
            SimilarColor(name, vec, space)
            for name, vec in color_table.items()
        ]

        for color in colors:
            color.matches = sorted(
                ((c, c.dist(color)) for c in csscolors),
                key=lambda c: c[1]
            )

        for i in range(similar_count):
            table_row("", (c.matches[i][0].name for c in colors))
            if term_colors:
                table_row("", (c.matches[i][0].ansi_str(itempad) for c in colors))
            table_row("", ("%10.8f" % c.matches[i][1] for c in colors))
            table_sep(len(colors))


if __name__ == "__main__":
    ns = parser.parse_args()

    namepad = max(len(c.name) for c in ns.colors)
    titlepad = max(namepad, 6)
    itempad = max(namepad, 6*3+2)
    linelen = titlepad + (itempad + 1) * len(ns.colors) + 1
    term_colors = ns.term_colors

    print("=" * linelen)
    print("Colors".center(linelen))
    print("-" * linelen)
    table_row("Color", (c.name for c in ns.colors))
    if term_colors:
        table_row("", (c.ansi_str(itempad) for c in ns.colors))
    table_sep(len(ns.colors))
    for cs in ["RGB", "HSV", "XYZ", "LAB", "LUV", "LCH_uv"]:
        table_row(cs, (vfmt(c.representations[cs]) for c in ns.colors))
    table_sep(len(ns.colors))

    if ns.space == "all":
        for space in spaces:
            compare(ns.colors, space, ns.count)
    else:
        compare(ns.colors, ns.space, ns.count)

    print("=" * linelen)
