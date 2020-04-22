import sys
import argparse


if __name__ == "__main__":

    if sys.version_info.major < 3:
        import subprocess
        sys.exit(subprocess.call(["python3"] + sys.argv))

    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument(
        "--frame",
        type=int,
        help="Frame to load",
        default=0
    )
    parser.add_argument(
        "--lottiepath",
        help="Additional path to add to sys.path",
        default=""
    )
    ns, _ = parser.parse_known_args()
    if ns.lottiepath:
        sys.path.insert(0, ns.lottiepath)
    import lottie
    animation = lottie.parsers.tgs.parse_tgs(ns.file)
    lottie.exporters.export_svg(animation, sys.stdout, ns.frame, True)
