import sys
import os
import pkgutil
import importlib
import inspect
import re
import collections
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
import lottie.objects
from lottie.objects.base import LottieEnum, LottieObject, PseudoList, LottieBase


root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
doxpath = os.path.join(root, "docs", "dox")
dox_classdoc = os.path.join(doxpath, "lottie_class.dox")
dox_summary = os.path.join(doxpath, "lottie.dox")


type_modules = {}
modules = []
Module = collections.namedtuple("Module", "name fullname module classes")


def extract_type_classdoc(name):
    return "\\ref {1}::{0} \"{0}\"".format(name, type_modules[name])


def extract_type_summary(name):
    return "<a href='#lottie_{0}'>{0}</a>".format(name)


def extract_type(prop, linkmode):
    name = prop.type.__name__

    if name in type_modules:
        name = linkmode(name)

    if linkmode is extract_type_summary and name == "NVector":
        name = "list of float"

    if prop.list is True:
        name = "list of %s" % name
    elif prop.list is PseudoList:
        name = "{0} or list of {0}".format(name)
    return name


def class_summary(cls):
    #out_summary.write(
        #"""\n\\section lottie_{0} {0}\nPython class: \\ref {1}::{0} "{0}"\n\n\\copybrief {1}::{0}\n\n"""
        #.format(clsname, type_modules[clsname])
    #)
    clsname = cls.__name__
    out_summary.write(
        r"""
<h2><a name='lottie_{0}'></a><a href='#lottie_{0}'>{0}</a></h2>
\par
Python class: \ref {1}::{0} "{0}"
\par
{2}
\par
        """
        .format(clsname, type_modules[clsname], (inspect.getdoc(cls) or "").lstrip("!").lstrip().replace("@brief", ""))
    )


for _, modname, _ in pkgutil.iter_modules(lottie.objects.__path__):
    if modname == "base":
        continue

    full_modname = "lottie.objects." + modname
    module = importlib.import_module(full_modname)

    classes = []

    for clsname, cls in inspect.getmembers(module):
        if inspect.isclass(cls):
            if issubclass(cls, LottieBase) and cls not in {LottieObject, LottieEnum} and cls.__module__ == full_modname:
                type_modules[clsname] = full_modname.replace(".", "::")
                classes.append(cls)

    modules.append(Module(name=modname, fullname=full_modname, module=module, classes=classes))


def proptable(out, cls, module, mode):
    out.write("Lottie name|Type|Description|Attribute\n")
    out.write("-----------|----|-----------|---------\n")
    for prop in cls._props:
        fqn = "%s::%s::%s" % (module.fullname.replace(".", "::"), cls.__name__, prop.name)
        type = extract_type(prop, mode)
        if hasattr(cls, prop.name):
            t = getattr(cls, prop.name)
            if isinstance(t, prop.type):
                type += " = %r" % t
        extra = ""
        if prop.lottie == "ef" and hasattr(cls, "_effects"):
            extra = "[%s]" % ", ".join(
                "<a href='#lottie_{0}'>{1}</a>".format(efcls.__name__, name)
                if mode is extract_type_summary
                else name
                for name, efcls in cls._effects
            )

        out.write(
            "{lottie} | {type} | \\copybrief {fqn} {extra} &nbsp; | \\ref {fqn} \"{name}\" \n"
            .format(
                lottie=prop.lottie,
                type=type,
                fqn=fqn,
                name=prop.name,
                extra=extra,
            )
        )


os.makedirs(doxpath, exist_ok=True)

with open(dox_classdoc, "w") as out_classdoc, open(dox_summary, "w") as out_summary:
    out_classdoc.write("/**\n")
    out_summary.write("""/**
\\page lottie_json Lottie JSON Format
\\ingroup Lottie
    """)

    out_summary.write("""\n\\section lottie_index Index\n""")
    for module in modules:
        out_summary.write(" - %s\n" % module.name)
        for cls in module.classes:
            out_summary.write("   - <a href='#lottie_{name}'>{name}</a>\n".format(name=cls.__name__))
        out_summary.write("\n")

    for module in modules:
        for cls in module.classes:
            clsname = cls.__name__
            if issubclass(cls, LottieObject):
                props = getattr(cls, "_props", None)
                class_summary(cls)
                sub = cls.__subclasses__()
                if sub:
                    out_summary.write("Subclasses:\n")
                    for sc in sub:
                        out_summary.write(" - <a href='#lottie_{name}'>{name}</a>\n".format(
                            name=sc.__name__
                        ))
                    out_summary.write("\n\par\n")
                if props:
                    out_classdoc.write("\\class %s.%s\n\\par Lottie JSON\n" % (module.fullname, clsname))
                    proptable(out_classdoc, cls, module, extract_type_classdoc)
                    out_classdoc.write("\n\n")

                    proptable(out_summary, cls, module, extract_type_summary)
                out_summary.write("\n\n")
            elif issubclass(cls, LottieEnum):
                class_summary(cls)
                out_summary.write("Lottie Value|Name|Description| Attribute\n")
                out_summary.write("------------|----|-----------|---------\n")
                for name, val in cls.__members__.items():
                    fqn = "%s::%s::%s" % (module.fullname.replace(".", "::"), clsname, name)
                    out_summary.write("{value} | {name} | \\copybrief {fqn} &nbsp; | \\ref {fqn} \"{name}\"\n".format(
                        value=val.value,
                        name=name,
                        fqn=fqn,
                    ))
                out_summary.write("\n\n")

    out_classdoc.write("*/")
    out_summary.write("*/")
