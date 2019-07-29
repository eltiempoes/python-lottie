#!/usr/bin/env python3

import re
import sys
import os
import argparse
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
import tgs.exporters
from tgs import parsers
from tgs.parsers.svg.importer import parse_color
try:
    import tgs.parsers.raster
    raster = True
except ImportError:
    raster = False


class Exporter:
    def __init__(self, name, extensions, callback, extra_options=[], pretty_options={}, slug=None):
        self.name = name
        self.extensions = extensions
        self.callback = callback
        self.extra_options = extra_options
        self.pretty_options = pretty_options
        self.slug = slug if slug is not None else extensions[0]

    def export(self, animation, filename, options, pretty):
        kw = options
        if pretty:
            kw.update(self.pretty_options)
        self.callback(animation, filename, **kw)


class ExtraOption:
    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs

    def add_argument(self, slug, parser):
        opt = "--%s-%s" % (slug, self.name.replace("_", "-"))
        parser.add_argument(opt, metavar=self.name, **self.kwargs)

    def nsvar(self, slug):
        return "%s_%s" % (slug, self.name)


class Importer:
    def __init__(self, name, extensions, callback, extra_options=[], slug=None):
        self.name = name
        self.extensions = extensions
        self.callback = callback
        self.extra_options = extra_options
        self.slug = slug if slug is not None else extensions[0]

    def load(self, stream, extra_options):
        return self.callback(stream, **extra_options)


def add_options(parser, ie, object):
    if not object.extra_options:
        return

    suf = " %sing options" % ie
    group = parser.add_argument_group(object.name + suf)
    for op in object.extra_options:
        op.add_argument(object.slug, group)


exporters = [
    Exporter("Telegram Animated Sticker", ["tgs"], tgs.exporters.export_tgs),
    Exporter("Lottie JSON", ["json"], tgs.exporters.export_lottie, [], dict(sort_keys=True, indent=4), "lottie"),
    Exporter("Lottie HTML", ["html", "htm"], tgs.exporters.export_embedded_html),
    Exporter("SVG", ["svg"], tgs.exporters.export_svg, [
        ExtraOption("frame", type=int, default=0, help="Frame to extract")
    ], {"pretty": True}),
    Exporter("Synfig", ["sif"], tgs.exporters.export_sif, [], {"pretty": True}),
]
if tgs.exporters.has_cairo:
    exporters += [
        Exporter("PNG", ["png"], tgs.exporters.export_png, [
            ExtraOption("dpi", type=int, default=96, help="Dots per inch"),
            ExtraOption("frame", type=int, default=0, help="Frame to extract"),
        ]),
        Exporter("PDF", ["pdf"], tgs.exporters.export_pdf, [
            ExtraOption("dpi", type=int, default=96, help="Dots per inch"),
            ExtraOption("frame", type=int, default=0, help="Frame to extract"),
        ]),
        Exporter("PostScript", ["ps"], tgs.exporters.export_ps, [
            ExtraOption("dpi", type=int, default=96, help="Dots per inch"),
            ExtraOption("frame", type=int, default=0, help="Frame to extract"),
        ]),
    ]
if tgs.exporters.has_gif:
    exporters += [
        Exporter("GIF", ["gif"], tgs.exporters.export_png, [
            ExtraOption("dpi", type=int, default=96, help="Dots per inch"),
            ExtraOption("skip_frames", type=int, default=5, help="Only renderer 1 out of these many frames"),
        ]),
    ]


importers = [
    Importer("SVG", ["svg"], parsers.svg.parse_svg_file, [
        ExtraOption("n_frames", type=int, default=60),
        ExtraOption("framerate", type=int, default=60),
    ]),
    Importer("Lottie JSON / Telegram Sticker", ["json", "tgs"], parsers.tgs.parse_tgs, [], "lottie"),
]
if raster:
    importers.append(
        Importer("Raster image", ["bmp", "png", "gif"], tgs.parsers.raster.raster_to_animation, [
            ExtraOption("n_colors", type=int, default=1, help="Number of colors to quantize"),
            ExtraOption("palette", type=parse_color, default=[], nargs="+", help="Custom palette"),
            # TODO color mode
        ])
    )


desc = """Converts between multiple formats

Supported formats:

- Input:
%s

- Output:
%s
""" % (
    "\n".join("%s- %s" % (" "*2, e.name) for e in exporters),
    "\n".join("%s- %s" % (" "*2, e.name) for e in importers)
)

parser = argparse.ArgumentParser(
    description=desc,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)

group = parser.add_argument_group("Generic input options")
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


group = parser.add_argument_group("Generic output options")

group.add_argument(
    "outfile",
    default="-",
    nargs="?",
    help="Output file"
)
group.add_argument(
    "--pretty", "-p",
    action="store_true",
    help="Pretty print (for formats that support it)",
)
group.add_argument(
    "--output-format", "-of",
    default=None,
    choices=[exporter.slug for exporter in exporters],
    help="Explicit output format (if missing implied by the output filename)",
)

for exporter in exporters:
    add_options(parser, "export", exporter)

for importer in importers:
    add_options(parser, "import", importer)

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
        suf = os.path.splitext(outfile)[1][1:]
        for p in exporters:
            if suf in p.extensions:
                exporter = p
                break
    if ns.output_format:
        exporter = None
        for p in exporters:
            if p.slug == ns.output_format:
                exporter = p
                break
    if not exporter:
        sys.stderr.write("Unknown exporter\n")
        sys.exit(1)

    i_options = {}
    for opt in importer.extra_options:
        i_options[opt.name] = getattr(ns, opt.nsvar(importer.slug))

    o_options = {}
    for opt in exporter.extra_options:
        o_options[opt.name] = getattr(ns, opt.nsvar(exporter.slug))

    an = importer.load(infile, i_options)
    exporter.export(an, outfile, o_options, ns.pretty)
