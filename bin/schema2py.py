import json
import os
import sys


def ucfirst(x):
    return x[0].upper() + x[1:]


def schema2py(out, filename, data, name):
    if data["type"] == "number":
        return schema2enum(out, filename, data, name)
    if data["type"] == "object":
        return schema2class(out, filename, data, name)


def schema2enum(out, filename, data, name):
    if name == "Boolean":
        return

    out.write("\n\nclass ")
    out.write(name)
    out.write("(TgsEnum):\n")
    for c in data["oneOf"]:
        out.write(" "*4)
        out.write(ucfirst(c["standsFor"]).replace(" ", ""))
        out.write(" = ")
        out.write(str(c["const"]))
        out.write("\n")


def schema2class(out, filename, data, name, ei=""):
    if "properties" not in data:
        return

    if "/layer/" in filename:
        name += "Layer"

    out.write("\n\nclass ")
    out.write(name)
    out.write("(TgsObject):\n")
    properties = []
    for n, p in data["properties"].items():
        properties.append({
            "out": n,
            "name": _prop_name(p),
            "type": _get_type(p),
            "raw": p
        })

    out.write(" "*4+ei)
    out.write("_props = {\n")
    for p in properties:
        out.write(" "*8+ei)
        out.write("\"%s\": \"%s\",\n" % (p["name"], p["out"]))
    out.write(" "*4+ei)
    out.write("}\n\n")

    out.write(" "*4+ei)
    out.write("def __init__(self):\n")
    for p in properties:
        out.write(" "*8+ei)
        out.write("# %s\n" % p["raw"]["description"])
        out.write(" "*8)
        out.write("self.%s = " % p["name"])
        if p["type"] == list:
            out.write("[]")
        elif p["type"] == str:
            out.write("\"\"")
        elif p["type"] == float:
            out.write("0")
        elif p["type"] == bool:
            out.write("False")
        elif p["type"] == object:
            if "oneOf" not in p["raw"]:
                out.write("None")
            else:
                desc = p["raw"]["oneOf"][0]
                if "value" in desc:
                    out.write("%s # %s" % (
                        desc["value"],
                        ", ". join("%(value)s: %(standsFor)s" % oo for oo in p["raw"]["oneOf"])
                    ))
                else:
                    clsname = ucfirst(desc["$ref"].rsplit("/", 1)[-1])
                    out.write("%s()" % clsname)
        elif p["type"] == type:
            clsname = p["class"]
            out.write("new %s()" % clsname)
        else:
            out.write("None")
        out.write("\n")


def _get_type(data):
    if data["type"] == "number":
        if "oneOf" in data:
            if data["oneOf"][0]["$ref"] == "#/helpers/boolean":
                return bool
            return object
        if "enum" in data and data["enum"] == [0, 1]:
            return bool
        return float
    if data["type"] == "object":
        if "properties" in data and "oneOf" not in data:
            return None
        return object
    if data["type"] == "array":
        return list
    if data["type"] == "string":
        return str
    return None


def _prop_name(p):
    if "extended_name" in p:
        title = p["extended_name"]
    elif "title" in p:
        title = p["title"]
    else:
        raise Exception("No name")
    if title[0] == "3":
        return "threedimensional"
    title = title.lower().replace(" ", "_").replace("-", "_")
    if title == "class":
        return "css_class"
    return title


schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "json")
outfile = sys.stdout

for root, _, files in os.walk(schema_path):
    for file in files:
        filepath = os.path.join(root, file)
        with open(filepath, "r") as fp:
            data = json.load(fp)
        if not data:
            continue
        classname = ucfirst(os.path.splitext(file)[0])
        schema2py(outfile, filepath, data, classname)

