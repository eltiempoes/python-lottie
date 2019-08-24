# pylint: disable=line-too-long
"""
Python plugin to convert the .sif format into lottie json format
input   : FILE_NAME.sif
output  : FILE_NAME.json
        : FILE_NAME.html
        : FILE_NAME.log

Supported Layers are mentioned below
"""
import os
import json
import sys
import logging
import gzip
import codecs
from lxml import etree
from canvas import gen_canvas
from layers.driver import gen_layers
from common.misc import modify_final_dump
from common.Canvas import Canvas
import settings


def write_to(filename, extension, data):
    """
    Helps in writing data to a specified file name

    Args:
        filename  (str) : Original file name
        extension (str) : original file name needs to be converted to this
        data      (str) : Data that needs to be written

    Returns:
        (str) : changed file name according to the extension specified
    """
    new_name = filename.split(".")
    new_name[-1] = extension
    new_name = ".".join(new_name)
    with open(new_name, "w") as fil:
        fil.write(data)
    return new_name


def parse(file_name):
    """
    Driver function for parsing .sif to lottie(.json) format

    Args:
        file_name (str) : Synfig file name that needs to be parsed to Lottie format

    Returns:
        (str) : File name in json format
    """
    tree = etree.parse(file_name)
    canvas = Canvas(root)
    gen_layers(settings.lottie_format["layers"], canvas, canvas.get_num_layers() - 1)

    # Storing the file name
    settings.file_name["fn"] = file_name

    # Storing the file directory
    settings.file_name["fd"] = os.path.dirname(file_name)

    # Initialize the logging
    init_logs()

    settings.lottie_format["layers"] = []
    gen_layers(settings.lottie_format["layers"], root, len(root) - 1)

    return modify_final_dump(settings.lottie_format)


def init_logs():
    """
    Initializes the logger, sets the file name in which the logs will be stored
    and sets the level of the logging(DEBUG | INFO : depending on what is
    specified)
    """
    name = settings.file_name['fn']
    name = name.split(".")
    name[-1] = 'log'
    name = '.'.join(name)
    path = os.path.join(settings.file_name['fd'], name)
    path = os.path.abspath(name)
    logging.basicConfig(filename=path, filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)


def export_tgs(file_name):
    structure = parse(file_name)
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
