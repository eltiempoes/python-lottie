import io
import json
import gzip
from ..objects import Animation


def parse_tgs_json(file):
    """!
    Reads both tgs and lottie files, returns the json structure
    """
    if isinstance(file, str):
        with open(file, "r") as fileobj:
            return parse_tgs_json(fileobj)

    if isinstance(file, io.TextIOBase):
        binfile = file.buffer
    else:
        binfile = file

    mn = binfile.read(2)
    binfile.seek(0)
    if mn == b'\x1f\x8b': # gzip magic number
        json_file = gzip.open(binfile, "rb")
    elif isinstance(file, io.TextIOBase):
        json_file = file
    else:
        json_file = io.TextIOWrapper(file)

    return json.load(json_file)


def parse_tgs(filename):
    """!
    Reads both tgs and lottie files
    """
    lottie = parse_tgs_json(filename)
    return Animation.load(lottie)
