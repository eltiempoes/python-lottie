from xml.dom import minidom
import copy
import enum

from .core_nodes import XmlDescriptor, ObjectRegistry
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

        if self.typename == "vector":
            value = NVector(
                float(xml_text(xml.getElementsByTagName("x")[0])),
                float(xml_text(xml.getElementsByTagName("y")[0]))
            )
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
            value = SifAnimatable.from_dom(xml_first_element_child(cn), self.type, registry)
        else:
            value = self.default()

        setattr(obj, self.att_name, value)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        param = parent.appendChild(dom.createElement(self.name))
        param.appendChild(getattr(obj, self.att_name).to_dom(dom, self.type))
        return param

    def from_python(self, value):
        if not isinstance(value, SifAnimatable):
            raise ValueError("%s isn't a valid value for %s" % (value, self.name))
        return value

    def default(self):
        return SifAnimatable(copy.deepcopy(self.type.default_value))


class XmlParam(XmlDescriptor):
    def __init__(self, name, typename, default=None, type_wrapper=noop, static=False):
        super().__init__(name)
        self.type = TypeDescriptor(typename, default, type_wrapper)
        self.static = static

    def from_xml(self, obj, parent: minidom.Element, registry: ObjectRegistry):
        for cn in xml_child_elements(parent, "param"):
            if cn.getAttribute("name") == self.name:
                value_node = xml_first_element_child(cn)
                if self.static:
                    value = self.type.value_from_xml_element(value_node, registry)
                else:
                    value = SifAnimatable.from_dom(value_node, self.type, registry)
                break
        else:
            value = self.default()

        setattr(obj, self.att_name, value)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        param = parent.appendChild(dom.createElement("param"))
        param.setAttribute("name", self.name)
        value = getattr(obj, self.att_name)
        if self.static:
            elem = self.type.value_to_xml_element(value, dom)
        else:
            elem = value.to_dom(dom, self.type)
        param.appendChild(elem)
        return param

    def from_python(self, value):
        if self.static:
            return self.type.type_wrapper(value)
        if not isinstance(value, SifAnimatable):
            raise ValueError("%s isn't a valid value for %s" % (value, self.name))
        return value

    def default(self):
        if self.static:
            return copy.deepcopy(self.type.default_value)
        return SifAnimatable(copy.deepcopy(self.type.default_value))


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


class SifAnimatable:
    def __init__(self, value=None):
        self._value = value
        self._animated = False
        self._keyframes = None

    def __repr__(self):
        return "<%s.%s %r>" % (__name__, self.__class__.__name__, self._value if not self._animated else "animated")

    @classmethod
    def from_dom(cls, xml: minidom.Element, param: TypeDescriptor, registry: ObjectRegistry):
        if xml.tagName == param.tag_name:
            return SifAnimatable(param.value_from_xml_element(xml, registry))
        elif xml.tagName != "animated":
            raise ValueError("Unknown element %s for %s" % (xml.tagName, param.typename))

        if xml.getAttribute("type") != param.typename:
            raise ValueError("Invalid type %s (should be %s)" % (xml.getAttribute("type"), param.typename))

        obj = SifAnimatable()
        obj._animated = True
        obj._keyframes = []
        for waypoint in xml_child_elements(xml, "waypoint"):
            obj._keyframes.append(SifKeyframe.from_dom(waypoint, param, registry))
        return obj

    def to_dom(self, dom: minidom.Document, param: TypeDescriptor):
        if not self._animated:
            element = param.value_to_xml_element(self.value, dom)
            return element

        element = dom.createElement("animated")
        element.setAttribute("type", param.typename)
        for kf in self._keyframes:
            element.appendChild(kf.to_dom(dom, param))
        return element

    def add_keyframe(self, *args, **kwargs):
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
    def animated(self):
        return self._animated

    @animated.setter
    def animated(self, v):
        if v != self._animated:
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
        self._value = v
        self._animated = False
        self._keyframes = None

    @property
    def keyframes(self):
        return self._keyframes


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
        dyl = param.appendChild(dom.createElement("dynamic_list"))
        dyl.setAttribute("type", self.type.typename)
        values = getattr(obj, self.att_name)
        for val in values:
            entry = dyl.appendChild(dom.createElement("entry"))
            entry.appendChild(self._value_to_dom(val, dom))

    def _value_to_dom(self, val, dom):
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
        return SifAnimatable.from_dom(element, self.type, registry)

    def from_python(self, value):
        return value

    def default(self):
        return []


class XmlStaticListParam(XmlDynamicListParam):
    _tag = "static_list"

    def _value_to_dom(self, val, dom):
        return value_to_xml_element(val, dom, self.decriptor)

    def _value_from_dom(self, element, registry):
        return value_from_xml_element(element, self.decriptor, registry)


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
