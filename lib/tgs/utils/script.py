import os
import sys
import argparse
import inspect
from ..exporters import exporters


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
        choices=list(exporters.keys()),
        default=formats,
        help="Formates to render",
        metavar="format"
    )
    parser.add_argument(
        "--verbosity", "-v",
        type=int,
        default=int(verbosity)
    )

    exporters.set_options(parser)

    if caller.__name__ == "__main__":
        ns = parser.parse_args()
        if ns.name == "-" and len(ns.formats) == 1:
            file = sys.stdout.buffer if ns.formats[0] == "tgs" else sys.stdout
            exporter = exporters[ns.formats[0]]
            exporter.export(animation, absname, exporter.argparse_options(ns))
        else:
            for fmt in ns.formats:
                absname = os.path.abspath(os.path.join(ns.path, ns.name + "." + fmt))
                if ns.verbosity:
                    print("file://" + absname)
                exporter = exporters[fmt]
                exporter.export(animation, absname, exporter.argparse_options(ns))
