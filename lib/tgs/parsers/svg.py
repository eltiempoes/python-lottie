from xml.etree import ElementTree
from .. import objects


ns_map = {
    "dc": "http://purl.org/dc/elements/1.1/",
    "cc": "http://creativecommons.org/ns#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "svg": "http://www.w3.org/2000/svg",
    "sodipodi": "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
    "inkscape": "http://www.inkscape.org/namespaces/inkscape",
}

for n, u in ns_map.items():
    ElementTree.register_namespace(n, u)

element_parsers = {}

def element_parser(func):
    element_parsers[func.__name__.split("_")[-1]] = func
    return func

def _qualified(ns, name):
    return "{%s}%s" % (ns_map[ns], name)


def _simplified(name):
    for k, v in ns_map.items():
        name = name.replace("{%s}" % v, k+":")
    return name


def _unqualified(name):
    return name.split("}")[-1]


def _parse_color(color):
    # TODO more format:
    return [int(color[1:3], 16) / 255, int(color[3:5], 16) / 255, int(color[5:7], 16) / 255]


def _add_shape(element, shape, shape_parent):
    style = dict(map(lambda x: x.split(":"), element.attrib["style"].split(";")))
    # TODO handle missing style attributes
    group = objects.Group()
    shape_parent.add_shape(group)
    group.add_shape(shape)
    group.add_shape(objects.Fill(_parse_color(style["fill"])))

    stroke = objects.Stroke()
    group.add_shape(stroke)
    stroke.color.value = _parse_color(style["stroke"])
    stroke.width.value = float(style.get("stroke-width", 0))
    linecap = style.get("stroke-linecap")
    if linecap == "round":
        stroke.line_cap = objects.shapes.LineCap.Round
    elif linecap == "butt":
        stroke.line_cap = objects.shapes.LineCap.Butt
    elif linecap == "square":
        stroke.line_cap = objects.shapes.LineCap.Square
    linejoin = style.get("stroke-linejoin")
    if linejoin == "round":
        stroke.line_cap = objects.shapes.LineJoin.Round
    elif linejoin == "bevel":
        stroke.line_cap = objects.shapes.LineJoin.Bevel
    elif linejoin in {"miter", "arcs", "miter-clip"}:
        stroke.line_cap = objects.shapes.LineJoin.Miter
    stroke.miter_limit = float(style.get("stroke-miterlimit", 0))
    # TODO transform
    return group


@element_parser
def parse_g(element, shape_parent):
    group = objects.Group()
    shape_parent.add_shape(group)
    group.name = element.attrib.get(_qualified("inkscape", "label"), element.attrib.get("id"))
    parse_svg_element(element, group)


@element_parser
def parse_ellipse(element, shape_parent):
    ellipse = objects.Ellipse()
    ellipse.position.value = [
        float(element.attrib["cx"]),
        float(element.attrib["cy"])
    ]
    ellipse.size.value = [
        float(element.attrib["rx"]),
        float(element.attrib["ry"])
    ]
    _add_shape(element, ellipse, shape_parent)


def parse_svg_element(element, shape_parent):
    for child in element:
        tag = _unqualified(child.tag)
        if tag in element_parsers:
            element_parsers[tag](child, shape_parent)


def parse_svg_etree(etree):
    animation = objects.Animation()
    svg = etree.getroot()
    animation.width = float(svg.attrib["width"])
    animation.height = float(svg.attrib["height"])
    animation.name = svg.attrib.get(_qualified("sodipodi", "docname"), svg.attrib.get("id"))
    layer = objects.ShapeLayer()
    animation.add_layer(layer)
    parse_svg_element(svg, layer)
    return animation


def parse_svg_file(file):
    return parse_svg_etree(ElementTree.parse(file))
