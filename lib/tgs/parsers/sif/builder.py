from xml.etree import ElementTree

from ... import objects
from ..svg.builder import SvgBuilder


blend_modes = {
    objects.BlendMode.Normal: 0, # composite
    objects.BlendMode.Multiply: 6,
    objects.BlendMode.Screen: 16,
    objects.BlendMode.Overlay: 20,
    objects.BlendMode.Darken: 3,
    objects.BlendMode.Lighten: 2,
    objects.BlendMode.HardLight: 17,
    objects.BlendMode.Difference: 18,
    objects.BlendMode.Hue: 9,
    objects.BlendMode.Saturation: 10,
    objects.BlendMode.Color: 8,
    objects.BlendMode.Luminosity: 11,
    #1  : "straight",
    #13 : "onto",
    #21 : "straight onto",
    #12 : "behind",
    #7  : "divide",
    #4  : "add",
    #5  : "subtract",
    objects.BlendMode.Exclusion: 18,
    objects.BlendMode.SoftLight: 6,
    objects.BlendMode.ColorDodge: 0,
    objects.BlendMode.ColorBurn: 0,
}




class SifBuilder:
    def __init__(self):
        super().__init__()
        self.canvas = ElementTree.Element("canvas")
        self.dom = ElementTree.ElementTree(self.canvas)
        self.dom.attrib["version"] = "1.0"

    def _format_time(self, time):
        return "%sf" % time

    def process(self, animation: objects.Animation):
        if animation.name:
            ElementTree.SubElement(self.canvas, "name").text = animation.name
        self.canvas.attrib["width"] = animation.width
        self.canvas.attrib["height"] = animation.height
        self.canvas.attrib["fps"] = animation.frame_rate
        self.canvas.attrib["begin-time"] = self._format_time(animation.in_point)
        self.canvas.attrib["end-time"] = self._format_time(animation.out_point)

        for layer in SvgBuilder.setup(animation):
            self.process_layer(layer, self.canvas)

    def process_layer(self, layer_builder, dom_parent):
        cn = layer_builder.lottie.__class__.__name__.lower()

        group = self.group_from_lottie(layer_builder.lottie, dom_parent)

        bm = getattr(layer_builder.lottie, "blend_mode", objects.BlendMode.Normal)
        self.simple_param("blend_method", bm, group, "integer").attrib["static"] = "true"

        stretch = getattr(layer_builder.lottie, "stretch", 1) or 1
        self.simple_param("time_dilation", stretch, group)

        # TODO seconds?
        in_point = getattr(layer_builder.lottie, "in_point", 0)
        self.simple_param("time_offset", self._format_time(in_point), group)

        handler = getattr(self, "_process_" + cn, None)
        if handler:
            handler(layer_builder.lottie, group, time)

        for c in reversed(layer_builder.children):
            self.process_layer(c, group, time)

    def group_from_lottie(self, lottie, dom_parent):
        g = ElementTree.SubElement(dom_parent, "layer")
        g.attrib["type"] = "group"
        g.attrib["active"] = "true"
        g.attrib["exclude_from_rendering"] = "false"
        g.attrib["version"] = "0.2"
        if lottie.name:
            g.attrib["desc"] = lottie.name
        self.set_transform(g, lottie.transform)
        return g

    def set_transform(self, group, transform):
        param = ElementTree.SubElement(group, "param")
        param.attrib["name"] = "transformation"
        composite = ElementTree.SubElement(param, "composite")
        composite.attrib["type"] = "transformation"
        self.process_vector("offset", transform.position, composite)
        self.process_vector("scale", transform.scale, composite)
        self.process_scalar("angle", "angle", transform.rotation, composite)
        self.process_scalar("angle", "skew_angle", transform.rotation, composite)

        self.process_scalar("real", "param", transform.rotation, group).attrib["name"] = "amount"
        self.process_vector("param", objects.MultiDimensional([0, 0]), group).attrib["name"] = "origin"
        # TODO get z_depth from position
        self.process_scalar("real", "param", objects.Value(0), group).attrib["name"] = "z_depth"

    def process_vector(self, name, multidim, parent):
        wrap = ElementTree.SubElement(parent, name)
        if multidim.animated:
            animated = ElementTree.SubElement(wrap, "animated")
            animated.attrib["type"] = "vector"
            for keyframe in multidim.keyframes:
                waypoint = ElementTree.SubElement(animated, "waypoint")
                # TODO convert to seconds?
                waypoint["time"] = self._format_time(keyframe.time)
                waypoint["before"] = waypoint["after"] = "clamped"
                vector = ElementTree.SubElement(waypoint, "vector")
                x, y = keyframe.start
                ElementTree.SubElement(vector, "x").text = str(x)
                ElementTree.SubElement(vector, "y").text = str(y)
        else:
            vector = ElementTree.SubElement(wrap, "vector")
            x, y = multidim.value
            ElementTree.SubElement(vector, "x").text = str(x)
            ElementTree.SubElement(vector, "y").text = str(y)
        return wrap

    def process_scalar(self, type, name, value, parent):
        wrap = ElementTree.SubElement(parent, name)
        if value.animated:
            animated = ElementTree.SubElement(wrap, "animated")
            animated.attrib["type"] = "vector"
            for keyframe in value.keyframes:
                waypoint = ElementTree.SubElement(animated, "waypoint")
                # TODO convert to seconds?
                waypoint["time"] = self._format_time(keyframe.time)
                waypoint["before"] = waypoint["after"] = "clamped"
                vector = ElementTree.SubElement(waypoint, type)
                ElementTree.SubElement(vector, type).text = str(keyframe.start)
        else:
            vector = ElementTree.SubElement(wrap, "vector")
            ElementTree.SubElement(vector, type).text = str(value.value)
        return wrap

    def simple_param(self, name, vaue, parent, type="real"):
        param = ElementTree.SubElement(parent, "param")
        param.attrib["name"] = name
        e_val = ElementTree.SubElement(blend, type)
        e_val.attrib["value"] = str(vaue)
        return e_val
