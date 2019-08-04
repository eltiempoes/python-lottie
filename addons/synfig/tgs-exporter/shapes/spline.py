import math

from misc import Count
import settings


def gen_shape_shape(lottie, layer, idx):
    """
    Generates the dictionary corresponding to properties/shape.json TODO shapeKeyframed
    """
    if layer.xpath("//entry/composite/point/animated"):
        return

    lottie["d"] = settings.DEFAULT_DIRECTION
    lottie["a"] = False
    lottie["ix"] = idx
    lottie["k"] = {}
    gen_shape_shapeprop(lottie["k"], layer.xpath("param[@name='bline']/bline")[0])


def gen_shape_shapeprop(lottie, bline):
    lottie["c"] = int(bline.attrib["loop"] == "true")
    lottie["v"] = []
    lottie["i"] = []
    lottie["o"] = []
    for v in bline.xpath("entry"):
        if len(v.xpath("composite/point/vector/x/text()")) == 0:
            import pdb; pdb.set_trace()
            pass
        x = float(v.xpath("composite/point/vector/x/text()")[0])
        y = float(v.xpath("composite/point/vector/y/text()")[0])
        lottie["v"].append([x, y])
        lottie["i"].append(pol2cart(v.xpath("composite/t1")[0], x, y))
        lottie["o"].append(pol2cart(v.xpath("composite/t2")[0], x, y))


def pol2cart(elem, x, y):
    r = float(elem.xpath("radial_composite/radius/real/@value")[0])
    th = float(elem.xpath("radial_composite/theta/angle/@value")[0]) / 180 * math.pi
    return [r * math.cos(th) + x, r * math.sin(th) + y]


def gen_shapes_spline(lottie, layer, idx):
    """
    Generates the dictionary corresponding to shapes/shape.json

    Args:
        lottie (dict)               : The lottie generated rectangle layer will be stored in it
        layer  (lxml.etree._Element): Synfig format rectangle layer
        idx    (int)                : Stores the index of the rectangle layer

    Returns:
        (None)
    """
    lottie["ty"] = "sh"     # Type: shape
    lottie["d"] = settings.DEFAULT_DIRECTION
    lottie["mn"] = ""       # Match name
    lottie["ky"] = {}
    gen_shape_shape(lottie["ky"], layer, idx)
