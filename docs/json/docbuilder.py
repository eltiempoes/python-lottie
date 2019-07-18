import sys
import os
import pkgutil
import importlib
import inspect
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "lib"
))
import tgs.objects
from tgs.objects.base import TgsEnum, TgsObject, PseudoList


def title(word, char="-"):
    print(word)
    print(char*len(word))
    print("")


def lowtitle(word, level=3):
    print("#" * level + " " + word)
    print("")


def list_item(txt):
    print(" * " + txt)


def extract_type(prop):
    name = prop.type.__name__
    if name.startswith("load_"):
        name = name[5:]

    if prop.list is True:
        name = "list of %s" % name
    elif prop.list is PseudoList:
        name = "%s or list of %s"
    return name


for _, modname, _ in pkgutil.iter_modules(tgs.objects.__path__):
    if modname == "base":
        continue

    module = importlib.import_module("tgs.objects." + modname)
    title(modname, "=")

    for clsname, cls in inspect.getmembers(module):
        if inspect.isclass(cls):
            if issubclass(cls, TgsObject) and cls != TgsObject:
                title(clsname)
                for prop in cls._props:
                    lowtitle(prop.lottie)
                    list_item("Description: " + prop.name.replace("_", " "))
                    list_item("Type: " + extract_type(prop))
                    print("")
                print("\n")
            elif issubclass(cls, TgsEnum) and cls != TgsEnum:
                title(clsname)
                for name, val in cls.__members__.items():
                    list_item("%s = %s" % (val.value, name))
                print("\n")


