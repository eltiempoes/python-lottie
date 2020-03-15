from xml.dom import minidom
import copy
import enum

from .core_nodes import XmlDescriptor
from .utils import *
from tgs import NVector


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
        cn = xml_first_element_child(parent, self.name)
        if cn:
            value = SifAnimatable.from_dom(xml_first_element_child(cn), self)
        else:
            value = self.default()

        setattr(obj, self.att_name, value)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        param = parent.appendChild(dom.createElement(self.name))
        param.appendChild(getattr(obj, self.att_name).to_dom(dom))
        return param

    def from_python(self, value):
        if not isinstance(value, SifAnimatable) or value._param is not self:
            raise ValueError("%s isn't a valid value for %s" % (value, self.name))
        return value


class XmlParam(XmlAnimatable):
    def from_xml(self, obj, parent: minidom.Element):
        for cn in xml_child_elements(parent, "param"):
            if cn.getAttribute("name") == self.name:
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
        for waypoint in xml_child_elements(xml, "waypoint"):
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
    def value_to_dom(cls, value, dom: minidom.Document, param: AnimatableTypeDescriptor):
        element = dom.createElement(param.typename)

        if param.typename == "vector":
            element.appendChild(xml_make_text(dom, "x", str(value.x)))
            element.appendChild(xml_make_text(dom, "y", str(value.y)))
            #element.setAttribute("guid", cls.guid())
        elif param.typename == "color":
            element.appendChild(xml_make_text(dom, "r", str(value[0])))
            element.appendChild(xml_make_text(dom, "g", str(value[1])))
            element.appendChild(xml_make_text(dom, "b", str(value[2])))
            element.appendChild(xml_make_text(dom, "a", str(value[3])))
            #element.setAttribute("guid", cls.guid())
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
            value = str_to_bool(xml.getAttribute("value"))
        else:
            raise ValueError("Unsupported type %s" % param.typename)

        return param.type_wrapper(value)

    def add_keyframe(self, *args, **kwargs):
        if self._param.static:
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


class XmlDynamicListParam(XmlDescriptor):
    def __init__(self, name, typename, att_name=None):
        super().__init__(name)
        self.decriptor = AnimatableTypeDescriptor(typename)
        if att_name is not None:
            self.att_name = att_name

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        param = parent.appendChild(dom.createElement("param"))
        param.setAttribute("name", self.name)
        dyl = param.appendChild(dom.createElement("dynamic_list"))
        dyl.setAttribute("type", self.decriptor.typename)
        values = getattr(obj, self.att_name)
        for val in values:
            entry = dyl.appendChild(dom.createElement("entry"))
            entry.appendChild(val.to_dom(dom))

    def from_xml(self, obj, parent: minidom.Element):
        values = []

        for cn in xml_child_elements(parent, "param"):
            if cn.getAttribute("name") == self.name:
                list = xml_first_element_child(cn)
                if list.getAttribute("type") != self.decriptor.typename:
                    raise ValueError(
                        "Wrong type for %s: got %s instead of %s" %
                        (self.name, self.decriptor.typename, list.getAttribute("type"))
                    )
                for entry in xml_child_elements(list, "entry"):
                    values.append(SifAnimatable.from_dom(xml_first_element_child(entry), self.decriptor))
                break

        setattr(obj, self.att_name, values)

    def from_python(self, value):
        return value

    def default(self):
        return []
