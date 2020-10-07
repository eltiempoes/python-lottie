import os
import argparse


root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
doxpath = os.path.join(root, "docs", "dox")
doxfile = os.path.join(doxpath, "downloads.dox")

ref = "master"

parser = argparse.ArgumentParser()
parser.add_argument("--version-base")
parser.add_argument("--version-suf")
parser.add_argument("--version")

ns = parser.parse_args()

ctx = {
    "commit": ns.version_suf,
    "fullversion": ns.version,
    "url_base": "https://gitlab.com/mattbas/python-lottie/-/jobs/artifacts/%s/raw/dist" % ref
}


#https://gitlab.com/mattbas/python-lottie/-/jobs/artifacts/master/raw/dist/lottie-synfig-0.4.0+dev891144d.zip?job=build
with open(doxfile, "w") as outf:
    outf.write("""
/**
    \\page downloads Downloads

    Downloads for {fullversion}

    \li <a href="{url_base}/lottie-synfig-{fullversion}.zip?job=build">Synfig Plugin</a>
    \li <a href="{url_base}/lottie-blender-{fullversion}.zip?job=build">Blender Addon</a>
    \li <a href="{url_base}/lottie-inkscape-{fullversion}.zip?job=build">Inkscape Extension</a>
    \li <a href="{url_base}/lottie-{fullversion}.tar.gz?job=build">Python package</a>
*/
""".format(**ctx))
