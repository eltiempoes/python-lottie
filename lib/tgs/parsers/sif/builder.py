import math
from xml.etree import ElementTree

from ... import objects
from ..svg.builder import SvgBuilderLayer, SvgBuilderShapeGroup, collect_shape


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
    coord_scale = 60

    def __init__(self):
        super().__init__()
        self.canvas = ElementTree.Element("canvas")
        self.dom = ElementTree.ElementTree(self.canvas)
        self.canvas.attrib["version"] = "1.0"

    def _format_time_f(self, time):
        return "%sf" % time

    def _format_time(self, time):
        return "%ss" % (time / self.framerate)

    def _x(self, v):
        return (v - self.width / 2) / self.coord_scale

    def _y(self, v):
        return (v - self.height / 2) / self.coord_scale

    def process(self, animation: objects.Animation):
        if animation.name:
            ElementTree.SubElement(self.canvas, "name").text = animation.name
        self.canvas.attrib["width"] = str(animation.width)
        self.canvas.attrib["height"] = str(animation.height)
        self.canvas.attrib["fps"] = str(animation.frame_rate)
        self.canvas.attrib["begin-time"] = self._format_time_f(animation.in_point)
        self.canvas.attrib["end-time"] = self._format_time_f(animation.out_point)
        self.framerate = animation.frame_rate
        self.end_frame = animation.out_point
        self.width = animation.width
        self.height = animation.height

        for layer in SvgBuilderLayer.setup(animation):
            self.process_layer(layer, self.canvas)

    def process_layer(self, layer_builder, dom_parent):
        cn = layer_builder.lottie.__class__.__name__.lower()

        layer = self.layer_from_lottie("group", layer_builder.lottie, dom_parent)

        bm = getattr(layer_builder.lottie, "blend_mode", objects.BlendMode.Normal)
        self.simple_param("blend_method", bm, layer, "integer").attrib["static"] = "true"

        stretch = getattr(layer_builder.lottie, "stretch", 1) or 1
        self.simple_param("time_dilation", stretch, layer)

        in_point = getattr(layer_builder.lottie, "in_point", 0)
        self.simple_param("time_offset", self._format_time(in_point), layer, "time")

        pcanv = ElementTree.SubElement(layer, "param")
        pcanv.attrib["name"] = "canvas"
        canvas = ElementTree.SubElement(pcanv, "canvas")
        out_point = getattr(layer_builder.lottie, "out_point", self.end_frame)
        canvas.attrib["end-time"] = self._format_time(out_point)

        handler = getattr(self, "_process_" + cn, None)
        if handler:
            handler(layer_builder.lottie, canvas)

        for c in reversed(layer_builder.children):
            self.process_layer(c, canvas)

    def layer_from_lottie(self, type, lottie, dom_parent):
        g = ElementTree.SubElement(dom_parent, "layer")
        g.attrib["type"] = type
        g.attrib["active"] = "true"
        g.attrib["exclude_from_rendering"] = "false"
        #g.attrib["version"] = "0.2"
        if lottie.name:
            g.attrib["desc"] = lottie.name
        transf = getattr(lottie, "transform", None)
        if transf:
            self.set_transform(g, lottie.transform)
        return g

    def set_transform(self, group, transform):
        param = ElementTree.SubElement(group, "param")
        param.attrib["name"] = "transformation"
        composite = ElementTree.SubElement(param, "composite")
        composite.attrib["type"] = "transformation"
        self.process_vector("offset", transform.position, composite)

        def get_scale(keyframe, elem):
            if keyframe is None:
                v = transform.scale.value
            else:
                v = keyframe.start
            ElementTree.SubElement(elem, "x").text = str(v[0] / 100)
            ElementTree.SubElement(elem, "y").text = str(v[1] / 100)

        self.process_vector_ext("scale", transform.scale.keyframes, composite, "vector", get_scale)
        self.process_scalar("angle", "angle", transform.rotation, composite)
        self.process_scalar("angle", "skew_angle", transform.rotation, composite)

        def getter(keyframe, elem):
            if keyframe is None:
                v = transform.opacity.value
            else:
                v = keyframe.start[0]
            elem.attrib["value"] = str(v/100)
        amountp = self.process_vector_ext("param", transform.opacity.keyframes, group, "real", getter)
        amountp.attrib["name"] = "amount"

        self.process_vector("param", objects.MultiDimensional([self.width/2, self.height/2]), group).attrib["name"] = "origin"
        # TODO get z_depth from position
        self.process_scalar("real", "param", objects.Value(0), group).attrib["name"] = "z_depth"

    def process_vector(self, name, multidim, parent):
        def getter(keyframe, elem):
            if keyframe is None:
                v = multidim.value
            else:
                v = keyframe.start
            ElementTree.SubElement(elem, "x").text = str(v[0])
            ElementTree.SubElement(elem, "y").text = str(v[1])

        return self.process_vector_ext(name, multidim.keyframes, parent, "vector", getter)

    def process_vector(self, name, multidim, parent):
        def getter(keyframe, elem):
            if keyframe is None:
                v = multidim.value
            else:
                v = keyframe.start
            ElementTree.SubElement(elem, "x").text = "0" #str(self._x(v[0]))
            ElementTree.SubElement(elem, "y").text = "0" #str(self._y(v[1]))

        return self.process_vector_ext(name, multidim.keyframes, parent, "vector", getter)

    def process_vector_ext(self, name, kframes, parent, type, getter):
        wrap = ElementTree.SubElement(parent, name)
        if kframes is not None:
            animated = ElementTree.SubElement(wrap, "animated")
            animated.attrib["type"] = type
            for keyframe in kframes:
                waypoint = ElementTree.SubElement(animated, "waypoint")
                waypoint.attrib["time"] = self._format_time(keyframe.time)
                waypoint.attrib["before"] = waypoint.attrib["after"] = "clamped"
                vector = ElementTree.SubElement(waypoint, type)
                getter(keyframe, vector)
        else:
            vector = ElementTree.SubElement(wrap, type)
            getter(None, vector)
        return wrap

    def process_scalar(self, type, name, value, parent):
        def getter(keyframe, elem):
            if keyframe is None:
                v = value.value
            else:
                v = keyframe.start
            elem.attrib["value"] = str(v)
        return self.process_vector_ext(name, value.keyframes, parent, type, getter)

    def simple_param(self, name, vaue, parent, type="real"):
        param = ElementTree.SubElement(parent, "param")
        param.attrib["name"] = name
        e_val = ElementTree.SubElement(param, type)
        e_val.attrib["value"] = str(vaue)
        return e_val

    def simple_composite_param(self, name, vaue, parent, type="real"):
        param = ElementTree.SubElement(parent, name)
        e_val = ElementTree.SubElement(param, type)
        e_val.attrib["value"] = str(vaue)
        return e_val

    def _process_shapelayer(self, object, dom_parent):
        group = SvgBuilderShapeGroup(object)
        for shape in object.shapes:
            collect_shape(shape, group)
        self.group_builder_process_children(group, dom_parent)

    def group_builder_path_to_sif(self, path, group, dom_parent):
        layers = []
        if group.fill:
            sif_shape = self.build_path("region", path, dom_parent)
            self.apply_group_fill(sif_shape, group.fill)
            layers.append(sif_shape)
        if group.stroke:
            sif_shape = self.build_path("outline", path, dom_parent)
            self.apply_group_stroke(sif_shape, group.stroke)
            layers.append(sif_shape)
        return layers

    def group_builder_paths_to_sif(self, group, dom_parent):
        if group.paths:
            for path in group.paths:
                self.group_builder_path_to_sif(path, group, dom_parent)

    def group_builder_process_children(self, group, dom_parent):
        for shape in reversed(group.children):
            if shape is None:
                self.group_builder_paths_to_sif(group, dom_parent)
            elif isinstance(shape, SvgBuilderShapeGroup):
                self.group_builder_to_sif(shape, dom_parent)
            else:
                if group.fill:
                    if isinstance(shape, objects.Rect):
                        sif_shape = self.build_rect(shape, dom_parent)
                    elif isinstance(shape, objects.Ellipse):
                        sif_shape = self.build_ellipse(shape, dom_parent)
                    else:
                        # TODO star
                        continue
                    self.apply_group_fill(sif_shape, group.fill)
                if group.stroke:
                    # TODO if not create bline for rect / ellipse etc
                    pass

    def build_rect(self, shape, dom_parent):
        layer = self.layer_from_lottie("rectangle", shape, dom_parent)

        keyframes = {}
        if shape.position.animated:
            keyframes.update({kf.time: kf for kf in shape.position.keyframes})
        if shape.size.animated:
            keyframes.update({kf.time: kf for kf in shape.size.keyframes})
        keyframes = list(sorted(keyframes.keys(), key=lambda kf: kf.time)) or None

        def getp1(kf, elem):
            pos = shape.position.get_value(kf.time)
            sz = shape.size.get_value(kf.time)
            ElementTree.SubElement(elem, "x").text = str(self._x(pos[0] - sz[0]/2))
            ElementTree.SubElement(elem, "y").text = str(self._y(pos[1] - sz[1]/2))

        def getp2(kf, elem):
            pos = shape.position.get_value(kf.time)
            sz = shape.size.get_value(kf.time)
            ElementTree.SubElement(elem, "x").text = str(self._x(pos[0] + sz[0]/2))
            ElementTree.SubElement(elem, "y").text = str(self._y(pos[1] + sz[1]/2))

        self.process_vector_ext("param", keyframes, layer, "vector", getp1).attrib["name"] = "point1"
        self.process_vector_ext("param", keyframes, layer, "vector", getp2).attrib["name"] = "point2"
        self.process_scalar("real", "param", shape.rounded, layer).attrib["name"] = "bevel"
        return layer

    def apply_group_fill(self, sif_shape, fill):
        # TODO gradients?
        if hasattr(fill, "colors"):
            return

        def getter(keyframe, elem):
            if keyframe is None:
                v = fill.color.value
            else:
                v = keyframe.start
            ElementTree.SubElement(elem, "r").text = str(v[0])
            ElementTree.SubElement(elem, "g").text = str(v[1])
            ElementTree.SubElement(elem, "b").text = str(v[2])
            ElementTree.SubElement(elem, "a").text = "1"

        self.process_vector_ext("param", fill.color.keyframes, sif_shape, "color", getter).attrib["name"] = "color"

        def get_op(keyframe, elem):
            if keyframe is None:
                v = fill.opacity.value
            else:
                v = keyframe.start
            v /= 100
            elem.attrib["value"] = str(v)

        self.process_vector_ext("param", fill.opacity.keyframes, sif_shape, "real", get_op).attrib["name"] = "amount"

    def apply_group_stroke(self, sif_shape, stroke):
        self.apply_group_fill(sif_shape, stroke)
        cusp = self._format_bool(stroke.line_join == objects.LineJoin.Miter)
        self.simple_param("sharp_cusps", cusp, sif_shape, "bool")
        round_cap = self._format_bool(stroke.line_cap == objects.LineCap.Round)
        self.simple_param("round_tip[0]", round_cap, sif_shape, "bool")
        self.simple_param("round_tip[1]", round_cap, sif_shape, "bool")
        self.process_scalar("real", "param", stroke.width, sif_shape).attrib["name"] = "width"

    def build_ellipse(self, shape, dom_parent):
        layer = self.layer_from_lottie("circle", shape, dom_parent)

        def get_r(keyframe, elem):
            if keyframe is None:
                v = shape.size.value
            else:
                v = keyframe.start
            sz = math.hypot(*v) / self.coord_scale
            elem.attrib["value"] = str(sz)
        self.process_vector_ext("param", shape.size.keyframes, layer, "real", get_r).attrib["name"] = "radius"
        self.process_vector("param", shape.position, layer).attrib["name"] = "origin"
        return layer

    def _format_bool(self, value):
        return str(bool(value)).lower()

    def build_path(self, type, path, dom_parent):
        layer = self.layer_from_lottie(type, path, dom_parent)
        bline_par = ElementTree.SubElement(layer, "param")
        bline_par.attrib["name"] = "bline"
        bline = ElementTree.SubElement(bline_par, "bline")
        bline.attrib["type"] = "bline_point"
        startbez = path.vertices.get_value()
        bline.attrib["loop"] = self._format_bool(startbez.closed)
        nverts = len(startbez.vertices)
        for point in range(nverts):
            self.bezier_point(path, point, bline)
        return layer

    def bezier_point(self, lottie_path, point_index, sif_parent):
        entry = ElementTree.SubElement(sif_parent, "entry")
        composite = ElementTree.SubElement(entry, "composite")
        composite.attrib["type"] = "bline_point"

        def get_point(keyframe, elem):
            if keyframe is None:
                bezier = lottie_path.vertices.value
            else:
                bezier = keyframe.start

            vert = bezier.vertices[point_index]
            ElementTree.SubElement(elem, "x").text = str(self._x(vert[0]))
            ElementTree.SubElement(elem, "y").text = str(self._y(vert[1]))

        self.process_vector_ext("point", lottie_path.vertices.keyframes, composite, "vector", get_point)
        self.simple_composite_param("split", "true", composite, "bool")
        self.simple_composite_param("split_radius", "true", composite, "bool")
        self.simple_composite_param("split_angle", "true", composite, "bool")
        self.simple_composite_param("width", "1.0", composite, "real")
        self.simple_composite_param("origin", "0.5", composite, "real")

        def get_tangent(keyframe, elem):
            if keyframe is None:
                bezier = lottie_path.vertices.value
            else:
                bezier = keyframe.start

            inp = getattr(bezier, which_point)[point_index]
            radius = math.hypot(*inp) / self.coord_scale
            theta = math.atan2(inp[1], inp[0]) * 180 / math.pi
            elem.attrib["type"] = "vector"
            self.simple_composite_param("radius", radius, elem, "real")
            self.simple_composite_param("theta", theta, elem, "angle")

        which_point = "in_point"
        self.process_vector_ext("t1", lottie_path.vertices.keyframes, composite, "radial_composite", get_tangent)
        which_point = "out_point"
        self.process_vector_ext("t2", lottie_path.vertices.keyframes, composite, "radial_composite", get_tangent)

    def group_builder_to_sif(self, shape_group, dom_parent):
        if shape_group.empty():
            return

        if shape_group.atomic() and len(shape_group.paths) == 1:
            layers = self.group_builder_path_to_sif(shape_group.paths[0], shape_group, dom_parent)
            if shape_group.lottie.name:
                for layer in layers:
                    layer.attrib["desc"] = shape_group.lottie.name
            return

        layer = self.layer_from_lottie("group", shape_group.lottie, dom_parent)

        pcanv = ElementTree.SubElement(layer, "param")
        pcanv.attrib["name"] = "canvas"
        canvas = ElementTree.SubElement(pcanv, "canvas")
        self.group_builder_process_children(shape_group, canvas)


def to_sif(animation):
    builder = SifBuilder()
    builder.process(animation)
    return builder.dom
