import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lottie
from lottie.exporters.tgs_validator import TgsValidator, Severity


parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument("outfile", nargs="?")

ns = parser.parse_args()

importer = lottie.importers.importers.get_from_filename(ns.infile)

animation = importer.process(ns.infile)

outfile = ns.outfile or ns.infile+".tgs"

exporter = lottie.exporters.exporters.get_from_filename(outfile)

if exporter.slug == "tgs":
    validator = TgsValidator(Severity.Error)
    validator(animation)
    if validator.errors:
        sys.stderr.write("Could not export TGS:\n")
        sys.stderr.write("\n".join(map(str, validator.errors))+"\n")
        sys.exit(1)

exporter.process(animation, outfile)
