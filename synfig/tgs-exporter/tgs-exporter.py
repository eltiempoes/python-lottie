# pylint: disable=line-too-long
"""
Python plugin to convert the .sif format into telegram animated stickers (.tgs)
input   : FILE_NAME.sif
output  : FILE_NAME.tgs

Supported Layers are mentioned below
"""
import os
import json
import sys
import gzip
import codecs
from lxml import etree
from canvas import gen_canvas
from layers.shape import gen_layer_shape
from layers.solid import gen_layer_solid
from layers.image import gen_layer_image
from misc import Count
import settings


def parse_to_lottie(file_name):
    """
    Driver function for parsing .sif to lottie(.json) format

    Args:
        file_name (str) : Synfig file name that needs to be parsed to Lottie format

    Returns:
        (str) : File name in json format
    """
    tree = etree.parse(file_name)
    root = tree.getroot()  # canvas
    gen_canvas(settings.lottie_format, root)

    # Storing the file name
    settings.file_name["fn"] = file_name

    # Storing the file directory
    settings.file_name["fd"] = os.path.dirname(file_name)

    num_layers = Count()
    settings.lottie_format["layers"] = []
    shape_layer = {"star", "circle", "rectangle", "simple_circle"}
    solid_layer = {"SolidColor"}
    image_layer = {"import"}
    supported_layers = shape_layer.union(solid_layer)
    supported_layers = supported_layers.union(image_layer)
    for child in root:
        if child.tag == "layer":
            if child.attrib["active"] == "false":   # Only render the active layers
                continue
            if child.attrib["type"] not in supported_layers:  # Only supported layers
                continue
            settings.lottie_format["layers"].insert(0, {})
            if child.attrib["type"] in shape_layer:           # Goto shape layer
                gen_layer_shape(settings.lottie_format["layers"][0],
                                child,
                                num_layers.inc())
            elif child.attrib["type"] in solid_layer:         # Goto solid layer
                gen_layer_solid(settings.lottie_format["layers"][0],
                                child,
                                num_layers.inc())
            elif child.attrib["type"] in image_layer:
                gen_layer_image(settings.lottie_format["layers"][0],
                                child,
                                num_layers.inc())

    return settings.lottie_format


def export_tgs(file_name):
    structure = parse_to_lottie(file_name)
    structure["tgs"] = 1
    basename = os.path.splitext(file_name)[0]
    out_filename = basename + ".tgs"
    with gzip.open(out_filename, "wb") as fil:
        json.dump(structure, codecs.getwriter('utf-8')(fil))


if len(sys.argv) < 2:
    sys.exit()
else:
    settings.init()
    FILE_NAME = sys.argv[1]
    export_tgs(FILE_NAME)
