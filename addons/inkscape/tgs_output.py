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
        "--lottiepath",
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
    if ns.lottiepath:
        sys.path.insert(0, ns.lottiepath)
    import lottie
    animation = lottie.parsers.svg.importer.parse_svg_file(ns.infile, ns.layer_frames, ns.frames, ns.fps)
    if ns.format == "lottie":
        lottie.exporters.export_lottie(animation, sys.stdout, ns.pretty)
    else:
        lottie.exporters.export_tgs(animation, sys.stdout.buffer)
