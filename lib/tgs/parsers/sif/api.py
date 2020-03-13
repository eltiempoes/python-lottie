import enum
from xml.dom import minidom
from distutils.util import strtobool

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


class XmlAttribute(XmlDescriptor):
    def __init__(self, name, type=str, default_value=None):
        super().__init__(name, default_value)
        self.type = type
        self.default_value = default_value

    def from_xml(self, obj, domnode: minidom.Element):
        xml_str = domnode.getAttribute(self.name)
        if xml_str:
            setattr(obj, self.att_name, value_from_xml(xml_str, self.type))

    def __repr__(self):
        return "%s.Attribute(%r)" % (__name__, self.name)

    def from_python(self, value):
        if value is None and self.default_value is None:
            return None
        if not value_isinstance(value, self.type):
            return self.type(value)
        return value

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        value = getattr(obj, self.att_name)
        if value is not None:
            parent.setAttribute(self.name, value_to_xml(value, self.type))

    def default(self):
        return self.default_value


class XmlSimpleElement(XmlDescriptor):
    def __init__(self, name, type=str, default_value=None):
        super().__init__(name, default_value)
        self.type = type
        self.default_value = default_value

    def from_xml(self, obj, domnode: minidom.Element):
        for cn in domnode.childNodes:
            if cn.nodeType == minidom.Node.ELEMENT_NODE and cn.tagName == self.name:
                xml_str = "".join(x.nodeValue for x in cn.childNodes)
                value = value_from_xml(xml_str, self.type)
                break
        else:
            value = self.default_value

        setattr(obj, self.att_name, value)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        value = getattr(obj, self.att_name)
        if value is not None:
            parent.appendChild(dom.createElement(self.name)).appendChild(
                dom.createTextNode(value_to_xml(value, self.type))
            )

    def from_python(self, value):
        if value is None and self.default_value is None:
            return None
        if not value_isinstance(value, self.type):
            return self.type(value)
        return value

    def default(self):
        return self.default_value


class XmlMeta(XmlDescriptor):
    def __init__(self, values, name="meta"):
        super().__init__(name)
        self.values = values

    def default(self):
        return {}

    def from_xml(self, obj, domnode: minidom.Element):
        values = {}

        for cn in domnode.childNodes:
            if cn.nodeType == minidom.Node.ELEMENT_NODE and cn.tagName == self.name:
                name = cn.getAttribute("name")
                values[name] = value_from_xml(cn.getAttribute("content"), self.values[name])

        setattr(obj, self.att_name, values)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        for name, value in getattr(obj, self.att_name).items():
            element = parent.appendChild(dom.createElement(self.name))
            element.setAttribute("name", name)
            element.setAttribute("content", value_to_xml(value, self.values[name]))

    def clean(self, value):
        return value


class XmlList(XmlDescriptor):
    def __init__(self, child_node, name=None):
        super().__init__(child_node._tag)
        self.child_node = child_node
        self.att_name = self.att_name + "s" if name is None else name

    def default(self):
        return []

    def clean(self, value):
        return value

    def from_xml(self, obj, domnode: minidom.Element):
        values = []
        for cn in domnode.childNodes:
            if cn.nodeType == minidom.Node.ELEMENT_NODE and cn.tagName == self.name:
                values.append(self.child_node.from_dom(cn))

        setattr(obj, self.att_name, values)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        for value in getattr(obj, self.att_name):
            parent.appendChild(value.to_dom(dom))


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

    @classmethod
    def from_dom(cls, xml: minidom.Element):
        instance = cls()
        for node in cls._nodes:
            node.from_xml(instance, xml)
        return instance

    def to_dom(self, dom: minidom.Document):
        element = dom.createElement(self._tag)
        for node in self._nodes:
            node.to_xml(self, element, dom)
        return element


class Layer(SifNode):
    _nodes = [
        XmlAttribute("type", str, "group"),
        XmlAttribute("active", bool_str, True),
        XmlAttribute("version", str, "0.3"),
        XmlAttribute("exclude_from_rendering", bool_str, False),
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
        XmlMeta({
            "background_first_color": NVector,
            "background_rendering": bool,
            "background_second_color": NVector,
            "background_size": NVector,
            "grid_color": NVector,
            "grid_show": bool,
            "grid_size": NVector,
            "grid_snap": bool,
            "guide_color": NVector,
            "guide_show": bool,
            "guide_snap": bool,
            "jack_offset": float,
            "onion_skin": bool,
            "onion_skin_future": int,
            "onion_skin_past": int,
        }),
        XmlList(Layer)
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

