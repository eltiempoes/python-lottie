import sys
import os
import pkgutil
import importlib
import inspect
import re
import collections
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
import tgs.objects
from tgs.objects.base import TgsEnum, TgsObject, PseudoList, Tgs


root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
doxpath = os.path.join(root, "docs", "dox")
dox_classdoc = os.path.join(root, "docs", "dox", "lottie_class.dox")
dox_summary = os.path.join(root, "docs", "dox", "lottie.dox")


type_modules = {}
modules = []
Module = collections.namedtuple("Module", "name fullname module classes")


def extract_type_classdoc(name):
    return "\\ref {1}::{0} \"{0}\"".format(name, type_modules[name])


def extract_type_summary(name):
    return "<a href='#lottie_{0}'>{0}</a>".format(name)


def extract_type(prop, linkmode):
    name = prop.type.__name__
    if name.startswith("load_"):
        name = re.sub("(^|_)([a-z])", lambda x: x.group(2).upper(), name[5:])
    elif name == "todo_func":
        name = "unknown objects"

    if name in type_modules:
        name = linkmode(name)

    if linkmode is extract_type_summary and name == "NVector":
        name = "list of float"

    if prop.list is True:
        name = "list of %s" % name
    elif prop.list is PseudoList:
        name = "{0} or list of {0}".format(name)
    return name


def class_summary(clsname):
    #out_summary.write(
        #"""\n\\section lottie_{0} {0}\nPython class: \\ref {1}::{0} "{0}"\n\n\\copybrief {1}::{0}\n\n"""
        #.format(clsname, type_modules[clsname])
    #)
    out_summary.write(
        """<h2><a name='lottie_{0}'></a><a href='#lottie_{0}'>{0}</a></h2>\n\\par\nPython class: \\ref {1}::{0} "{0}"\n\\par\n\\copybrief {1}::{0}\n\\par\n"""
        .format(clsname, type_modules[clsname])
    )


for _, modname, _ in pkgutil.iter_modules(tgs.objects.__path__):
    if modname == "base":
        continue

    full_modname = "tgs.objects." + modname
    module = importlib.import_module(full_modname)

    classes = []

    for clsname, cls in inspect.getmembers(module):
        if inspect.isclass(cls):
            if issubclass(cls, Tgs) and cls not in {TgsObject, TgsEnum} and cls.__module__ == full_modname:
                type_modules[clsname] = full_modname.replace(".", "::")
                classes.append(cls)

    modules.append(Module(name=modname, fullname=full_modname, module=module, classes=classes))


def proptable(out, cls, module, mode):
    out.write("Lottie name|Type|Description|Attribute\n")
    out.write("-----------|----|-----------|---------\n")
    for prop in cls._props:
        fqn = "%s::%s::%s" % (module.fullname.replace(".", "::"), cls.__name__, prop.name)
        out.write(
            "{lottie} | {type} | \\copybrief {fqn} | \\ref {fqn} \"{name}\" \n"
            .format(
                lottie=prop.lottie,
                type=extract_type(prop, mode),
                fqn=fqn,
                name=prop.name
            )
        )


with open(dox_classdoc, "w") as out_classdoc, open(dox_summary, "w") as out_summary:
    out_classdoc.write("/**\n")
    out_summary.write("""/**
        \\page lottie_json Lottie JSON Format
        \\ingroup Lottie
    """)
    for module in modules:
        #out_summary.write("""\n\\section lottie_{0} {0}\n""".format(module.name))

        for cls in module.classes:
            clsname = cls.__name__
            if issubclass(cls, TgsObject):
                props = getattr(cls, "_props", None)
                class_summary(clsname)
                sub = cls.__subclasses__()
                if sub:
                    out_summary.write("Subclasses:\n")
                    for sc in sub:
                        out_summary.write(" - <a href='#lottie_{name}'>{name}</a>\n".format(
                            name=sc.__name__
                        ))
                if props:
                    out_classdoc.write("\\class %s.%s\n\\par Lottie JSON\n" % (module.fullname, clsname))
                    proptable(out_classdoc, cls, module, extract_type_classdoc)
                    out_classdoc.write("\n\n")

                    proptable(out_summary, cls, module, extract_type_summary)
                out_summary.write("\n\n")
            elif issubclass(cls, TgsEnum):
                class_summary(clsname)
                out_summary.write("Lottie Value|Name|Description| Attribute\n")
                out_summary.write("-----------|----|-----------|---------\n")
                for name, val in cls.__members__.items():
                    fqn = "%s::%s::%s" % (module.fullname.replace(".", "::"), clsname, name)
                    out_summary.write("{value} | {name} | \\copybrief {fqn} | \\ref {fqn} \"{name}\"\n".format(
                        value=val.value,
                        name=name,
                        fqn=fqn,
                    ))
                out_summary.write("\n\n")

    out_classdoc.write("*/")
    out_summary.write("*/")
