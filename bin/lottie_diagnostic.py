#!/usr/bin/env python3

import sys
import os
import argparse
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.exporters import exporters
from lottie.importers import importers
from lottie.utils.stripper import float_strip, heavy_strip
from lottie import __version__


def print_loader(loader, type):
    print("* Available %s:" % type)
    for porter in loader:
        print("  * %s" % porter.name)
    if loader.failed_modules:
        print("* Failed %s:" % type)
        for name, missing in loader.failed_modules.items():
            print("  * %s (missing %s)" % (name, missing))


print("* Python version: %s" % sys.version.replace("\n", " "))
print("* Python Lottie version: %s" % __version__)
print_loader(importers, "Importers")
print_loader(exporters, "Exporters")
