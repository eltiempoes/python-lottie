import re
import math
from xml.etree import ElementTree

from .handler import SvgHandler, NameMode
from ... import objects
from ...utils.nvector import NVector


class SvgBuilder(SvgHandler):
    namestart = (
        r":_A-Za-z\xC0-\xD6\xD8-\xF6\xF8-\u02FF\u0370-\u037D\u037F-\u1FFF" +
        r"\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF" +
        r"\uFDF0-\uFFFD\U00010000-\U000EFFFF"
    )
    namenostart = r"-.0-9\xB7\u0300-\u036F\u203F-\u2040"
    id_re = re.compile("^[%s][%s%s]*$" % (namestart, namenostart, namestart))

    def __init__(self):
        super().__init__()
        self.svg = ElementTree.Element("svg")
        self.dom = ElementTree.ElementTree(self.svg)
        self.svg.attrib["xmlns"] = self.ns_map["svg"]
        self.ids = set()
        self.idc = 0
        self.name_mode = NameMode.Inkscape

    def gen_id(self):
        #TODO should check if id_n already exists
        self.idc += 1
        id = "id_%s" % self.idc
        self.ids.add(id)
        return id

    def set_id(self, dom, lottieobj, inkscape_qual=None, force=False):
        n = getattr(lottieobj, "name", None)
        if n is None or self.name_mode == NameMode.NoName:
            if force:
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

    def process(self, animation: objects.Animation, time=0):
        self.svg.attrib["width"] = str(animation.width)
        self.svg.attrib["height"] = str(animation.height)
        self.svg.attrib["viewBox"] = "0 0 %s %s" % (animation.width, animation.height)
        self.svg.attrib["version"] = "1.1"
        self.set_id(self.svg, animation, self.qualified("sodipodi", "docname"))
        self.defs = ElementTree.SubElement(self.svg, "defs")

        for layer in SvgBuilder.setup(animation):
            self.process_layer(layer, self.svg, time)

    def process_layer(self, layer_builder, dom_parent, time):
        cn = layer_builder.lottie.__class__.__name__.lower()
        handler = getattr(self, "_process_" + cn, None)

        g = self.group_from_lottie(layer_builder.lottie, dom_parent, time, True)
        if handler:
            handler(layer_builder.lottie, g, time)

        for c in reversed(layer_builder.children):
            self.process_layer(c, g, time)

    def _process_nulllayer(self, object, dom_parent, time):
        dom_parent.attrib["opacity"] = "1"

    def _process_shapelayer(self, object, dom_parent, time):
        group = SvgBuilderShapeGroup(object)
        group.layer = True
        for shape in object.shapes:
            collect_shape(shape, group)
        self.group_builder_process_children(group, dom_parent, time)

    def set_transform(self, dom, transform, time):
        trans = []
        pos = NVector(*transform.position.get_value(time))
        anchor = NVector(*transform.anchor_point.get_value(time))
        pos -= anchor
        if pos[0] != 0 or pos[0] != 0:
            trans.append("translate(%s, %s)" % (pos.components[0], pos.components[1]))

        scale = NVector(*transform.scale.get_value(time))
        if scale[0] != 100 or scale[1] != 100:
            scale /= 100
            trans.append("scale(%s, %s)" % (scale.components[0], scale.components[1]))

        rot = transform.rotation.get_value(time)
        if rot != 0:
            trans.append("rotate(%s, %s, %s)" % (rot, anchor[0], anchor[1]))

        op = transform.opacity.get_value(time)
        if op != 100:
            dom.attrib["opacity"] = str(op/100)

        if transform.skew:
            skew = transform.skew.get_value(time)
            if skew != 0:
                axis = transform.skew_axis.get_value(time) * math.pi / 180
                skx = skew * math.cos(axis)
                sky = skew * math.sin(axis)
                trans.append("skewX(%s)" % skx)
                trans.append("skewY(%s)" % sky)

        dom.attrib["transform"] = " ".join(trans)

    def group_to_style(self, group, time):
        style = {}
        if group.fill:
            style["fill-opacity"] = group.fill.opacity.get_value(time) / 100
            if isinstance(group.fill, objects.GradientFill):
                style["fill"] = "url(#%s)" % self.process_gradient(group.fill, time)
            else:
                style["fill"] = color_to_css(group.fill.color.get_value(time))
        else:
            style["fill"] = "none"

        if group.stroke:
            if isinstance(group.stroke, objects.GradientStroke):
                style["stroke"] = "url(#%s)" % self.process_gradient(group.stroke, time)
            else:
                style["stroke"] = color_to_css(group.stroke.color.get_value(time))

            style["stroke-opacity"] = group.stroke.opacity.get_value(time) / 100
            style["stroke-width"] = group.stroke.width.get_value(time)
            if group.stroke.miter_limit is not None:
                style["stroke-miterlimit"] = group.stroke.miter_limit

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
        else:
            style["stroke"] = "none"

        return ";".join(map(
            lambda x: ":".join(map(str, x)),
            style.items()
        ))

    def process_gradient(self, gradient, time):
        spos = NVector(*gradient.start_point.get_value(time))
        epos = NVector(*gradient.end_point.get_value(time))

        if gradient.gradient_type == objects.GradientType.Linear:
            dom = ElementTree.SubElement(self.defs, "linerGradient")
            dom.attrib["x1"] = str(spos[0])
            dom.attrib["y1"] = str(spos[1])
            dom.attrib["x2"] = str(epos[0])
            dom.attrib["y2"] = str(epos[1])
        elif gradient.gradient_type == objects.GradientType.Radial:
            dom = ElementTree.SubElement(self.defs, "linerGradient")
            dom.attrib["cx"] = str(spos[0])
            dom.attrib["cy"] = str(spos[1])
            dom.attrib["r"] = str((epos-spos).length)
            a = gradient.highlight_angle.get_value(time) * math.pi / 180
            l = gradient.highlight_length.get_value(time)
            dom.attrib["fx"] = str(spos[0] + math.cos(a) * l)
            dom.attrib["fy"] = str(spos[1] + math.sin(a) * l)

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

    def group_from_lottie(self, lottie, dom_parent, time, layer):
        g = ElementTree.SubElement(dom_parent, "g")
        if layer and self.name_mode == NameMode.Inkscape:
            g.attrib[self.qualified("inkscape", "groupmode")] = "layer"
        self.set_id(g, lottie, self.qualified("inkscape", "label"))
        self.set_transform(g, lottie.transform, time)
        return g

    def group_builder_to_svg(self, group, dom_parent, time):
        if group.empty():
            return

        if group.atomic():
            path = self.build_path(group.paths, dom_parent, time)
            self.set_id(path, group.paths[0])
            path.attrib["style"] = self.group_to_style(group, time)
            self.set_transform(path, group.lottie.transform, time)
            return

        g = self.group_from_lottie(group.lottie, dom_parent, time, group.layer)
        self.group_builder_process_children(group, g, time)

    def group_builder_process_children(self, group, g, time):
        style = self.group_to_style(group, time)
        for shape in reversed(group.children):
            if shape is None:
                if group.paths:
                    path = self.build_path(group.paths, g, time)
                    self.set_id(path, group.paths[0])
                    path.attrib["style"] = style
            elif isinstance(shape, SvgBuilderShapeGroup):
                self.group_builder_to_svg(shape, g, time)
            else:
                if isinstance(shape, objects.Rect):
                    svgshape = self.build_rect(shape, g, time)
                elif isinstance(shape, objects.Ellipse):
                    svgshape = self.build_ellipse(shape, g, time)
                else:
                    # TODO star
                    continue
                self.set_id(svgshape, shape)
                svgshape.attrib["style"] = style

    def build_rect(self, shape, parent, time):
        rect = ElementTree.SubElement(parent, "rect")
        size = shape.size.get_value(time)
        pos = shape.position.get_value(time)
        rect.attrib["width"] = str(size[0])
        rect.attrib["height"] = str(size[1])
        rect.attrib["x"] = str(pos[0] - size[0] / 2)
        rect.attrib["y"] = str(pos[1] - size[1] / 2)
        rect.attrib["rx"] = shape.rounded.get_value(time)
        return rect

    def build_ellipse(self, shape, parent, time):
        ellipse = ElementTree.SubElement(parent, "ellipse")
        size = shape.size.get_value(time)
        pos = shape.position.get_value(time)
        ellipse.attrib["rx"] = str(size[0] / 2)
        ellipse.attrib["ry"] = str(size[1] / 2)
        ellipse.attrib["cx"] = str(pos[0])
        ellipse.attrib["cy"] = str(pos[1])
        return ellipse

    def build_path(self, shapes, parent, time):
        path = ElementTree.SubElement(parent, "path")
        d = ""
        for shape in shapes:
            bez = shape.vertices.get_value(time)
            d += "M %s,%s " % tuple(bez.vertices[0])
            for i in range(1, len(bez.vertices)):
                qfrom = NVector(*bez.vertices[i-1])
                h1 = NVector(*bez.out_point[i-1]) + qfrom
                qto = NVector(*bez.vertices[i])
                h2 = NVector(*bez.in_point[i]) + qto
                d += "C %s,%s %s,%s %s,%s " % (
                    h1[0], h1[1],
                    h2[0], h2[1],
                    qto[0], qto[1],
                )
            if bez.closed:
                qfrom = NVector(*bez.vertices[-1])
                h1 = NVector(*bez.out_point[-1]) + qfrom
                qto = NVector(*bez.vertices[0])
                h2 = NVector(*bez.in_point[0]) + qto
                d += "C %s,%s %s,%s %s,%s Z" % (
                    h1[0], h1[1],
                    h2[0], h2[1],
                    qto[0], qto[1],
                )

        path.attrib["d"] = d
        return path


def color_to_css(color):
    return "rgb(%s, %s, %s)" % tuple(map(lambda c: round(c*255), color[:3]))


class SvgBuilderShapeGroup:
    def __init__(self, lottie):
        self.lottie = lottie
        self.children = []
        self.paths = []
        self.subgroups = []
        self.fill = None
        self.stroke = None
        self.layer = False

    def atomic(self):
        return self.children == [None]

    def empty(self):
        return not self.children

    def finalize(self, thresh=6):
        for g in self.subgroups:
            if g.layer:
                self.layer = True
                return
        nchild = len(self.children)
        self.layer = nchild > thresh and self.lottie.name


def collect_shape(shape, shape_group):
    if isinstance(shape, (objects.Rect, objects.Ellipse, objects.Star)):
        shape_group.children.append(shape)
    elif isinstance(shape, (objects.Fill, objects.GradientFill)):
        shape_group.fill = shape
    elif isinstance(shape, (objects.Stroke, objects.GradientStroke)):
        shape_group.stroke = shape
    elif isinstance(shape, (objects.Shape)):
        if not shape_group.paths:
            shape_group.children.append(None)
        shape_group.paths.append(shape)
    elif isinstance(shape, (objects.Group)):
        subgroup = SvgBuilderShapeGroup(shape)
        shape_group.children.append(subgroup)
        shape_group.subgroups.append(subgroup)
        for subshape in shape.shapes:
            collect_shape(subshape, subgroup)
        subgroup.finalize()

class SvgBuilderLayer:
    def __init__(self, lottie):
        self.lottie = lottie
        self.children = []

    @classmethod
    def setup(cls, animation):
        layers = {}
        flat_layers = []
        for layer in animation.layers:
            laybuilder = cls(layer)
            flat_layers.append(laybuilder)
            if layer.index is not None:
                layers[layer.index] = laybuilder

        top_layers = []
        for layer in flat_layers:
            if layer.lottie.parent is not None:
                layers[layer.lottie.parent].children.append(layer)
            else:
                top_layers.append(layer)
        return reversed(top_layers)


def to_svg(animation, time):
    builder = SvgBuilder()
    builder.process(animation, time)
    return builder.dom

