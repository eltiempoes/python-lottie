import sys
import argparse
from distutils.util import strtobool


if __name__ == "__main__":
    if sys.version_info.major < 3:
        import subprocess
        sys.exit(subprocess.call(["python3"] + sys.argv))

    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument(
        "--fps",
        type=int,
        help="Frames per second",
        default=60
    )
    parser.add_argument(
        "--frames",
        type=int,
        help="Number of frames",
        default=60
    )
    parser.add_argument(
        "--format",
        choices=["tgs", "lottie"],
        help="Output format",
        default="tgs"
    )
    parser.add_argument(
        "--pretty",
        type=strtobool,
        help="Pretty print JSON",
        default=1
    )
    parser.add_argument(
        "--tgspath",
        help="Additional path to add to sys.path",
        default=""
    )
    ns, _ = parser.parse_known_args()
    if ns.tgspath:
        sys.path.append(ns.tgspath)
    import tgs
    animation = tgs.parsers.svg.importer.parse_svg_file(ns.infile, ns.frames, ns.fps)
    if ns.format == "lottie":
        kw = {}
        if ns.pretty:
            kw.update(sort_keys=True, indent=4)
        tgs.exporters.export_lottie(animation, sys.stdout, **kw)
    else:
        tgs.exporters.export_tgs(animation, sys.stdout.buffer)
