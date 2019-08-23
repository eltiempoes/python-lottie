import os
import sys
import argparse
import inspect
from ..exporters import exporters
from .stripper import float_strip


def _get_caller():
    return inspect.getmodule(inspect.currentframe().f_back.f_back)


def _get_parser(caller, basename, path, formats, verbosity):
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
        choices=list(sum((e.extensions for e in exporters), [])),
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

    return parser


def get_parser(basename=None, path="/tmp", formats=["html"], verbosity=1):
    caller = _get_caller()
    return _get_parser(caller, basename, path, formats, verbosity)


def run(animation, ns):
    if ns.name == "-" and len(ns.formats) == 1:
        file = sys.stdout.buffer if ns.formats[0] == "tgs" else sys.stdout
        exporter = exporters.get_from_extension(ns.formats[0])
        exporter.export(animation, absname, exporter.argparse_options(ns))
    else:
        for fmt in ns.formats:
            absname = os.path.abspath(os.path.join(ns.path, ns.name + "." + fmt))
            if ns.verbosity:
                print("file://" + absname)
            exporter = exporters.get_from_extension(fmt)
            exporter.export(animation, absname, exporter.argparse_options(ns))


def script_main(animation, basename=None, path="/tmp", formats=["html"], verbosity=1, strip=float_strip):
    """
    Sets up a script to output an animation into various formats
    """
    caller = _get_caller()
    if caller.__name__ == "__main__":
        parser = _get_parser(caller, basename, path, formats, verbosity)
        strip(animation)
        run(animation, parser.parse_args())
