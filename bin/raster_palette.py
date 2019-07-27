#!/usr/bin/env python3

import sys
import os
import argparse
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))

parser = argparse.ArgumentParser(
    description="Shows the palette of a raster image"
)
parser.add_argument(
    "infile",
    help="Input file"
)
parser.add_argument(
    "--colors", "-c",
    default=1,
    type=int,
    help="Number of colors to quantize"
)

if __name__ == "__main__":
    from tgs.parsers.raster import RasterImage
    ns = parser.parse_args()

    raster = RasterImage.open(ns.infile)
    palette = raster.k_means(ns.colors)

    for color in palette:
        print("#%02x%02x%02x %f : %s" % (
            int(round(color[0])),
            int(round(color[1])),
            int(round(color[2])),
            color[3] / 255,
            list(color/255),
        ))
