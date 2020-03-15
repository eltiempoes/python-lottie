from .utils import *
from .core_nodes import XmlDescriptor


class XmlParamSif(XmlDescriptor):
    def __init__(self, name, child_node):
        super().__init__(name)
        self.child_node = child_node

    def from_xml(self, obj, parent: minidom.Element):
        for cn in xml_child_elements(parent, "param"):
            if cn.getAttribute("name") == self.name:
                value = self.child_node.from_dom(xml_first_element_child(cn))
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
        if not isinstance(value, self.child_node):
            raise ValueError("%s isn't a valid value for %s" % (value, self.name))
        return value

    def default(self):
        return self.child_node()


class SifNodeList:
    def __init__(self, type):
        self._items = []
        self._type = type

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, name):
        return self._items[name]

    def __getslice__(self, i, j):
        return self._items[i:j]

    def __setitem__(self, key, value: "Layer"):
        self.validate(value)
        self._items[key] = value

    def append(self, value: "Layer"):
        self.validate(value)
        self._items.append(value)

    def __str__(self):
        return str(self._items)

    def __repr__(self):
        return "<SifNodeList %s>" % self._items

    def validate(self, value):
        if not isinstance(value, self._type):
            raise ValueError("Not a valid object: %s" % value)


class XmlSifElement(XmlDescriptor):
    def __init__(self, name, child_node):
        super().__init__(name)
        self.child_node = child_node

    def default(self):
        return self.child_node()

    def clean(self, value):
        if not isinstance(value, self.child_node):
            raise ValueError("Invalid value for %s: %s" % (self.name, value))
        return value

    def from_xml(self, obj, parent: minidom.Element):
        cn = xml_first_element_child(parent, self.name, allow_none=True)
        if cn:
            value = self.child_node.from_dom(xml_first_element_child(cn))
        else:
            value = self.default()

        setattr(obj, self.att_name, value)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        value = getattr(obj, self.att_name)
        node = dom.createElement(self.name)
        node.appendChild(value.to_dom(dom))
        parent.appendChild(node)


class XmlList(XmlDescriptor):
    def __init__(self, child_node, name=None, wrapper_tag=None):
        super().__init__(wrapper_tag or child_node._tag)
        self.child_node = child_node
        self.att_name = self.att_name + "s" if name is None else name
        self.wrapper_tag = wrapper_tag

    def default(self):
        return SifNodeList(self.child_node)

    def clean(self, value):
        return value

    def from_xml(self, obj, parent: minidom.Element):
        values = self.default()
        for cn in xml_child_elements(parent, self.name):
            value_node = cn
            if self.wrapper_tag:
                value_node = xml_first_element_child(cn)
            values.append(self.child_node.from_dom(value_node))

        setattr(obj, self.att_name, values)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        for value in getattr(obj, self.att_name):
            value_node = value.to_dom(dom)
            if self.wrapper_tag:
                wrapper = dom.createElement(self.wrapper_tag)
                wrapper.appendChild(value_node)
                value_node = wrapper
            parent.appendChild(value_node)


class XmlWrapper(XmlDescriptor):
    def __init__(self, name, wrapped: XmlDescriptor):
        super().__init__(name)
        self.wrapped = wrapped

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        wrapper = parent.appendChild(dom.createElement(self.name))
        self.wrapped.to_xml(obj, wrapper, dom)

    def from_xml(self, obj, parent: minidom.Element):
        wrapper = xml_first_element_child(parent, self.name, True)
        if wrapper:
            return self.wrapped.from_xml(obj, wrapper)
        return self.default()

    def from_python(self, value):
        return self.wrapped.from_python(value)

    def initialize_object(self, dict, obj):
        return self.wrapped.initialize_object(dict, obj)

    def clean(self, value):
        return self.wrapped.clean(value)

    def default(self):
        return self.wrapped.default()


class XmlWrapperParam(XmlWrapper):
    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        wrapper = parent.appendChild(dom.createElement("param"))
        wrapper.setAttribute("name", self.name)
        self.wrapped.to_xml(obj, wrapper, dom)

    def from_xml(self, obj, parent: minidom.Element):
        for wrapper in xml_child_elements(parent, "param"):
            if wrapper.getAttribute("name") == self.name:
                return self.wrapped.from_xml(obj, wrapper)
        return self.default()
