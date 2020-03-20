from xml.dom import minidom
import copy
import enum

from .core_nodes import XmlDescriptor, ObjectRegistry, XmlSimpleElement
from .utils import *
from tgs import NVector


def noop(x):
    return x


class TypeDescriptor:
    _type_tag_names = {
        "bone_object": "bone"
    }

    def __init__(self, typename, default=None, type_wrapper=noop):
        self.typename = typename
        self.type_wrapper = type_wrapper
        self.default_value = default

    def value_to_xml_element(self, value, dom: minidom.Document):
        element = dom.createElement(self.tag_name)

        if self.typename == "vector":
            element.appendChild(xml_make_text(dom, "x", str(value.x)))
            element.appendChild(xml_make_text(dom, "y", str(value.y)))
            if hasattr(value, "guid"):
                element.setAttribute("guid", value.guid)
        elif self.typename == "color":
            element.appendChild(xml_make_text(dom, "r", str(value[0])))
            element.appendChild(xml_make_text(dom, "g", str(value[1])))
            element.appendChild(xml_make_text(dom, "b", str(value[2])))
            element.appendChild(xml_make_text(dom, "a", str(value[3])))
        elif self.typename == "gradient":
            for point in value:
                element.appendChild(point.to_dom(dom))
        elif self.typename == "bool":
            element.setAttribute("value", "true" if value else "false")
        elif self.typename == "bone_object":
            element.setAttribute("guid", value.guid)
            element.setAttribute("type", self.typename)
        elif self.typename == "string":
            element.appendChild(dom.createTextNode(value))
        else:
            if isinstance(value, enum.Enum):
                value = value.value
            element.setAttribute("value", str(value))

        return element

    @property
    def tag_name(self):
        return self._type_tag_names.get(self.typename, self.typename)

    def value_from_xml_element(self, xml: minidom.Element, registry: ObjectRegistry):
        if xml.tagName != self.tag_name:
            raise ValueError("Wrong value type (%s instead of %s)" % (xml.tagName, self.tag_name))

        guid = xml.getAttribute("guid")
        if guid and guid in registry.registry:
            value = registry.registry[guid]
        elif self.typename == "vector":
            value = NVector(
                float(xml_text(xml.getElementsByTagName("x")[0])),
                float(xml_text(xml.getElementsByTagName("y")[0]))
            )
            if xml.getAttribute("guid"):
                value.guid = xml.getAttribute("guid")
                registry.register(value)
        elif self.typename == "color":
            value = NVector(
                float(xml_text(xml.getElementsByTagName("r")[0])),
                float(xml_text(xml.getElementsByTagName("g")[0])),
                float(xml_text(xml.getElementsByTagName("b")[0])),
                float(xml_text(xml.getElementsByTagName("a")[0]))
            )
        elif self.typename == "gradient":
            value = [
                GradientPoint.from_dom(sub, registry)
                for sub in xml_child_elements(xml, GradientPoint.type.typename)
            ]
        elif self.typename == "real" or self.typename == "angle":
            value = float(xml.getAttribute("value"))
        elif self.typename == "integer":
            value = int(xml.getAttribute("value"))
        elif self.typename == "time":
            value = FrameTime(xml.getAttribute("value"))
        elif self.typename == "bool":
            value = str_to_bool(xml.getAttribute("value"))
        elif self.typename == "string":
            return xml_text(xml)
        elif self.typename == "bone_object":
            # Already done above but this forces the guid to be present
            return registry.get_object(xml.getAttribute("guid"))
        else:
            raise ValueError("Unsupported type %s" % self.typename)

        return self.type_wrapper(value)


class XmlAnimatable(XmlDescriptor):
    def __init__(self, name, typename, default=None, type_wrapper=noop):
        super().__init__(name)
        self.type = TypeDescriptor(typename, default, type_wrapper)

    def from_xml(self, obj, parent: minidom.Element, registry: ObjectRegistry):
        cn = xml_first_element_child(parent, self.name)
        if cn:
            value = SifAstNode.from_dom(xml_first_element_child(cn), self.type, registry)
        else:
            value = self.default()

        setattr(obj, self.att_name, value)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        param = parent.appendChild(dom.createElement(self.name))
        param.appendChild(getattr(obj, self.att_name).to_dom(dom, self.type))
        return param

    def from_python(self, value):
        if not isinstance(value, SifAstNode):
            raise ValueError("%s isn't a valid value for %s" % (value, self.name))
        return value

    def default(self):
        return SifValue(copy.deepcopy(self.type.default_value))


class XmlParam(XmlDescriptor):
    def __init__(self, name, typename, default=None, type_wrapper=noop, static=False):
        super().__init__(name)
        self.type = TypeDescriptor(typename, default, type_wrapper)
        self.static = static

    def _def(self):
        from ..api import Def
        return Def

    def from_xml(self, obj, parent: minidom.Element, registry: ObjectRegistry):
        for cn in xml_child_elements(parent, "param"):
            if cn.getAttribute("name") == self.name:
                use = cn.getAttribute("use")
                if use:
                    value = registry.get_object(use)
                else:
                    value_node = xml_first_element_child(cn)
                    if self.static:
                        value = self.type.value_from_xml_element(value_node, registry)
                    else:
                        value = SifAstNode.from_dom(value_node, self.type, registry)
                break
        else:
            value = self.default()

        setattr(obj, self.att_name, value)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        param = parent.appendChild(dom.createElement("param"))
        param.setAttribute("name", self.name)
        value = getattr(obj, self.att_name)
        if isinstance(value, self._def()):
            param.setAttribute("use", value.id)
        else:
            if self.static:
                elem = self.type.value_to_xml_element(value, dom)
            else:
                elem = value.to_dom(dom, self.type)
            param.appendChild(elem)
        return param

    def from_python(self, value):
        if self.static:
            return self.type.type_wrapper(value)
        if not isinstance(value, (SifAstNode, self._def())):
            raise ValueError("%s isn't a valid value for %s" % (value, self.name))
        return value

    def default(self):
        if self.static:
            return copy.deepcopy(self.type.default_value)
        return SifValue(copy.deepcopy(self.type.default_value))


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

    def __eq__(self, other):
        return self.value == other.value and self.unit == other.unit

    def __ne__(self, other):
        return self.value == other.value and self.unit == other.unit

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


class SifKeyframe:
    def __init__(self, value, time: FrameTime, ease_in=Interpolation.Clamped, ease_out=Interpolation.Clamped):
        self.value = value
        self.time = time
        self.ease_in = ease_in
        self.ease_out = ease_out

    @classmethod
    def from_dom(cls, xml: minidom.Element, param: TypeDescriptor, registry: ObjectRegistry):
        return cls(
            param.value_from_xml_element(xml_first_element_child(xml), registry),
            FrameTime(xml.getAttribute("time")),
            Interpolation(xml.getAttribute("before")),
            Interpolation(xml.getAttribute("after"))
        )

    def to_dom(self, dom: minidom.Document, param: TypeDescriptor):
        element = dom.createElement("waypoint")
        element.setAttribute("time", str(self.time))
        element.setAttribute("before", self.ease_in.value)
        element.setAttribute("after", self.ease_out.value)
        element.appendChild(param.value_to_xml_element(self.value, dom))
        return element

    def __repr__(self):
        return "<SifKeyframe %s %s>" % (self.time, self.value)


class SifAstNode:
    _subclasses = None
    _tag = None

    @staticmethod
    def from_dom(xml: minidom.Element, param: TypeDescriptor, registry: ObjectRegistry):
        if xml.tagName == param.typename:
            return SifValue.from_dom(xml, param, registry)

        xmltype = xml.getAttribute("type")
        if xmltype != param.typename and xmltype != "weighted_" + param.typename:
            raise ValueError("Invalid type %s (should be %s)" % (xmltype, param.typename))

        return SifAstNode.ast_node_types()[xml.tagName].from_dom(xml, param, registry)

    @staticmethod
    def ast_node_types():
        if SifAstNode._subclasses is None:
            SifAstNode._subclasses = {}
            SifAstNode._gather_ast_types(SifAstNode)
        return SifAstNode._subclasses

    @staticmethod
    def _gather_ast_types(cls):
        for subcls in cls.__subclasses__():
            if subcls._tag:
                SifAstNode._subclasses[subcls._tag] = subcls
            SifAstNode._gather_ast_types(subcls)

    def _prepare_to_dom(self, dom: minidom.Document, param: TypeDescriptor):
        element = dom.createElement(self._tag)
        element.setAttribute("type", param.typename)
        return element


class SifValue(SifAstNode):
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.value)

    @classmethod
    def from_dom(cls, xml: minidom.Element, param: TypeDescriptor, registry: ObjectRegistry):
        return SifValue(param.value_from_xml_element(xml, registry))

    def to_dom(self, dom: minidom.Document, param: TypeDescriptor):
        return param.value_to_xml_element(self.value, dom)


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


class SifAstComplex(SifAstNode, metaclass=SifNodeMeta):
    _nodes = []

    def __init__(self, **kw):
        for node in self._nodes:
            node.initialize_object(kw, self)

    @classmethod
    def from_dom(cls, xml: minidom.Element, param: TypeDescriptor, registry: ObjectRegistry):
        instance = cls()
        for node in cls._nodes:
            node.from_xml(instance, xml, registry)
        return instance

    def to_dom(self, dom: minidom.Document, param: TypeDescriptor):
        element = self._prepare_to_dom(dom, param)
        for node in self._nodes:
            node.to_xml(self, element, dom)
        return element


class SifAdd(SifAstComplex):
    _tag = "add"

    _nodes = [
        XmlAnimatable("lhs", "vector"),
        XmlAnimatable("rhs", "vector"),
        XmlAnimatable("scalar", "real"),
    ]


class SifAnimated(SifAstNode):
    _tag = "animated"

    def __init__(self):
        self.keyframes = []

    @classmethod
    def from_dom(cls, xml: minidom.Element, param: TypeDescriptor, registry: ObjectRegistry):
        obj = SifAnimated()
        for waypoint in xml_child_elements(xml, "waypoint"):
            obj.keyframes.append(SifKeyframe.from_dom(waypoint, param, registry))
        return obj

    def to_dom(self, dom: minidom.Document, param: TypeDescriptor):
        element = self._prepare_to_dom(dom, param)
        for kf in self.keyframes:
            element.appendChild(kf.to_dom(dom, param))
        return element

    def add_keyframe(self, *args, **kwargs):
        if not kwargs and len(args) == 1 and isinstance(args[0], SifKeyframe):
            keyframe = args[0]
        else:
            keyframe = SifKeyframe(*args, **kwargs)

        self.keyframes.append(keyframe)


class SifAnimatedFile(SifAstComplex):
    _tag = "animated_file"

    _nodes = [
        XmlAnimatable("filename", "string"),
    ]


class SifAnimatedFile(SifAstComplex):
    _tag = "animated_file"

    _nodes = [
        XmlAnimatable("filename", "string"),
    ]


class Accuracy(enum.Enum):
    Rough = 0
    Normal = 1
    Fine = 2
    Extreme = 3


class DerivativeOrder:
    FirstDerivative = 0
    SecondDerivative = 1


class SifDerivative(SifAstComplex):
    _tag = "derivative"

    _nodes = [
        XmlAnimatable("link", "vector"),
        XmlAnimatable("interval", "real", 0.01),
        XmlAnimatable("accuracy", "integer", Accuracy.Normal, Accuracy),
        XmlAnimatable("order", "integer", DerivativeOrder.FirstDerivative, DerivativeOrder),
    ]


class SifDynamic(SifAstComplex):
    _tag = "dynamic"

    _nodes = [
        XmlAnimatable("tip_static", "vector"),
        XmlAnimatable("origin", "vector"),
        XmlAnimatable("force", "vector"),
        XmlAnimatable("torque", "real", 0.),
        XmlAnimatable("damping", "real", 0.4),
        XmlAnimatable("friction", "real", 0.4),
        XmlAnimatable("spring", "real", 30.),
        XmlAnimatable("torsion", "real", 30.),
        XmlAnimatable("mass", "real", 0.3),
        XmlAnimatable("inertia", "real", 0.3),
        XmlAnimatable("spring_rigid", "bool", False),
        XmlAnimatable("torsion_rigid", "bool", False),
        XmlAnimatable("origin_drags_tip", "bool", True),
    ]


class SifGreyed(SifAstComplex):
    _tag = "greyed"

    _nodes = [
        XmlAnimatable("link", "vector"),
    ]


class SifLinear(SifAstComplex):
    _tag = "linear"

    _nodes = [
        XmlAnimatable("slope", "vector"),
        XmlAnimatable("offset", "vector"),
    ]


class SifLinear(SifAstComplex):
    _tag = "linear"

    _nodes = [
        XmlAnimatable("slope", "vector"),
        XmlAnimatable("offset", "vector"),
    ]


class SifRadialComposite(SifAstComplex):
    _tag = "radial_composite"

    _nodes = [
        XmlAnimatable("radius", "real", 0.),
        XmlAnimatable("theta", "angle", 0.),
    ]


class InterpolationType(enum.Enum):
    NearestNeighbour = 0
    Linear = 1
    Cosine = 2
    Spline = 3
    Cubic = 4


class SifRandom(SifAstComplex):
    _tag = "random"

    _nodes = [
        XmlAnimatable("link", "vector"),
        XmlAnimatable("radius", "real", 0.),
        XmlAnimatable("seed", "integer", 0),
        XmlAnimatable("speed", "real", 1.),
        XmlAnimatable("smooth", "integer", InterpolationType.Cubic, InterpolationType),
        XmlAnimatable("loop", "real", 0.),
    ]


class SifReference(SifAstComplex):
    _tag = "link"

    _nodes = [
        XmlAnimatable("reference", "vector"),
    ]


class SifScale(SifAstComplex):
    _tag = "scale"

    _nodes = [
        XmlAnimatable("reference", "vector"),
        XmlAnimatable("scalar", "real", 1.),
    ]


class XmlDynamicListParam(XmlDescriptor):
    _tag = "dynamic_list"

    def __init__(self, name, typename, att_name=None):
        super().__init__(name)
        self.type = TypeDescriptor(typename)
        if att_name is not None:
            self.att_name = att_name

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        param = parent.appendChild(dom.createElement("param"))
        param.setAttribute("name", self.name)
        dyl = param.appendChild(dom.createElement(self._tag))
        dyl.setAttribute("type", self.type.typename)
        values = getattr(obj, self.att_name)
        for val in values:
            entry = dyl.appendChild(dom.createElement("entry"))
            entry.appendChild(self._value_to_dom(val, dom))

    def _value_to_dom(self, val, dom: minidom.Document):
        return val.to_dom(dom, self.type)

    def from_xml(self, obj, parent: minidom.Element, registry: ObjectRegistry):
        values = []

        for cn in xml_child_elements(parent, "param"):
            if cn.getAttribute("name") == self.name:
                list = xml_first_element_child(cn)
                if list.getAttribute("type") != self.type.typename:
                    raise ValueError(
                        "Wrong type for %s: got %s instead of %s" %
                        (self.name, self.type.typename, list.getAttribute("type"))
                    )
                for entry in xml_child_elements(list, "entry"):
                    values.append(self._value_from_dom(xml_first_element_child(entry), registry))
                break

        setattr(obj, self.att_name, values)

    def _value_from_dom(self, element, registry):
        return SifAstNode.from_dom(element, self.type, registry)

    def from_python(self, value):
        return value

    def default(self):
        return []


class XmlStaticListParam(XmlDynamicListParam):
    _tag = "static_list"

    def _value_to_dom(self, val, dom: minidom.Document):
        return self.type.value_to_xml_element(val, dom)

    def _value_from_dom(self, element: minidom.Element, registry: ObjectRegistry):
        return self.type.value_from_xml_element(element, registry)


class GradientPoint:
    type = TypeDescriptor("color")

    def __init__(self, pos: float, color: NVector):
        self.pos = pos
        self.color = color

    def to_dom(self, dom: minidom.Document):
        element = self.type.value_to_xml_element(self.color, dom)
        element.setAttribute("pos", value_to_xml_string(self.pos, float))
        return element

    @classmethod
    def from_dom(cls, xml: minidom.Element, registry: ObjectRegistry):
        return GradientPoint(
            value_from_xml_string(xml.getAttribute("pos"), float),
            cls.type.value_from_xml_element(xml, registry)
        )

    def __repr__(self):
        return "<GradientPoint %s %s>" % (self.pos, self.color)


class SifStep(SifAstComplex):
    _tag = "step"

    _nodes = [
        XmlAnimatable("link", "vector"),
        XmlAnimatable("duration", "time", FrameTime(1, FrameTime.Unit.Seconds)),
        XmlAnimatable("start_time", "time", FrameTime(0, FrameTime.Unit.Seconds)),
        XmlAnimatable("intersection", "real", 0.5),
    ]


class SifSubtract(SifAstComplex):
    _tag = "subtract"

    _nodes = [
        XmlAnimatable("lhs", "vector"),
        XmlAnimatable("rhs", "vector"),
        XmlAnimatable("scalar", "real", 1.),
    ]


class SifSwitch(SifAstComplex):
    _tag = "switch"

    _nodes = [
        XmlAnimatable("link_off", "vector"),
        XmlAnimatable("link_on", "vector"),
        XmlAnimatable("switch", "bool", False),
    ]


class SifTimedSwap(SifAstComplex):
    _tag = "timed_swap"

    _nodes = [
        XmlAnimatable("before", "vector"),
        XmlAnimatable("after", "vector"),
        XmlAnimatable("time", "time", FrameTime(0, FrameTime.Unit.Seconds)),
        XmlAnimatable("length", "time", FrameTime(0, FrameTime.Unit.Seconds)),
    ]


class SifTimeLoop(SifAstComplex):
    _tag = "timeloop"

    _nodes = [
        XmlAnimatable("link", "vector"),
        XmlAnimatable("link_time", "time", FrameTime(0, FrameTime.Unit.Seconds)),
        XmlAnimatable("local_time", "time", FrameTime(0, FrameTime.Unit.Seconds)),
        XmlAnimatable("duration", "time", FrameTime(0, FrameTime.Unit.Seconds)),
    ]

