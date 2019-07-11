from .handler import SvgHandler, NameMode
from xml.etree import ElementTree
from .. import objects


class SvgBuilder(SvgHandler):
    namestart = r":_A-Za-z\xC0-\xD6\xD8-\xF6\xF8-\x2FF\x370-\x37D\x37F-\x1FFF\x200C-\x200D\x2070-\x218F\x2C00-\x2FEF\x3001-\xD7FF\xF900-\xFDCF\xFDF0-\xFFFD\x10000-\xEFFFF"
    namenostart = r"-.0-9\xB7\x0300-\x036F\x203F-\x2040"
    id_re = re.compile("^[%s][%s%s]*$" % (namestart, namenostart, namestart))

    def __init__(self):
        super().__init__(self)
        self.svg = ElementTree.Element("svg")
        self.dom = ElementTree.ElementTree(self.svg)
        self.svg["xmlns"] = self.ns_map["svg"]
        self.ids = {}
        self.idc = 0
        self.name_mode = NameMode.Inkscape

    def gen_id(self):
        #TODO should check if id_n already exists
        self.idc += 1
        id = "id_" + self.idc
        self.ids.add(id)
        return id

    def set_id(self, dom, lottieobj, inkscape_qual=None, force=False):
        n = getattr(lottieobj, "name", None)
        if n is None or self.name_mode == NameMode.NoName:
            if self.force:
                dom.attrib["id"] = self.gen_id()
            return

        idn = n.replace(" ", "_")
        if self.id_re.match(idn) and idn not in self.ids:
            self.ids.add(idn)
        else:
            idn = self.gen_id()

        dom.attrib["id"] = idn
        if inkscape_qual:
            dom.attrib[inkscape_qual] = n

    def process_animation(self, animation: objects.Animation, time=0):
        self.svg.attrib["width"] = animation.width
        self.svg.attrib["height"] = animation.height
        self.svg.attrib["viewBox"] = "0 0 %s %s" % (animation.width, animation.height)
        self.svg.attrib["version"] = "1.1"
        self.set_id(self.svg, animation, self.qualified("sodipodi", "docname"))
        for layer in animation.layers:
            self.parse_item(layer, self.svg, time)

    def process_item(self, object, dom_parent, time):
        cn = object.__class__.__name__.lower()
        handler = getattr(self, "_process_" + cn, None)
        if handler:
            handler(object, dom_parent, time)

    def _process_shapelayer(self, object, dom_parent, time):
        g = ElementTree.SubElement(dom_parent, "g")
        if self.name_mode == NameMode.Inkscape:
            g.attrib[self.qualified("inkscape", "groupmode")] = "layer"
        self.set_id(g, object, self.qualified("inkscape", "label"))
        self.set_transform(g, object.transform, time)

        group = SvgBuilderShapeGroup(None)
        for shape in object.shapes:
            self.process_shape(shape, group)

    def set_transform(self, dom, transform, time):
        trans = []
        pos = NVector(transform.position.get_value(time))
        anchor = NVector(transform.anchor_point.get_value(time))
        pos -= anchor
        if pos[0] != 0 or pos[0] != 0:
            trans.append("translate(%s, %s)" % pos.components)

        scale = NVector(transform.position.get_value(time))
        if scale[0] != 100 or scale[1] != 100:
            scale /= 100
            trans.append("scale(%s, %s)" % scale.components)

        rot = transform.rotation.get_value(time)
        if rot != 0:
            trans.append("rotate(%s, %s, %s)" % (rot, achor[0], anchor[1]))

        op = transform.opacity.get_value(time)
        if op != 100:
            dom.attrib["style"] = dom.attrib.get("style", "") + "opacity:%s;" % (op/100)

        skew = transform.skew.get_value(time)
        if skew != 0:
            axis = transform.skew_axis.get_value(time) * math.pi / 180
            skx = skew * math.cos(axis)
            sky = skew * math.sin(axis)
            trans.append("skewX(%s)" % skx)
            trans.append("skewY(%s)" % sky)

        dom.attrib["transform"] = " ".join(trans)

    def process_shape(self, shape, shape_group):
        if isinstance(shape, (objects.Rect, objects.Ellipse, objects.Star)):
            shape_group.shapes.append(shape)
        elif isinstance(shape, (objects.Fill, objects.GradientFill)):
            shape_group.fill = shape
        elif isinstance(shape, (objects.Stroke, objects.GradientStroke)):
            shape_group.stroke = shape
        elif isinstance(shape, (objects.Shape)):
            shape_group.paths.append(shape)
        elif isinstance(shape, (objects.Group)):
            subgroup = SvgBuilderShapeGroup(shape)
            shape_group.subgroups.append(subgroup)
            for subshape in shape.shapes:
                self.process_shape(subshape, subgroup)


class SvgBuilderShapeGroup:
    def __init__(self, parent):
        self.parent = parent
        self.shapes = []
        self.paths = []
        self.subgroups = []
        self.fill = None
        self.stroke = None

    def atomic(self):
        return not self.shapes and not self.subgroups

    def empty(self):
        return self.atomic and not self.paths
