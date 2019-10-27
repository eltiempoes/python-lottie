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
    parser.add_argument(
        "--layer-frames",
        type=int,
        help="If greater than 0, treats every layer in the SVG as a different animation frame, "
            "greater values increase the time each frames lasts for.",
        default=0
    )
    ns, _ = parser.parse_known_args()
    if ns.tgspath:
        sys.path.append(ns.tgspath)
    import tgs
    animation = tgs.parsers.svg.importer.parse_svg_file(ns.infile, ns.layer_frames, ns.frames, ns.fps)
    if ns.format == "lottie":
        tgs.exporters.export_lottie(animation, sys.stdout, ns.pretty)
    else:
        tgs.exporters.export_tgs(animation, sys.stdout.buffer)
