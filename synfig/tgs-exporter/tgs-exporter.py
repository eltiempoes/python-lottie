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
from helpers.transform import gen_helpers_transform



def gen_group_layer(toplottie, lottie, layer, num_layers):
    """
    Generates the dictionary corresponding to layers/null.json

    Args:
        lottie (dict)               : Lottie generate shape stored here
        layer  (lxml.etree._Element): Synfig format shape layer
        idx    (int)                : Stores the index(number of) of shape layer

    Returns:
        (None)
    """
    idx = num_layers.inc()
    lottie["ddd"] = settings.DEFAULT_3D
    lottie["ind"] = idx
    lottie["ty"] = settings.LAYER_NULL_TYPE
    lottie["nm"] = layer.attrib.get("desc", "Null Layer %s" % idx)
    lottie["sr"] = settings.LAYER_DEFAULT_STRETCH
    lottie["ks"] = {}   # Transform properties to be filled
    pos = [0, 0]            # default
    anchor = [0, 0, 0]      # default
    scale = [100, 100, 100]  # default
    gen_helpers_transform(lottie["ks"], layer, pos, anchor, scale)
    lottie["ao"] = settings.LAYER_DEFAULT_AUTO_ORIENT
    lottie["ip"] = settings.lottie_format["ip"]
    lottie["op"] = settings.lottie_format["op"]
    lottie["st"] = 0 # layer.xpath("param[@name='time_offset']/time/@value") ?
    for child in layer.xpath("param[@name='canvas']/canvas/layer"):
        child_lottie = gen_layer(toplottie, child, num_layers)
        if child_lottie:
            child_lottie["parent"] = idx


def gen_layer(lottie, child, num_layers):
    shape_layer = {"star", "circle", "rectangle", "simple_circle"}
    solid_layer = {"SolidColor"}
    image_layer = {"import"}
    group_layer = {"group"}
    supported_layers = shape_layer.union(solid_layer).union(image_layer).union(group_layer)

    if child.attrib["active"] == "false":   # Only render the active layers
        return None

    if child.attrib["type"] not in supported_layers:  # Only supported layers
        sys.stderr.write("Unsupported layer type: %s" % child.attrib["type"])
        return None

    lottie["layers"].insert(0, {})
    if child.attrib["type"] in shape_layer:           # Goto shape layer
        gen_layer_shape(lottie["layers"][0],
                        child,
                        num_layers.inc())
    elif child.attrib["type"] in solid_layer:         # Goto solid layer
        gen_layer_solid(lottie["layers"][0],
                        child,
                        num_layers.inc())
    elif child.attrib["type"] in image_layer:
        gen_layer_image(lottie["layers"][0],
                        child,
                        num_layers.inc())
    elif child.attrib["type"] in group_layer:
        gen_group_layer(lottie, lottie["layers"][0], child, num_layers)

    return lottie["layers"][0]


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
    for child in root:
        if child.tag == "layer":
            gen_layer(settings.lottie_format, child, num_layers)

    return settings.lottie_format


def export_tgs(file_name):
    structure = parse_to_lottie(file_name)
    structure["tgs"] = 1
    basename = os.path.splitext(file_name)[0]
    out_filename = basename + ".tgs"
    with gzip.open(out_filename, "wb") as fil:
        json.dump(structure, codecs.getwriter('utf-8')(fil))

    #json.dump(structure, sys.stderr, indent=4)


if len(sys.argv) < 2:
    sys.exit()
else:
    settings.init()
    FILE_NAME = sys.argv[1]
    export_tgs(FILE_NAME)
