import json
import os
import sys


def ucfirst(x):
    return x[0].upper() + x[1:]


def schema2py(out, filename, data):
    if data["type"] == "number":
        return schema2enum(out, filename, data)
    if data["type"] == "object":
        return schema2class(out, filename, data)


def schema2enum(out, filename, data):
    if filename.endswith("/boolean.json"):
        return

    out.write("\n\nclass ")
    out.write(class_name(filename))
    out.write("(TgsEnum):\n")
    vals = {}
    for c in data["oneOf"]:
        out.write(" "*4)
        name = ucfirst(c["standsFor"]).replace(" ", "")
        value = c["const"]
        out.write("%s = %s\n" % (name, value))
        vals[value] = name

    if "default" in data:
        out.write("\n")
        out.write(" "*4)
        out.write("@classmethod\n")
        out.write(" "*4)
        out.write("def default(cls):\n")
        out.write(" "*8)
        out.write("return cls.%s\n" % vals[data["default"]])


class ClassProp:
    def __init__(self, out, data):
        self.out = out
        self.name = self._prop_name(data)
        self.value = None
        self.raw = data
        self.value_comment = None
        if "const" in data:
            self.value = repr(data["const"])
        else:
            self._get_value(data)

    def ensure_unique_name(self, properties):
        if self._check_unique_name(properties):
            return
        if "description" in self.raw:
            self.name = self._format_name(self.raw["description"].replace(".", ""))
            if self._check_unique_name(properties):
                return
        self.name = self.out
        if not self._check_unique_name(properties):
            raise Exception("Cannot find unique property name")

    def _check_unique_name(self, properties):
        for p in properties:
            if p.name == self.name:
                return False
        return True

    def _prop_name(self, data):
        if "extended_name" in data:
            title = data["extended_name"]
        elif "title" in data:
            title = data["title"]
        else:
            raise Exception("No name")
        if title[0] == "3":
            return "threedimensional"
        title = self._format_name(title)
        if title == "class":
            return "css_class"
        return title

    def _format_name(self, n):
        return n.lower().replace(" ", "_").replace("-", "_")

    def _get_value(self, data):
        if data["type"] == "number":
            if "oneOf" in data:
                if data["oneOf"][0]["$ref"] == "#/helpers/boolean":
                    self.value = "False"
                else:
                    self._get_value_object(data)
            elif "enum" in data and data["enum"] == [0, 1]:
                self.value = "False"
            else:
                self.value = "0"
        elif data["type"] == "object":
            if "properties" in data and "oneOf" not in data:
                self.value = 'None'
            self._get_value_object(data)
        elif data["type"] == "array":
            self.value = "[]"
            if "items" in data:
                intype = data["items"].get("type", "object")
                if intype == "object":
                    self.value_comment = ", ". join(
                        class_name(oo["$ref"])
                        for oo in data["items"]["oneOf"]
                    )
                else:
                    self.value_comment = intype
        elif data["type"] == "string":
            self.value = '""'
        else:
            self.value = 'None'

    def _get_value_object(self, data):
        if "oneOf" not in data:
            self.value = 'None'
        else:
            desc = data["oneOf"][0]
            if "value" in desc:
                self.value = desc["value"]
                self.value_comment = ", ". join("%(value)s: %(standsFor)s" % oo for oo in data["oneOf"])
            else:
                clsname = class_name(desc["$ref"])
                if data["type"] == "number":
                    self.value = "%s.default()" % clsname
                else:
                    self.value = "%s()" % clsname

    def write_init(self, out, indent):
        out.write(indent)
        out.write("# %s\n" % self.raw["description"])
        out.write(indent)
        out.write("self.%s = %s" % (self.name, self.value))
        if self.value_comment:
            out.write(" # %s" % self.value_comment)
        out.write("\n")


def schema2class(out, filename, data, ei=""):
    if "properties" not in data:
        return

    out.write("\n\nclass ")
    out.write(class_name(filename))
    out.write("(TgsObject):\n")
    properties = []
    for n, p in data["properties"].items():
        prop = ClassProp(n, p)
        prop.ensure_unique_name(properties)
        properties.append(prop)

    out.write(" "*4+ei)
    out.write("_props = {\n")
    for p in properties:
        out.write(" "*8+ei)
        out.write("\"%s\": \"%s\",\n" % (p.name, p.out))
    out.write(" "*4+ei)
    out.write("}\n\n")

    out.write(" "*4+ei)
    out.write("def __init__(self):\n")
    for p in properties:
        p.write_init(out, " "*8+ei)





def class_name(filename):
    bits = os.path.splitext(filename)[0].rsplit("/", 2)
    name = ucfirst(bits.pop())
    if bits[-1] == "layers":
        name += "Layer"
    elif bits[-1] == "effects":
        name += "Effect"
    return name


schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "json")
outfile = sys.stdout

for root, _, files in os.walk(schema_path):
    for file in files:
        filepath = os.path.join(root, file)
        with open(filepath, "r") as fp:
            data = json.load(fp)
        if not data:
            continue
        schema2py(outfile, filepath, data)

