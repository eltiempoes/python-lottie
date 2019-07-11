import re
import math
from xml.etree import ElementTree

from .handler import SvgHandler, NameMode
from ... import objects
from ...utils.nvector import NVector


class SvgBuilder(SvgHandler):
    namestart = (
        r":_A-Za-z\xC0-\xD6\xD8-\xF6\xF8-\x2FF\x370-\x37D\x37F-\x1FFF" +
        r"\x200C-\x200D\x2070-\x218F\x2C00-\x2FEF\x3001-\xD7FF\xF900-\xFDCF" +
        r"\xFDF0-\xFFFD\x10000-\xEFFFF"
    )
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
        return n

    def process_animation(self, animation: objects.Animation, time=0):
        self.svg.attrib["width"] = animation.width
        self.svg.attrib["height"] = animation.height
        self.svg.attrib["viewBox"] = "0 0 %s %s" % (animation.width, animation.height)
        self.svg.attrib["version"] = "1.1"
        self.set_id(self.svg, animation, self.qualified("sodipodi", "docname"))
        self.defs = ElementTree.SubElement(self.svg, "defs")

        for layer in animation.layers:
            self.parse_item(layer, self.svg, time)

    def process_item(self, object, dom_parent, time):
        cn = object.__class__.__name__.lower()
        handler = getattr(self, "_process_" + cn, None)
        if handler:
            handler(object, dom_parent, time)

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
            trans.append("rotate(%s, %s, %s)" % (rot, anchor[0], anchor[1]))

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

    def collect_shape(self, shape, shape_group):
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
                self.collect_shape(subshape, subgroup)
            subgroup.finalize()

    def _process_shapelayer(self, object, dom_parent, time):
        group = SvgBuilderShapeGroup(object)
        group.layer = True
        for shape in object.shapes:
            self.collect_shape(shape, group)
        self.group_to_svg(group, dom_parent, time)

    def group_to_style(self, group, time):
        style = {}
        if group.fill:
            style["fill-opacity"] = group.fill.opacity.get_value(time) / 100
            if isinstance(group.fill, objects.GradientFill):
                style["fill"] = "url(#%s)" % self.process_gradient(group.fill, time)
            else:
                style["fill"] = color_to_css(group.fill.color.get_value(time))

        if group.stroke:
            if isinstance(group.stroke, objects.GradientStroke):
                style["stroke"] = "url(#%s)" % self.process_gradient(group.stroke, time)
            else:
                style["stroke"] = color_to_css(group.stroke.color.get_value(time))

            style["stroke-opacity"] = group.stroke.opacity.get_value(time) / 100
            style["stroke-width"] = group.stroke.width.get_value(time)
            style["stroke-miterlimit"] = group.stroke.miter_limit.get_value(time)

            if group.stroke.line_cap == objects.LineCap.Round:
                style["stroke-linecap"] = "round"
            elif group.stroke.line_cap == objects.LineCap.Butt:
                style["stroke-linecap"] = "butt"
            elif group.stroke.line_cap == objects.LineCap.Square:
                style["stroke-linecap"] = "square"

            if group.stroke.line_join == objects.LineJoin.Round:
                style["stroke-linejoin"] = "round"
            elif group.stroke.line_join == objects.LineJoin.Bevel:
                style["stroke-linejoin"] = "bevel"
            elif group.stroke.line_join == objects.LineJoin.Miter:
                style["stroke-linejoin"] = "miter"

        return ";".join(map(
            lambda x: ":".join(map(str, x)),
            style.items()
        ))

    def process_gradient(self, gradient, time):
        spos = NVector(gradient.start_point.get_value(time))
        epos = NVector(gradient.end_point.get_value(time))

        if gradient.gradient_type == objects.GradientType.Linear:
            dom = ElementTree.SubElement(self.defs, "linerGradient")
            dom.attrib["x1"] = spos[0]
            dom.attrib["y1"] = spos[1]
            dom.attrib["x2"] = epos[0]
            dom.attrib["y2"] = epos[1]
        elif gradient.gradient_type == objects.GradientType.Radial:
            dom = ElementTree.SubElement(self.defs, "linerGradient")
            dom.attrib["cx"] = spos[0]
            dom.attrib["cy"] = spos[1]
            dom.attrib["r"] = (epos-spos).length
            a = gradient.highlight_angle.get_value(time) * math.pi / 180
            l = gradient.highlight_length.get_value(time)
            dom.attrib["fx"] = spos[0] + math.cos(a) * l
            dom.attrib["fy"] = spos[1] + math.sin(a) * l

        id = self.set_id(dom, gradient, force=True)
        dom.attrib["id"] = id
        dom.attrib["gradientUnits"] = "userSpaceOnUse"

        colors = gradient.colors.colors.get_value(time)
        for i in range(0, len(colors), 4):
            off = colors[i]
            color = colors[i+1:i+4]
            stop = ElementTree.SubElement(dom, "stop")
            stop.attrib["offset"] = "%s%%" % (off * 100)
            stop.attrib["stop-color"] = color_to_css(color)

        return id

    def group_to_svg(self, group, dom_parent, time):
        g = ElementTree.SubElement(dom_parent, "g")
        if group.layer and self.name_mode == NameMode.Inkscape:
            g.attrib[self.qualified("inkscape", "groupmode")] = "layer"
        self.set_id(g, group.lottie, self.qualified("inkscape", "label"))
        self.set_transform(g, group.lottie.transform, time)

        group.attrib["opacity"] = group.lottie.transform.opacity.get_value(time) / 100
        style = self.group_to_style(group, time)
        for shape in group.shape:
            if isinstance(shape, objects.Rect):
                svgshape = self.build_rect(shape, g, time)
            elif isinstance(shape, objects.Ellipse):
                svgshape = self.build_ellipse(shape, g, time)
            else:
                # TODO star
                continue
            self.set_id(svgshape, shape)
            svgshape.attrib["style"] = style

        if group.paths:
            path = self.build_path(group.paths, g, time)
            self.set_id(svgshape, group.paths[0])
            path.attrib["style"] = style

        for subgroup in group.subgroups:
            self.group_to_svg(subgroup, g, time)

    def build_rect(self, shape, parent, time):
        rect = ElementTree.SubElement(parent, "rect")
        size = shape.size.get_value(time)
        pos = shape.position.get_value(time)
        rect.attrib["width"] = size[0]
        rect.attrib["height"] = size[1]
        rect.attrib["x"] = pos[0] - size[0] / 2
        rect.attrib["y"] = pos[1] - size[1] / 2
        rect.attrib["rx"] = shape.rounded.get_value(time)
        return rect

    def build_ellipse(self, shape, parent, time):
        ellipse = ElementTree.SubElement(parent, "ellipse")
        size = shape.size.get_value(time)
        pos = shape.position.get_value(time)
        ellipse.attrib["rx"] = size[0] / 2
        ellipse.attrib["ry"] = size[1] / 2
        ellipse.attrib["cx"] = pos[0]
        ellipse.attrib["cy"] = pos[1]
        return ellipse

    def build_path(self, shapes, parent, time):
        path = ElementTree.SubElement(parent, "path")
        d = ""
        for shape in shapes:
            bez = shape.vertices.get_value(time)
            d += "M %s,%s " % bez.vertices[0]
            for i in range(1, len(bez.vertices)):
                qfrom = NVector(bez.vertices[i-1])
                h1 = NVector(bez.out_points[i-1]) + qfrom
                qto = NVector(bez.vertices[i])
                h2 = NVector(bez.in_points[i]) + qto
                d += "C %s,%s %s,%s %s,%s %s,%s " % (
                    h1[0], h1[1],
                    h2[0], h2[1],
                    qto[0], qto[1],
                )
            if bez.closed:
                qfrom = NVector(bez.vertices[-1])
                h1 = NVector(bez.out_points[-1]) + qfrom
                qto = NVector(bez.vertices[0])
                h2 = NVector(bez.in_points[0]) + qto
                d += "C %s,%s %s,%s %s,%s %s,%s Z" % (
                    h1[0], h1[1],
                    h2[0], h2[1],
                    qto[0], qto[1],
                )

        path.attrib["d"] = d
        return path

def color_to_css(color):
    return "rgb%s" % tuple(map(lambda c: round(c*255), color[:3]))


class SvgBuilderShapeGroup:
    def __init__(self, lottie):
        self.lottie = lottie
        self.shapes = []
        self.paths = []
        self.subgroups = []
        self.fill = None
        self.stroke = None
        self.layer = False

    def atomic(self):
        return not self.shapes and not self.subgroups

    def empty(self):
        return self.atomic and not self.paths

    def finalize(self, thresh=6):
        for g in self.subgroups:
            if g.layer:
                self.layer = True
                return
        nchild = len(self.shapes) + len(self.subgroups)
        if self.paths:
            nchild += 1
        self.layer = nchild > thresh and self.lottie.name
