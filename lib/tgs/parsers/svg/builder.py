import re
import math
from xml.etree import ElementTree

from .handler import SvgHandler, NameMode
from ... import objects
from ...nvector import NVector
from ...utils import restructure
try:
    from ...utils import font
    has_font = True
except ImportError:
    has_font = False


class SvgBuilder(SvgHandler, restructure.AbstractBuilder):
    merge_paths = True
    namestart = (
        r":_A-Za-z\xC0-\xD6\xD8-\xF6\xF8-\u02FF\u0370-\u037D\u037F-\u1FFF" +
        r"\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF" +
        r"\uFDF0-\uFFFD\U00010000-\U000EFFFF"
    )
    namenostart = r"-.0-9\xB7\u0300-\u036F\u203F-\u2040"
    id_re = re.compile("^[%s][%s%s]*$" % (namestart, namenostart, namestart))

    def __init__(self, time=0):
        super().__init__()
        self.svg = ElementTree.Element("svg")
        self.dom = ElementTree.ElementTree(self.svg)
        self.svg.attrib["xmlns"] = self.ns_map["svg"]
        self.ids = set()
        self.idc = 0
        self.name_mode = NameMode.Inkscape
        self.time = time

    def gen_id(self, prefix="id"):
        #TODO should check if id_n already exists
        self.idc += 1
        id = "%s_%s" % (prefix, self.idc)
        self.ids.add(id)
        return id

    def set_id(self, dom, lottieobj, inkscape_qual=None, force=False):
        n = getattr(lottieobj, "name", None)
        if n is None or self.name_mode == NameMode.NoName:
            if force:
                id = self.gen_id(dom.tag)
                dom.attrib["id"] = id
                return id
            return None

        idn = n.replace(" ", "_")
        if self.id_re.match(idn) and idn not in self.ids:
            self.ids.add(idn)
        else:
            idn = self.gen_id(dom.tag)

        dom.attrib["id"] = idn
        if inkscape_qual:
            dom.attrib[inkscape_qual] = n
        return n

    def _on_animation(self, animation: objects.Animation):
        self.svg.attrib["width"] = str(animation.width)
        self.svg.attrib["height"] = str(animation.height)
        self.svg.attrib["viewBox"] = "0 0 %s %s" % (animation.width, animation.height)
        self.svg.attrib["version"] = "1.1"
        self.set_id(self.svg, animation, self.qualified("sodipodi", "docname"))
        self.defs = ElementTree.SubElement(self.svg, "defs")
        if self.name_mode == NameMode.Inkscape:
            self.svg.attrib[self.qualified("inkscape", "export-xdpi")] = "96"
            self.svg.attrib[self.qualified("inkscape", "export-ydpi")] = "96"
            namedview = ElementTree.SubElement(self.svg, self.qualified("sodipodi", "namedview"))
            namedview.attrib[self.qualified("inkscape", "pagecheckerboard")] = "true"
            namedview.attrib["borderlayer"] = "true"
            namedview.attrib["bordercolor"] = "#666666"
            namedview.attrib["pagecolor"] = "#ffffff"
        self.svg.attrib["style"] = "fill: none; stroke: none"

        return self.svg

    def _on_layer(self, layer_builder, dom_parent):
        if layer_builder.lottie.in_point > self.time or layer_builder.lottie.out_point < self.time:
            return None

        g = self.group_from_lottie(layer_builder.lottie, dom_parent, True)
        if isinstance(layer_builder.lottie, objects.NullLayer):
            g.attrib["opacity"] = "1"
        if not layer_builder.lottie.name:
            g.attrib[self.qualified("inkscape", "label")] = layer_builder.lottie.__class__.__name__
        if layer_builder.shapegroup:
            g.attrib["style"] = self.group_to_style(layer_builder.shapegroup)
        if layer_builder.lottie.hidden:
            g.attrib.setdefault("style", "")
            g.attrib["style"] += "display: none;"

        return g

    def _get_value(self, prop, default=NVector(0, 0)):
        if prop:
            v = prop.get_value(self.time)
        else:
            v = default

        if v is None:
            return default
        if isinstance(v, NVector):
            return v.clone()
        return v

    def set_transform(self, dom, transform):
        trans = []
        pos = self._get_value(transform.position)
        anchor = self._get_value(transform.anchor_point)
        pos -= anchor
        if pos[0] != 0 or pos[1] != 0:
            trans.append("translate(%s, %s)" % (pos.components[0], pos.components[1]))

        scale = self._get_value(transform.scale, NVector(100, 100))
        if scale[0] != 100 or scale[1] != 100:
            scale /= 100
            trans.append("scale(%s, %s)" % (scale.components[0], scale.components[1]))

        rot = self._get_value(transform.rotation, 0)
        if rot != 0:
            trans.append("rotate(%s, %s, %s)" % (rot, anchor[0], anchor[1]))

        if transform.opacity is not None:
            op = transform.opacity.get_value(self.time)
            if op != 100:
                dom.attrib["opacity"] = str(op/100)

        skew = self._get_value(transform.skew, 0)
        if skew != 0:
            axis = self._get_value(transform.skew_axis, 0) * math.pi / 180
            skx = skew * math.cos(axis)
            sky = skew * math.sin(axis)
            # TODO looks like skew moves things around in svg
            trans.append("skewX(%s)" % skx)
            trans.append("skewY(%s)" % sky)

        if trans:
            dom.attrib["transform"] = " ".join(trans)

    def group_to_style(self, group):
        style = {}
        if group.fill:
            style["fill-opacity"] = group.fill.opacity.get_value(self.time) / 100
            if isinstance(group.fill, objects.GradientFill):
                style["fill"] = "url(#%s)" % self.process_gradient(group.fill)
            else:
                style["fill"] = color_to_css(group.fill.color.get_value(self.time))

        if group.stroke:
            if isinstance(group.stroke, objects.GradientStroke):
                style["stroke"] = "url(#%s)" % self.process_gradient(group.stroke)
            else:
                style["stroke"] = color_to_css(group.stroke.color.get_value(self.time))

            style["stroke-opacity"] = group.stroke.opacity.get_value(self.time) / 100
            style["stroke-width"] = group.stroke.width.get_value(self.time)
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

        return ";".join(map(
            lambda x: ":".join(map(str, x)),
            style.items()
        ))

    def process_gradient(self, gradient):
        spos = gradient.start_point.get_value(self.time)
        epos = gradient.end_point.get_value(self.time)

        if gradient.gradient_type == objects.GradientType.Linear:
            dom = ElementTree.SubElement(self.defs, "linearGradient")
            dom.attrib["x1"] = str(spos[0])
            dom.attrib["y1"] = str(spos[1])
            dom.attrib["x2"] = str(epos[0])
            dom.attrib["y2"] = str(epos[1])
        elif gradient.gradient_type == objects.GradientType.Radial:
            dom = ElementTree.SubElement(self.defs, "radialGradient")
            dom.attrib["cx"] = str(spos[0])
            dom.attrib["cy"] = str(spos[1])
            dom.attrib["r"] = str((epos-spos).length)
            a = gradient.highlight_angle.get_value(self.time) * math.pi / 180
            l = gradient.highlight_length.get_value(self.time)
            dom.attrib["fx"] = str(spos[0] + math.cos(a) * l)
            dom.attrib["fy"] = str(spos[1] + math.sin(a) * l)

        id = self.set_id(dom, gradient, force=True)
        dom.attrib["gradientUnits"] = "userSpaceOnUse"

        colors = gradient.colors.colors.get_value(self.time)
        for i in range(0, len(colors), 4):
            off = colors[i]
            color = colors[i+1:i+4]
            stop = ElementTree.SubElement(dom, "stop")
            stop.attrib["offset"] = "%s%%" % (off * 100)
            stop.attrib["stop-color"] = color_to_css(color)

        return id

    def group_from_lottie(self, lottie, dom_parent, layer):
        g = ElementTree.SubElement(dom_parent, "g")
        if layer and self.name_mode == NameMode.Inkscape:
            g.attrib[self.qualified("inkscape", "groupmode")] = "layer"
        self.set_id(g, lottie, self.qualified("inkscape", "label"), force=True)
        self.set_transform(g, lottie.transform)
        return g

    def _on_shapegroup(self, group, dom_parent):
        if group.empty():
            return

        if len(group.children) == 1 and isinstance(group.children[0], restructure.RestructuredPathMerger):
            path = self.build_path(group.paths.paths, dom_parent)
            self.set_id(path, group.paths.paths[0], force=True)
            path.attrib["style"] = self.group_to_style(group)
            self.set_transform(path, group.lottie.transform)
            return

        g = self.group_from_lottie(group.lottie, dom_parent, group.layer)
        g.attrib["style"] = self.group_to_style(group)
        self.shapegroup_process_children(group, g)
        return g

    def _on_merged_path(self, shape, shapegroup, out_parent):
        path = self.build_path(shape.paths, out_parent)
        self.set_id(path, shape.paths[0])
        path.attrib["style"] = self.group_to_style(shapegroup)
        return path

    def _on_shape(self, shape, shapegroup, out_parent):
        if isinstance(shape, objects.Rect):
            svgshape = self.build_rect(shape, out_parent)
        elif isinstance(shape, objects.Ellipse):
            svgshape = self.build_ellipse(shape, out_parent)
        elif isinstance(shape, objects.Star):
            svgshape = self.build_path([shape.to_bezier()], out_parent)
        elif isinstance(shape, objects.Path):
            svgshape = self.build_path([shape], out_parent)
        elif has_font and isinstance(shape, font.FontShape):
            svgshape = self.build_text(shape, out_parent)
        else:
            return
        self.set_id(svgshape, shape, force=True)
        if "style" not in svgshape.attrib:
            svgshape.attrib["style"] = ""
        svgshape.attrib["style"] += self.group_to_style(shapegroup)
        if shape.hidden:
            svgshape.attrib["style"] += "display: none;"
        return svgshape

    def build_rect(self, shape, parent):
        rect = ElementTree.SubElement(parent, "rect")
        size = shape.size.get_value(self.time)
        pos = shape.position.get_value(self.time)
        rect.attrib["width"] = str(size[0])
        rect.attrib["height"] = str(size[1])
        rect.attrib["x"] = str(pos[0] - size[0] / 2)
        rect.attrib["y"] = str(pos[1] - size[1] / 2)
        rect.attrib["rx"] = str(shape.rounded.get_value(self.time))
        return rect

    def build_ellipse(self, shape, parent):
        ellipse = ElementTree.SubElement(parent, "ellipse")
        size = shape.size.get_value(self.time)
        pos = shape.position.get_value(self.time)
        ellipse.attrib["rx"] = str(size[0] / 2)
        ellipse.attrib["ry"] = str(size[1] / 2)
        ellipse.attrib["cx"] = str(pos[0])
        ellipse.attrib["cy"] = str(pos[1])
        return ellipse

    def build_path(self, shapes, parent):
        path = ElementTree.SubElement(parent, "path")
        d = ""
        for shape in shapes:
            bez = shape.shape.get_value(self.time)
            if not bez.vertices:
                continue
            if d:
                d += "\n"
            d += "M %s,%s " % tuple(bez.vertices[0].components[:2])
            for i in range(1, len(bez.vertices)):
                qfrom = bez.vertices[i-1]
                h1 = bez.out_tangents[i-1] + qfrom
                qto = bez.vertices[i]
                h2 = bez.in_tangents[i] + qto
                d += "C %s,%s %s,%s %s,%s " % (
                    h1[0], h1[1],
                    h2[0], h2[1],
                    qto[0], qto[1],
                )
            if bez.closed:
                qfrom = bez.vertices[-1]
                h1 = bez.out_tangents[-1] + qfrom
                qto = bez.vertices[0]
                h2 = bez.in_tangents[0] + qto
                d += "C %s,%s %s,%s %s,%s Z" % (
                    h1[0], h1[1],
                    h2[0], h2[1],
                    qto[0], qto[1],
                )

        path.attrib["d"] = d
        return path

    def _on_shape_modifier(self, shape, shapegroup, out_parent):
        if isinstance(shape.lottie, objects.Repeater):
            svgshape = self.build_repeater(shape.lottie, shape.child, shapegroup, out_parent)
        elif isinstance(shape.lottie, objects.RoundedCorners):
            svgshape = self.build_rouded_corners(shape.lottie, shape.child, shapegroup, out_parent)
        else:
            return self.shapegroup_process_child(shape.child, shapegroup, out_parent)
        if svgshape:
            self.set_id(svgshape, shape, force=True)
            svgshape.attrib["style"] = self.group_to_style(shapegroup)
        return svgshape

    def build_repeater(self, shape, child, shapegroup, out_parent):
        original = self.shapegroup_process_child(child, shapegroup, out_parent)
        if not original:
            return

        ncopies = int(round(shape.copies.get_value(self.time)))
        if ncopies == 1:
            return

        out_parent.remove(original)

        g = ElementTree.SubElement(out_parent, "g")

        for copy in range(ncopies-1):
            use = ElementTree.SubElement(g, "use")
            use.attrib[self.qualified("xlink", "href")] = "#" + original.attrib["id"]

        orig_wrapper = ElementTree.SubElement(g, "g")
        orig_wrapper.append(original)

        transform = objects.Transform()
        so = shape.transform.start_opacity.get_value(self.time)
        eo = shape.transform.end_opacity.get_value(self.time)
        position = shape.transform.position.get_value(self.time)
        rotation = shape.transform.rotation.get_value(self.time)
        anchor_point = shape.transform.anchor_point.get_value(self.time)
        for i in range(ncopies-1, -1, -1):
            of = i / (ncopies-1)
            transform.opacity.value = so * of + eo * (1 - of)
            self.set_transform(g[i], transform)
            transform.position.value += position
            transform.rotation.value += rotation
            transform.anchor_point.value += anchor_point

        return g

    def build_rouded_corners(self, shape, child, shapegroup, out_parent):
        round_amount = shape.radius.get_value(self.time)
        if isinstance(child, objects.Shape):
            path = child.to_bezier()
            bezier = path.shape.get_value(self.time).rounded(round_amount)
            path.shape.clear_animation(bezier)
            return self._on_shape(path, shapegroup, out_parent)

        if isinstance(child, restructure.RestructuredShapeGroup):
            self._build_rouded_corners_group(child, round_amount)
            return self._on_shapegroup(child, out_parent)

        return child

    def _build_rouded_corners_group(self, shapegroup, round_amount):
        children = []
        for sh in shapegroup.children:
            if isinstance(sh, objects.Shape):
                path = sh.to_bezier()
                bezier = path.shape.get_value(self.time).rounded(round_amount)
                path.shape.clear_animation(bezier)
                sh = path
            elif isinstance(sh, restructure.RestructuredShapeGroup):
                self._build_rouded_corners_group(sh, round_amount)
            children.append(sh)
        shapegroup.children = children

    def _custom_object_supported(self, shape):
        if has_font and isinstance(shape, font.FontShape):
            return True
        return False

    def build_text(self, shape, parent):
        text = ElementTree.SubElement(parent, "text")
        if "family" in shape.query:
            text.attrib["font-family"] = shape.query["family"]
        if "weight" in shape.query:
            text.attrib["font-weight"] = str(shape.query.weight_to_css())
        slant = int(shape.query.get("slant", 0))
        if slant > 0 and slant < 110:
            text.attrib["font-style"] = "italic"
        elif slant >= 110:
            text.attrib["font-style"] = "oblique"

        text.attrib["font-size"] = str(shape.size)

        text.attrib["white-space"] = "pre"

        pos = shape.style.position
        text.attrib["x"] = str(pos.x)
        text.attrib["y"] = str(pos.y)
        text.text = shape.text

        return text


def color_to_css(color):
    #if len(color) == 4:
        #return ("rgba(%s, %s, %s" % tuple(map(lambda c: int(round(c*255)), color[:3]))) + ", %s)" % color[3]
    return "rgb(%s, %s, %s)" % tuple(map(lambda c: int(round(c*255)), color[:3]))


def to_svg(animation, time):
    builder = SvgBuilder(time)
    builder.process(animation)
    return builder.dom
