import sys
import os
import pkgutil
import importlib
import inspect
import re
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
import tgs.objects
from tgs.objects.base import TgsEnum, TgsObject, PseudoList


root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
doxfile = os.path.join(root, "docs", "dox", "lottie.dox")


type_modules = {
    "Layer": "tgs.objects.layers",
    "ShapeElement": "tgs.objects.shapes",
}

def extract_type(prop):
    name = prop.type.__name__
    if name.startswith("load_"):
        name = re.sub("(^|_)([a-z])", lambda x: x.group(2).upper(), name[5:])
        if name in type_modules:
            name = "\\ref {1}.{0} \"{0}\"".format(name, type_modules[name])
    elif name == "todo_func":
        name = "unknown objects"

    if prop.list is True:
        name = "list of %s" % name
    elif prop.list is PseudoList:
        name = "%s or list of %s"
    return name


with open(doxfile, "w") as out:
    out.write("/**\n")

    for _, modname, _ in pkgutil.iter_modules(tgs.objects.__path__):
        if modname == "base":
            continue

        full_modname = "tgs.objects." + modname
        module = importlib.import_module(full_modname)

        for clsname, cls in inspect.getmembers(module):
            if inspect.isclass(cls):
                if issubclass(cls, TgsObject) and cls != TgsObject:
                    props = getattr(cls, "_props", None)
                    if not props:
                        continue
                    out.write("\\class %s.%s\n\\par Lottie JSON\n" % (module.__name__, cls.__name__))
                    out.write("Lottie name|Attribute|Type|Description\n")
                    out.write("-----------|---------|----|-----------\n")
                    for prop in cls._props:
                        out.write("{0} | {1}#{2} | {3} | \\copybrief {2}\n".format(prop.lottie, clsname, prop.name, extract_type(prop)))
                    out.write("\n")
                elif issubclass(cls, TgsEnum) and cls != TgsEnum:
                    pass

    out.write("*/")
