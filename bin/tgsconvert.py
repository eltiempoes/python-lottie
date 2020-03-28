#!/usr/bin/env python3

import re
import sys
import os
import argparse
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.exporters import exporters
from tgs.importers import importers
from tgs.utils.stripper import float_strip, heavy_strip


desc = """Converts between multiple formats

Supported formats:

- Input:
%s

- Output:
%s
""" % (
    "\n".join("%s- %s" % (" "*2, e.name) for e in importers),
    "\n".join("%s- %s" % (" "*2, e.name) for e in exporters),
)

parser = argparse.ArgumentParser(
    description=desc,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)

group = importers.set_options(parser)
group.add_argument(
    "infile",
    default="-",
    nargs="?",
    help="Input file"
)
group.add_argument(
    "--input-format", "-if",
    default=None,
    choices=[importer.slug for importer in importers],
    help="Explicit output format (if missing implied by the input filename)",
)


group = exporters.set_options(parser)

group.add_argument(
    "outfile",
    default="-",
    nargs="?",
    help="Output file"
)
group.add_argument(
    "--output-format", "-of",
    default=None,
    choices=[exporter.slug for exporter in exporters],
    help="Explicit output format (if missing implied by the output filename)",
)
group.add_argument(
    "--sanitize",
    default=False,
    action="store_true",
    help="Ensure the animation is 512x512 and 30 or 60 fps",
)
group.add_argument(
    "--optimize",
    "-O",
    default=1,
    type=int,
    choices=[0, 1, 2],
    help="Optimize the animation parameter: 0 no optimization, 1 truncate floats, 2 truncate floats and names",
)

if __name__ == "__main__":
    ns = parser.parse_args()

    infile = ns.infile
    importer = None
    if infile == "-":
        infile = sys.stdin
    else:
        suf = os.path.splitext(infile)[1][1:]
        for p in importers:
            if suf in p.extensions:
                importer = p
                break
    if ns.input_format:
        importer = None
        for p in importers:
            if p.slug == ns.input_format:
                importer = p
                break
    if not importer:
        sys.stderr.write("Unknown importer\n")
        sys.exit(1)

    outfile = ns.outfile
    exporter = None
    if outfile == "-":
        outfile = sys.stdout
    else:
        exporter = exporters.get_from_filename(outfile)
    if ns.output_format:
        exporter = exporters.get(ns.output_format)

    if not exporter:
        sys.stderr.write("Unknown exporter\n")
        sys.exit(1)

    i_options = {}
    for opt in importer.extra_options:
        i_options[opt.name] = getattr(ns, opt.nsvar(importer.slug))

    o_options = exporter.argparse_options(ns)

    an = importer.process(infile, **i_options)
    if ns.optimize == 1:
        float_strip(an)
    elif ns.optimize >= 2:
        heavy_strip(an)
    if ns.sanitize:
        an.tgs_sanitize()
    exporter.process(an, outfile, **o_options)
