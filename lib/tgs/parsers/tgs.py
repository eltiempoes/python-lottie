import json
import gzip
from ..objects import Animation


def parse_tgs_json(filename):
    """!
    Reads both tgs and lottie files, returns the json structure
    """
    with open(filename, "r") as file:
        mn = file.buffer.read(2)
        file.buffer.seek(0)
        if mn == b'\x1f\x8b': # gzip magic number
            json_file = gzip.open(file.buffer, "rb")
        else:
            json_file = file
        return json.load(json_file)


def parse_tgs(filename):
    """!
    Reads both tgs and lottie files
    """
    lottie = parse_tgs_json(filename)
    return Animation.load(lottie)
