import os
import sys
import argparse
import inspect
from .. import exporters


exporter_map = {
    "tgs": exporters.export_tgs,
    "json": lambda a, f: exporters.export_lottie(a, f, sort_keys=True, indent=4),
    "html": exporters.export_embedded_html,
    "svg": exporters.export_svg,
    "sif": exporters.export_sif,
}

if exporters.has_cairo:
    exporter_map.update({
        "png": exporters.export_png,
        "pdf": exporters.export_pdf,
        "ps": exporters.export_ps,
    })

if exporters.has_gif:
    exporter_map.update({
        "gif": exporters.export_gif
    })


def script_main(animation, basename=None, path="/tmp", formats=["html"], verbosity=1):
    """
    Sets up a script to output an animation into various formats
    """
    caller = inspect.getmodule(inspect.currentframe().f_back)
    if basename is None:
        basename = os.path.splitext(os.path.basename(caller.__file__))[0]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name",
        "-n",
        default=basename,
        help="Output basename",
    )
    parser.add_argument(
        "--path",
        default=path,
        help="Output path",
    )
    parser.add_argument(
        "--formats", "-f",
        nargs="+",
        choices=list(exporter_map.keys()),
        default=formats,
        help="Formates to render",
        metavar="format"
    )
    parser.add_argument(
        "--verbosity", "-v",
        type=int,
        default=int(verbosity)
    )

    if caller.__name__ == "__main__":
        ns = parser.parse_args()
        if ns.name == "-" and len(ns.formats) == 1:
            file = sys.stdout.buffer if ns.formats[0] == "tgs" else sys.stdout
            exporter_map[ns.formats[0]](animation, file)
        else:
            for fmt in ns.formats:
                absname = os.path.abspath(os.path.join(ns.path, ns.name + "." + fmt))
                if ns.verbosity:
                    print("file://" + absname)
                exporter_map[fmt](animation, absname)
