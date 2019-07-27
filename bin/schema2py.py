import json
import os
import sys
import argparse


def ucfirst(x):
    return x[0].upper() + x[1:]


def schema2py(out, filename, data, limit):
    if limit and class_name(filename) not in limit:
        return
    if data["type"] == "number":
        return schema2enum(out, filename, data)
    if data["type"] == "object":
        return schema2class(out, filename, data)


def schema2enum(out, filename, data):
    if filename.endswith("/boolean.json"):
        return

    out.write("\n\n## \ingroup Lottie\nclass ")
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
        self.list = False
        self.type = "float"
        if "const" in data:
            self.value = repr(data["const"])
        else:
            self._get_value(data)
            if self.value_comment == "MultiDimensional, MultiDimensionalKeyframed":
                self.value_comment = None
            elif self.value_comment == "Value, ValueKeyframed":
                self.value_comment = None

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
                    self.type = bool.__name__
                    self.value = "False"
                else:
                    self._get_value_object(data)
            elif "enum" in data and data["enum"] == [0, 1]:
                self.type = bool.__name__
                self.value = "False"
            else:
                self.value = "0"
        elif data["type"] == "object":
            if "properties" in data and "oneOf" not in data:
                self.value = 'None'
            self._get_value_object(data)
        elif data["type"] == "array":
            self.list = True
            self.value = "[]"
            if "items" in data:
                intype = data["items"].get("type", "object")
                if intype == "object":
                    self.type = "todo_func"
                    if len(data["items"]["oneOf"]) == 1:
                        self.type = class_name(data["items"]["oneOf"][0]["$ref"])
                    self.value_comment = ", ". join(
                        class_name(oo["$ref"])
                        for oo in data["items"]["oneOf"]
                    )
                else:
                    self.value_comment = intype
        elif data["type"] == "string":
            self.type = "str"
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
                    self.type = clsname
                    self.value = "%s()" % clsname

                if len(data["oneOf"]) > 1:
                    self.value_comment = ", ".join(
                        class_name(oo["$ref"])
                        for oo in data["oneOf"]
                    )
                if self.value_comment == "MultiDimensional, MultiDimensionalKeyframed":
                    self.type = "MultiDimensional"
                elif self.value_comment == "Value, ValueKeyframed":
                    self.type = "Value"
                else:
                    self.type = "todo_func"

    def write_init(self, out, indent):
        out.write(indent)
        out.write("## %s\n" % self.raw["description"])
        out.write(indent)
        out.write("self.%s = %s" % (self.name, self.value))
        if self.value_comment:
            out.write(" # %s" % self.value_comment)
        out.write("\n")


def schema2class(out, filename, data, ei=""):
    if "properties" not in data:
        return

    out.write("\n\n## \ingroup Lottie\nclass ")
    out.write(class_name(filename))
    out.write("(TgsObject): # TODO check\n")
    properties = []
    for n, p in data["properties"].items():
        prop = ClassProp(n, p)
        prop.ensure_unique_name(properties)
        properties.append(prop)

    out.write(" "*4+ei)
    out.write("_props = [\n")
    for p in properties:
        out.write(" "*8+ei)
        out.write("TgsProp(\"%s\", \"%s\", %s, %s),\n" % (p.name, p.out, p.type, p.list))
    out.write(" "*4+ei)
    out.write("]\n\n")

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
    elif name == "Transform" and bits[-1] == "shapes":
        name += "Shape"
    elif name == "Shape" and bits[-1] == "properties":
        name += "Property"
    elif name == "ShapeKeyframed":
        name = "ShapePropertyKeyframed"
    return name


p = argparse.ArgumentParser(
    description="Generates Python classes from the lottie-web JSON schema"
)
p.add_argument("limit", nargs="*")
schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "json")
p.add_argument("--load", "-l", default=schema_path)


if __name__ == "__main__":
    ns = p.parse_args()

    outfile = sys.stdout
    limit = ns.limit

    for root, _, files in os.walk(ns.load):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, "r") as fp:
                data = json.load(fp)
            if not data:
                continue
            schema2py(outfile, filepath, data, limit)
