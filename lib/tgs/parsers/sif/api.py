import enum
from uuid import uuid4
from .xml.utils import *
from .xml.core_nodes import *
from .xml.animatable import *
from .xml.wrappers import *


class SifNodeMeta(type):
    def __new__(cls, name, bases, attr):
        props = []
        for base in bases:
            if type(base) == cls:
                props += base._nodes
        attr["_nodes"] = props + attr.get("_nodes", [])
        if "_tag" not in attr:
            attr["_tag"] = name.lower()
        attr["_nodemap"] = {
            node.att_name: node
            for node in attr["_nodes"]
        }
        return super().__new__(cls, name, bases, attr)


class SifNode(metaclass=SifNodeMeta):
    def __init__(self, **kw):
        for node in self._nodes:
            node.initialize_object(kw, self)

    def __setattr__(self, name, value):
        if name in self._nodemap:
            value = self._nodemap[name].clean(value)
        return super().__setattr__(name, value)

    @staticmethod
    def static_from_dom(cls, xml: minidom.Element):
        instance = cls()
        for node in cls._nodes:
            node.from_xml(instance, xml)
        return instance

    @classmethod
    def from_dom(cls, xml: minidom.Element):
        return SifNode.static_from_dom(cls, xml)

    def to_dom(self, dom: minidom.Document):
        element = dom.createElement(self._tag)
        for node in self._nodes:
            node.to_xml(self, element, dom)
        return element


class SifTransform(SifNode):
    _nodes = [
        XmlAnimatable("offset", "vector", NVector(0, 0)),
        XmlAnimatable("angle", "angle", 0.),
        XmlAnimatable("skew_angle", "angle", 0.),
        XmlAnimatable("scale", "vector", NVector(1, 1)),
    ]

    @classmethod
    def from_dom(cls, xml: minidom.Element):
        if xml.tagName != "composite" or xml.getAttribute("type") != "transformation":
            raise ValueError("Invalid transform element: %s" % xml.tagName)
        return super().from_dom(xml)

    def to_dom(self, dom: minidom.Document):
        element = dom.createElement("composite")
        element.setAttribute("type", "transformation")
        for node in self._nodes:
            node.to_xml(self, element, dom)
        return element


class RadialComposite(SifNode):
    _nodes = [
        XmlAnimatable("radius", "real", 0.),
        XmlAnimatable("theta", "angle", 0.),
    ]

    def to_dom(self, dom: minidom.Document):
        element = dom.createElement("radial_composite")
        element.setAttribute("type", "vector")
        for node in self._nodes:
            node.to_xml(self, element, dom)
        return element


class BlinePoint(SifNode):
    _nodes = [
        XmlAnimatable("point", "vector", NVector(0, 0)),
        XmlAnimatable("width", "real", 1.),
        XmlAnimatable("origin", "real", .5),
        XmlAnimatable("split", "bool", False),
        XmlSifElement("t1", RadialComposite),
        XmlSifElement("t2", RadialComposite),
        XmlAnimatable("split_radius", "bool", True),
        XmlAnimatable("split_angle", "bool", False),
    ]

    def to_dom(self, dom: minidom.Document):
        element = dom.createElement("composite")
        element.setAttribute("type", "bline_point")
        for node in self._nodes:
            node.to_xml(self, element, dom)
        return element


class Bline(SifNode):
    _nodes = [
        XmlAttribute("loop", bool_str, False),
        XmlAttribute("type", str, "bline_point"),
        XmlList(BlinePoint, "points", "entry"),
    ]


class BlendMethod(enum.Enum):
    Composite = 0
    Multiply = 6
    Screen = 16
    Overlay = 20
    Darken = 3
    Lighten = 2
    HardLight = 17
    Difference = 18
    Hue = 9
    Saturation = 10
    Color = 8
    Luminosity = 11
    Exclusion = 18
    SoftLight = 6
    ColorDodge = 0
    ColorBurn = 0
    Straight = 1
    Onto = 13
    StraightOnto = 21
    Behind = 12
    Divide = 7
    Add = 4
    Subtract = 5


class BlurType(enum.Enum):
    Box = 0
    FastGaussian = 1
    CrossHatch = 2
    Gaussian = 3
    Disc = 4


class WindingStyle(enum.Enum):
    NonZero = 0
    EvenOdd = 1


class Layer(SifNode):
    _types = None

    _layer_type = None

    _nodes = [
        XmlAttribute("type", str),
        XmlAttribute("active", bool_str, True),
        XmlAttribute("version", str, "0.3"),
        XmlAttribute("exclude_from_rendering", bool_str, False),
        XmlAttribute("desc", str, ""),
    ]

    def __init__(self, **kw):
        super().__init__(**kw)
        self.type = self._layer_type

    def __repr__(self):
        return "<%s.%s %r>" % (__name__, self.__class__.__name__, self.desc or self.type)

    def to_dom(self, dom: minidom.Document):
        element = dom.createElement("layer")
        for node in self._nodes:
            node.to_xml(self, element, dom)
        return element

    @classmethod
    def from_dom(cls, xml: minidom.Element):
        actual_class = cls
        if cls == Layer:
            type = xml.getAttribute("type")
            actual_class = Layer.layer_types().get(type, Layer)

        return SifNode.static_from_dom(actual_class, xml)

    @staticmethod
    def layer_types():
        if Layer._types is None:
            Layer._types = {}
            Layer._gather_layer_types(Layer)
        return Layer._types

    @staticmethod
    def _gather_layer_types(cls):
        for subcls in cls.__subclasses__():
            if subcls._layer_type:
                Layer._types[subcls._layer_type] = subcls
            Layer._gather_layer_types(subcls)


class DrawableLayer(Layer):
    _nodes = [
        XmlParam("z_depth", "real", 0.),
        XmlParam("amount", "real", 1.),
        XmlParam("blend_method", "integer", BlendMethod.Composite, False, BlendMethod),
    ]


class GroupLayer(DrawableLayer):
    _layer_type = "group"

    _nodes = [
        XmlParam("origin", "vector", NVector(0, 0)),
        XmlParamSif("transformation", SifTransform),
        XmlWrapperParam("canvas", XmlWrapper("canvas", XmlList(Layer))),
        XmlParam("time_dilation", "real", 0.),
        XmlParam("time_offset", "time", FrameTime(0, FrameTime.Unit.Frame)),
        XmlParam("children_lock", "bool", False),
        XmlParam("outline_grow", "real", 0.),
        XmlParam("z_range", "bool", False, True),
        XmlParam("z_range_position", "real", 0.),
        XmlParam("z_range_depth", "real", 0.),
        XmlParam("z_range_blur", "real", 0.),
    ]


class RectangleLayer(DrawableLayer):
    _layer_type = "rectangle"

    _nodes = [
        XmlParam("color", "color", NVector(0, 0, 0, 1)),
        XmlParam("point1", "vector", NVector(0, 0)),
        XmlParam("point2", "vector", NVector(0, 0)),
        XmlParam("expand", "real", 0.),
        XmlParam("invert", "bool", False),
        XmlParam("feather_x", "real", 0.),
        XmlParam("feather_y", "real", 0.),
        XmlParam("bevel", "real", 0.),
        XmlParam("bevCircle", "bool", True),
    ]


class CircleLayer(DrawableLayer):
    _layer_type = "circle"

    _nodes = [
        XmlParam("color", "color", NVector(0, 0, 0, 1)),
        XmlParam("radius", "real", 0.),
        XmlParam("feather", "real", 0.),
        XmlParam("origin", "vector", NVector(0, 0)),
        XmlParam("invert", "bool", False),
    ]


class ComplexShape(DrawableLayer):
    _nodes = [
        XmlParam("color", "color", NVector(0, 0, 0, 1)),
        XmlParam("origin", "vector", NVector(0, 0)),
        XmlParam("invert", "bool", False),
        XmlParam("antialias", "bool", False),
        XmlParam("feather", "real", 0.),
        XmlParam("blurtype", "integer", BlurType.FastGaussian, False, BlurType),
        XmlParam("winding_style", "integer", WindingStyle.NonZero, False, WindingStyle),
    ]


class StarLayer(ComplexShape):
    _layer_type = "star"

    _nodes = [
        XmlParam("radius1", "real", 0.),
        XmlParam("radius2", "real", 0.),
        XmlParam("angle", "angle", 0.),
        XmlParam("points", "integer", 5),
        XmlParam("regular_polygon", "bool", False),
    ]


class LineCap(enum.Enum):
    Rounded = 1
    Squared = 2
    Peak = 3
    Flat = 4
    InnerRounded = 5
    OffPeak = 6


class CuspStyle(enum.Enum):
    Miter = 0
    Round = 1
    Bevel = 2


class AbstractOutline(ComplexShape):
    _nodes = [
        XmlParam("width", "real", 0.1),
        XmlParam("expand", "real", 0.),
        XmlParamSif("bline", Bline),
    ]


class OutlineLayer(AbstractOutline):
    _layer_type = "outline"

    _nodes = [
        XmlParam("sharp_cusps", "bool", True),
        XmlParam("round_tip[0]", "bool", True),
        XmlParam("round_tip[1]", "bool", True),
        XmlParam("homogeneous_width", "bool", True),
    ]

    @property
    def start_tip(self):
        return LineCap.Rounded if self.round_tip_0 else LineCap.Flat

    @property
    def end_tip(self):
        return LineCap.Rounded if self.round_tip_1 else LineCap.Flat

    @property
    def cusp_type(self):
        return CuspStyle.Miter if self.sharp_cusps else CuspStyle.Round


class AdvancedOutlineLayer(AbstractOutline):
    _layer_type = "advanced_outline"

    _nodes = [
        XmlParam("start_tip", "integer", LineCap.Rounded, False, LineCap),
        XmlParam("end_tip", "integer", LineCap.Rounded, False, LineCap),
        XmlParam("cusp_type", "integer", CuspStyle.Miter, False, CuspStyle),
        XmlParam("smoothness", "real", 1.),
        XmlParam("homogeneous", "bool", False),
        # TODO wplist
    ]


class PolygonLayer(ComplexShape):
    _layer_type = "polygon"

    _nodes = [
        XmlDynamicListParam("vector_list", "vector", "points"),
    ]


class RegionLayer(ComplexShape):
    _layer_type = "region"

    _nodes = [
        XmlParamSif("bline", Bline),
    ]


class TransformDown(Layer):
    pass


class TranslateLayer(TransformDown):
    _layer_type = "translate"

    _nodes = [
        XmlParam("origin", "vector", NVector(0, 0)),
    ]


class RotateLayer(TransformDown):
    _layer_type = "rotate"

    _nodes = [
        XmlParam("origin", "vector", NVector(0, 0)),
        XmlParam("amount", "angle", 0.),
    ]


class ScaleLayer(TransformDown):
    _layer_type = "zoom"

    _nodes = [
        XmlParam("center", "vector", NVector(0, 0)),
        XmlParam("amount", "real", 0.),
    ]


class Canvas(SifNode):
    _nodes = [
        XmlAttribute("version"),
        XmlAttribute("width", float, 512),
        XmlAttribute("height", float, 512),
        XmlAttribute("xres", float, 2834.645752),
        XmlAttribute("yres", float, 2834.645752),
        XmlAttribute("gamma-r", float, 2.200000),
        XmlAttribute("gamma-g", float, 2.200000),
        XmlAttribute("gamma-b", float, 2.200000),
        XmlAttribute("view-box", NVector),
        XmlAttribute("antialias", bool, True),
        XmlAttribute("fps", float, 60),
        XmlAttribute("begin-time", FrameTime, FrameTime(0, FrameTime.Unit.Frame)),
        XmlAttribute("end-time", FrameTime, FrameTime(3, FrameTime.Unit.Seconds)),
        XmlAttribute("bgcolor", NVector, NVector(0, 0, 0, 0)),
        XmlSimpleElement("name"),
        XmlMeta("background_first_color", NVector, NVector(0.88, 0.88, 0.88)),
        XmlMeta("background_rendering", bool, False),
        XmlMeta("background_second_color", NVector, NVector(0.65, 0.65, 0.65)),
        XmlMeta("background_size", NVector, NVector(15, 15)),
        XmlMeta("grid_color", NVector, NVector(0.62, 0.62, 0.62)),
        XmlMeta("grid_show", bool, False),
        XmlMeta("grid_size", NVector, NVector(0.25, 0.25)),
        XmlMeta("grid_snap", bool, False),
        XmlMeta("guide_color", NVector, NVector(0.4, 0.4, 1)),
        XmlMeta("guide_show", bool, True),
        XmlMeta("guide_snap", bool, False),
        XmlMeta("jack_offset", float, 0),
        XmlMeta("onion_skin", bool, False),
        XmlMeta("onion_skin_future", int, 0),
        XmlMeta("onion_skin_past", int, 1),
        XmlList(Layer),
    ]

    def __init__(self, **kw):
        super().__init__(**kw)
        self.registry = {}

    def register(self, object):
        guid = getattr(object, "guid", None)
        if guid is None:
            guid = Canvas.guid()
            object.guid = guid
        self.registry[guid] = object

    def to_xml(self):
        dom = minidom.Document()
        dom.appendChild(self.to_dom(dom))
        return dom

    @classmethod
    def from_xml_file(cls, xml):
        if isinstance(xml, str):
            xml = open(xml, "r")
        return cls.from_xml(minidom.parse(xml))

    @classmethod
    def from_xml_string(cls, xml):
        return cls.from_xml(minidom.parseString(xml))

    @classmethod
    def from_xml(cls, xml: minidom.Document):
        obj = cls.from_dom(xml.documentElement)
        xml.unlink()
        return obj

    def time_to_frames(self, time: FrameTime):
        if time.unit == FrameTime.Unit.Frame:
            return time.value
        elif time.unit == FrameTime.Unit.Seconds:
            return time.value * self.fps

    @classmethod
    def guid(cls):
        return str(uuid4()).replace("-", "").upper()
