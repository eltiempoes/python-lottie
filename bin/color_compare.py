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
    choices=spaces+["all"],
    default="LAB",
    help="Color space for the distance"
)
parser.add_argument(
    "--count", "-c",
    type=int,
    default=1,
    help="Number of similar colors to get"
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
        table_sep(len(colors))

        csscolors = {
            name: ManagedColor(*vec[:3]).converted(ColorMode[space]).vector
            for name, vec in color_table.items()
        }

        for color in colors:
            color.matches = sorted(
                ((cn, (color.rep(space) - cv).length) for cn, cv in csscolors.items()),
                key=lambda c: c[1]
            )

        for i in range(similar_count):
            table_row("", (c.matches[i][0] for c in colors))
            table_row("", ("%10.8f" % c.matches[i][1] for c in colors))
            table_sep(len(colors))


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

    if ns.space == "all":
        for space in spaces:
            compare(ns.colors, space, ns.count)
    else:
        compare(ns.colors, ns.space, ns.count)

    print("=" * linelen)
