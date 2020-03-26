import os
import sys
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tgs
from tgs.exporters.tgs_validator import TgsValidator, Severity


parser = argparse.ArgumentParser()
parser.add_argument("infile")

ns = parser.parse_args()

with open(ns.infile) as sif_file:
    animation = tgs.parsers.sif.parse_sif_file(sif_file)


validator = TgsValidator(Severity.Error)
validator(animation)
if validator.errors:
    raise Exception("\n".join(map(str, validator.errors))+"\n")


with open(os.path.splitext(ns.infile)[0]+".tgs", "wb") as tgs_file:
    tgs.exporters.core.export_tgs(animation, tgs_file)
