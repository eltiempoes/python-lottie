import enum
from uuid import uuid4
from xml.dom import minidom
from distutils.util import strtobool
import copy

from ...nvector import NVector, Color


class _tag:
    def __init__(self, type):
        self.type = type

    def __call__(self, v):
        return self.type(v)


bool_str = _tag(bool)


def value_from_xml(xml_str, type):
    if type in (bool_str, bool):
        return bool(strtobool(xml_str))
    elif type is NVector:
        return NVector(*map(float, xml_str.split()))
    return type(xml_str)


def value_to_xml(value, type):
    if type is bool:
        return "1" if value else "0"
    if type is bool_str:
        return "true" if value else "false"
    elif type is NVector:
        return " ".join(map(str, value))
    return str(value)


def value_isinstance(value, type):
    if isinstance(type, _tag):
        type = type.type
    return isinstance(value, type)


def xml_text(node):
    return "".join(
        x.nodeValue
        for x in node.childNodes
        if x.nodeType in {minidom.Node.TEXT_NODE, minidom.Node.CDATA_SECTION_NODE}
    )


def xml_make_text(dom: minidom.Document, tag_name, text):
    e = dom.createElement(tag_name)
    e.appendChild(dom.createTextNode(text))
    return e


def xml_first_element_child(xml: minidom.Node):
    for ch in xml.childNodes:
        if ch.nodeType == minidom.Node.ELEMENT_NODE:
            return ch

    raise ValueError("No child element in %s" % getattr(xml, "tagName", "node"))


class XmlDescriptor:
    def __init__(self, name, default_value=None):
        self.name = name
        self.att_name = name.replace("-", "_")

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        raise NotImplementedError

    def from_xml(self, obj, parent: minidom.Element):
        raise NotImplementedError

    def from_python(self, value):
        raise NotImplementedError

    def initialize_object(self, dict, obj):
        if self.att_name in dict:
            setattr(obj, self.att_name, self.from_python(dict[self.att_name]))
        else:
            setattr(obj, self.att_name, self.default())

    def clean(self, value):
        return self.from_python(value)

    def default(self):
        return None

    def __repr__(self):
        return "%s.%s(%r)" % (__name__, self.__class__, self.name)


class TypedXmlDescriptor(XmlDescriptor):
    def __init__(self, name, type=str, default_value=None):
        super().__init__(name, default_value)
        self.type = type
        self.default_value = default_value

    def from_python(self, value):
        if value is None and self.default_value is None:
            return None
        if not value_isinstance(value, self.type):
            return self.type(value)
        return value

    def default(self):
        return copy.deepcopy(self.default_value)


class XmlAttribute(TypedXmlDescriptor):
    def from_xml(self, obj, domnode: minidom.Element):
        xml_str = domnode.getAttribute(self.name)
        if xml_str:
            setattr(obj, self.att_name, value_from_xml(xml_str, self.type))

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        value = getattr(obj, self.att_name)
        if value is not None:
            parent.setAttribute(self.name, value_to_xml(value, self.type))


class XmlSimpleElement(TypedXmlDescriptor):
    def from_xml(self, obj, domnode: minidom.Element):
        for cn in domnode.childNodes:
            if cn.nodeType == minidom.Node.ELEMENT_NODE and cn.tagName == self.name:
                value = value_from_xml(xml_text(cn), self.type)
                break
        else:
            value = self.default_value

        setattr(obj, self.att_name, value)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        value = getattr(obj, self.att_name)
        if value is not None:
            parent.appendChild(xml_make_text(dom, self.name, value_to_xml(value, self.type)))


class XmlMeta(TypedXmlDescriptor):
    def from_xml(self, obj, domnode: minidom.Element):
        for cn in domnode.childNodes:
            if (
                cn.nodeType == minidom.Node.ELEMENT_NODE and cn.tagName == "meta"
                and cn.getAttribute("name") == self.name
            ):
                value = value_from_xml(cn.getAttribute("content"), self.type)
                break
        else:
            value = self.default_value

        setattr(obj, self.att_name, value)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        value = getattr(obj, self.att_name)
        if value is not None:
            meta = parent.appendChild(dom.createElement("meta"))
            meta.setAttribute("name", self.name)
            meta.setAttribute("content", value_to_xml(value, self.type))


class LayerList:
    def __init__(self):
        self._layers = []

    def __len__(self):
        return len(self._layers)

    def __iter__(self):
        return iter(self._layers)

    def __getitem__(self, name):
        return self._layers[name]

    def __getslice__(self, i, j):
        return self._layers[i:j]

    def __setitem__(self, key, value: "Layer"):
        self.validate(value)
        self._layers[key] = value

    def append(self, value: "Layer"):
        self.validate(value)
        self._layers.append(value)

    def __str__(self):
        return str(self._layers)

    def __repr__(self):
        return "<LayerList %s>" % self._layers

    def validate(self, value: "Layer"):
        if not isinstance(value, Layer):
            raise ValueError("Not a layer: %s" % value)


class XmlList(XmlDescriptor):
    def __init__(self, child_node, name=None):
        super().__init__(child_node._tag)
        self.child_node = child_node
        self.att_name = self.att_name + "s" if name is None else name

    def default(self):
        return LayerList()

    def clean(self, value):
        return value

    def from_xml(self, obj, domnode: minidom.Element):
        values = LayerList()
        for cn in domnode.childNodes:
            if cn.nodeType == minidom.Node.ELEMENT_NODE and cn.tagName == self.name:
                values.append(self.child_node.from_dom(cn))

        setattr(obj, self.att_name, values)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        for value in getattr(obj, self.att_name):
            parent.appendChild(value.to_dom(dom))


class AnimatableTypeDescriptor:
    def __init__(self, typename, default=None, static=False, type_wrapper=lambda x: x):
        self.typename = typename
        self.static = static
        self.type_wrapper = type_wrapper
        self.default_value = default

    def default(self):
        return SifAnimatable(self, copy.deepcopy(self.default_value))


class XmlAnimatable(AnimatableTypeDescriptor, XmlDescriptor):
    def __init__(self, name, *a, **kw):
        XmlDescriptor.__init__(self, name)
        AnimatableTypeDescriptor.__init__(self, *a, **kw)

    def from_xml(self, obj, parent: minidom.Element):
        for cn in parent.childNodes:
            if cn.nodeType == minidom.Node.ELEMENT_NODE and cn.tagName == self.name:
                value = SifAnimatable.from_dom(xml_first_element_child(cn), self)
                break
        else:
            value = self.default()

        setattr(obj, self.att_name, value)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        param = parent.appendChild(dom.createElement(self.name))
        param.appendChild(getattr(obj, self.att_name).to_dom(dom))
        return param

    def clean(self, value):
        if not isinstance(value, SifAnimatable) or value._param is not self:
            raise ValueError("%s isn't a valid value for %s" % (value, self.name))
        return value


class XmlParam(XmlAnimatable):
    def from_xml(self, obj, parent: minidom.Element):
        for cn in parent.childNodes:
            if (
                cn.nodeType == minidom.Node.ELEMENT_NODE and cn.tagName == "param"
                and cn.getAttribute("name") == self.name
            ):
                value = SifAnimatable.from_dom(xml_first_element_child(cn), self)
                break
        else:
            value = self.default()

        setattr(obj, self.att_name, value)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        param = parent.appendChild(dom.createElement("param"))
        param.setAttribute("name", self.name)
        param.appendChild(getattr(obj, self.att_name).to_dom(dom))
        return param


class XmlCompositeParam(XmlDescriptor):
    def from_xml(self, obj, parent: minidom.Element):
        for cn in parent.childNodes:
            if (
                cn.nodeType == minidom.Node.ELEMENT_NODE and cn.tagName == "param"
                and cn.getAttribute("name") == self.name
            ):
                value = SifTransform.from_dom(xml_first_element_child(cn))
                break
        else:
            value = self.default()

        setattr(obj, self.att_name, value)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        param = parent.appendChild(dom.createElement("param"))
        param.setAttribute("name", self.name)
        param.appendChild(getattr(obj, self.att_name).to_dom(dom))
        return param

    def clean(self, value):
        if not isinstance(value, SifTransform):
            raise ValueError("%s isn't a valid value for %s" % (value, self.name))
        return value

    def default(self):
        return SifTransform()


class XmlCanvasParam(XmlDescriptor):
    def __init__(self, name="canvas"):
        super().__init__(name)

    def from_xml(self, obj, parent: minidom.Element):
        value = LayerList()

        for cn in parent.childNodes:
            if (
                cn.nodeType == minidom.Node.ELEMENT_NODE and cn.tagName == "param"
                and cn.getAttribute("name") == self.name
            ):
                canvas = xml_first_element_child(cn)
                if canvas.tagName != "canvas":
                    raise ValueError("Missing canvas")
                for gc in canvas.childNodes:
                    if gc.nodeType == minidom.Node.ELEMENT_NODE and gc.tagName == "layer":
                        value.append(Layer.from_dom(gc))
                break

        setattr(obj, self.att_name, value)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        param = parent.appendChild(dom.createElement("param"))
        param.setAttribute("name", self.name)
        canvas = param.appendChild(dom.createElement("canvas"))
        value = getattr(obj, self.att_name)
        for layer in value:
            canvas.appendChild(layer.to_dom(dom))
        return param

    def clean(self, value):
        if not isinstance(value, LayerList):
            raise ValueError("%s isn't a valid value for %s" % (value, self.name))
        return value

    def default(self):
        return LayerList()


class FrameTime:
    class Unit(enum.Enum):
        Frame = "f"
        Seconds = "s"

    def __init__(self, value, unit=None):
        if isinstance(value, str) or unit is None:
            self.value = float(value[:-1])
            self.unit = self.Unit(value[-1])
        else:
            self.value = value
            self.unit = unit

    def __str__(self):
        return "%s%s" % (self.value, self.unit.value)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self)


class Interpolation(enum.Enum):
    Auto = "auto"
    Linear = "linear"
    Clamped = "clamped"
    Ease = "halt"
    Constant = "constant"


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


class SifKeyframe:
    def __init__(self, value, time: FrameTime, ease_in=Interpolation.Clamped, ease_out=Interpolation.Clamped):
        self.value = value
        self.time = time
        self.ease_in = ease_in
        self.ease_out = ease_out

    @classmethod
    def from_dom(cls, xml: minidom.Element, param: AnimatableTypeDescriptor):
        return cls(
            SifAnimatable.value_from_dom(xml_first_element_child(xml), param),
            FrameTime(xml.getAttribute("time")),
            Interpolation(xml.getAttribute("before")),
            Interpolation(xml.getAttribute("after"))
        )

    def to_dom(self, dom: minidom.Document, param: AnimatableTypeDescriptor):
        element = dom.createElement("waypoint")
        element.setAttribute("time", str(self.time))
        element.setAttribute("before", self.ease_in.value)
        element.setAttribute("after", self.ease_out.value)
        element.appendChild(SifAnimatable.value_to_dom(self.value, dom, param))
        return element


class SifAnimatable:
    def __init__(self, param: AnimatableTypeDescriptor, value=None):
        self._value = value
        self._animated = False
        self._keyframes = None
        self._param = param

    def __repr__(self):
        return "<%s.%s %r>" % (__name__, self.__class__.__name__, self._value if not self._animated else "animated")

    @classmethod
    def from_dom(cls, xml: minidom.Element, param: AnimatableTypeDescriptor):
        if xml.tagName == param.typename:
            return SifAnimatable(param, SifAnimatable.value_from_dom(xml, param))
        elif xml.tagName != "animated":
            raise ValueError("Unknown element %s for %s" % (xml.tagName, param.name))

        if xml.getAttribute("type") != param.typename:
            raise ValueError("Invalid type %s (should be %s)" % (xml.getAttribute("type"), param.typename))

        if param.static:
            raise ValueError("Animating static value for %s" % (param.name))

        obj = SifAnimatable(param)
        obj._animated = True
        obj._keyframes = []
        for waypoint in xml.childNodes:
            if waypoint.nodeType == minidom.Node.ELEMENT_NODE and waypoint.tagName == "waypoint":
                obj._keyframes.append(SifKeyframe.from_dom(waypoint, param))
        return obj

    def to_dom(self, dom: minidom.Document):
        if not self._animated:
            element = SifAnimatable.value_to_dom(self.value, dom, self._param)
            if self._param.static:
                element.setAttribute("static", "true")
            return element

        element = dom.createElement("animated")
        element.setAttribute("type", self._param.typename)
        for kf in self._keyframes:
            element.appendChild(kf.to_dom(dom, self._param))
        return element

    @classmethod
    def guid(cls):
        return str(uuid4()).replace("-", "").upper()

    @classmethod
    def value_to_dom(cls, value, dom: minidom.Document, param: AnimatableTypeDescriptor):
        element = dom.createElement(param.typename)

        if param.typename == "vector":
            element.appendChild(xml_make_text(dom, "x", str(value.x)))
            element.appendChild(xml_make_text(dom, "y", str(value.y)))
            element.setAttribute("guid", cls.guid())
        elif param.typename == "color":
            element.appendChild(xml_make_text(dom, "r", str(value[0])))
            element.appendChild(xml_make_text(dom, "g", str(value[1])))
            element.appendChild(xml_make_text(dom, "b", str(value[2])))
            element.appendChild(xml_make_text(dom, "a", str(value[3])))
            element.setAttribute("guid", cls.guid())
        elif param.typename == "bool":
            element.setAttribute("value", "true" if value else "false")
        else:
            if isinstance(value, enum.Enum):
                value = value.value
            element.setAttribute("value", str(value))

        return element

    @classmethod
    def value_from_dom(cls, xml: minidom.Element, param: AnimatableTypeDescriptor):
        if xml.tagName != param.typename:
            raise ValueError("Wrong value type (%s instead of %s)" % (xml.tagName, param.typename))

        if param.typename == "vector":
            value = NVector(
                float(xml_text(xml.getElementsByTagName("x")[0])),
                float(xml_text(xml.getElementsByTagName("y")[0]))
            )
        elif param.typename == "color":
            value = NVector(
                float(xml_text(xml.getElementsByTagName("r")[0])),
                float(xml_text(xml.getElementsByTagName("g")[0])),
                float(xml_text(xml.getElementsByTagName("b")[0])),
                float(xml_text(xml.getElementsByTagName("a")[0]))
            )
        elif param.typename == "real" or param.typename == "angle":
            value = float(xml.getAttribute("value"))
        elif param.typename == "integer":
            value = int(xml.getAttribute("value"))
        elif param.typename == "time":
            value = FrameTime(xml.getAttribute("value"))
        elif param.typename == "bool":
            value = bool(strtobool(xml.getAttribute("value")))
        else:
            raise ValueError("Unsupported type %s" % param.typename)

        return param.type_wrapper(value)

    def add_keyframe(self, *args, **kwargs):
        if self._static:
            raise ValueError("Cannot animate static value")
        if not kwargs and len(args) == 1 and isinstance(args[0], SifKeyframe):
            keyframe = args[0]
        else:
            keyframe = SifKeyframe(*args, **kwargs)

        if not self._animated:
            self._animated = True
            self._keyframes = [keyframe]
            self._value = None
        else:
            self._keyframes.append(keyframe)

    @property
    def static(self):
        return self._param.static

    @property
    def animated(self):
        return self._animated

    @animated.setter
    def animated(self, v):
        if v != self._animated:
            if self._param.static:
                raise ValueError("Cannot animate static value")
            self._animated = v
            if self._animated:
                self._keyframes = []
                if self._value is not None:
                    self._keyframes.append(SifKeyframe(self.value, FrameTime(0, FrameTime.Unit.Frame)))
                self._value = None
            else:
                if self._keyframes:
                    self._value = self._keyframes[0].value
                self._keyframes = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = self._param.type_wrapper(v)
        self._animated = False
        self._keyframes = None

    @property
    def keyframes(self):
        return self._keyframes


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


class Layer(SifNode):
    _layer_type = None

    _nodes = [
        XmlAttribute("type", str),
        XmlAttribute("active", bool_str, True),
        XmlAttribute("version", str, "0.3"),
        XmlAttribute("exclude_from_rendering", bool_str, False),
        XmlAttribute("desc", str, ""),
        XmlParam("z_depth", "real", 0.),
        XmlParam("amount", "real", 1.),
        XmlParam("blend_method", "integer", BlendMethod.Composite, False, BlendMethod),
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
            for subcls in Layer.__subclasses__():
                if subcls._layer_type == type:
                    actual_class = subcls
                    break

        return SifNode.static_from_dom(actual_class, xml)


class GroupLayer(Layer):
    _layer_type = "group"

    _nodes = [
        XmlParam("origin", "vector", NVector(0, 0)),
        XmlCompositeParam("transformation"),
        XmlCanvasParam(),
        XmlParam("time_dilation", "real", 0.),
        XmlParam("time_offset", "time", FrameTime(0, FrameTime.Unit.Frame)),
        XmlParam("children_lock", "bool", False),
        XmlParam("outline_grow", "real", 0.),
        XmlParam("z_range", "bool", False, True),
        XmlParam("z_range_position", "real", 0.),
        XmlParam("z_range_depth", "real", 0.),
        XmlParam("z_range_blur", "real", 0.),
    ]


class RectangleLayer(Layer):
    _layer_type = "rectangle"

    _nodes = [
        XmlParam("color", "color", NVector(0, 0, 0, 1)),
        XmlParam("point1", "vector", NVector(0, 0)),
        XmlParam("point2", "vector", NVector(0, 0)),
        XmlParam("invert", "bool", False),
        XmlParam("feather_x", "real", 0.),
        XmlParam("feather_y", "real", 0.),
        XmlParam("bevel", "real", 0.),
        XmlParam("bevCircle", "bool", True),
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
