#!/usr/bin/env python3
import sys
import os
import pkgutil
import inspect
import argparse
import importlib
from functools import reduce
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
import lottie.objects
from lottie.objects.base import LottieEnum, LottieObject, PseudoList, LottieBase, PseudoBool
from lottie.objects.properties import Value, MultiDimensional
from lottie import NVector


class LanguageBind:
    extension = None

    def __init__(self, outpath):
        self.outpath = outpath
        self.out = None

    def _on_global_start(self):
        pass

    def _on_global_close(self):
        pass

    def _on_module_start(self, name):
        pass

    def _on_module_dependencies(self, depdict):
        pass

    def _on_module_close(self, name):
        pass

    def _on_class_open(self, cls, name, docs, bases):
        pass

    def _on_class_attribute(self, prop):
        pass

    def _on_class_init(self, name, valuedict, props):
        pass

    def _on_class_to_lottie(self, name, props):
        pass

    def _on_class_close(self):
        pass

    def _on_enum_open(self, name, docs):
        pass

    def _on_enum_value(self, name, value):
        pass

    def _on_enum_close(self):
        pass

    # Values

    def _on_value_null(self):
        pass

    def _on_value_number(self, value):
        return str(value)

    def _on_value_string(self, value):
        return repr(value)

    def _on_value_bool(self, value):
        return str(value).lower()

    def _on_value_list(self, value):
        return "[%s]" % ", ".join(map(self.convert_value, value))

    def _on_value_object(self, value, ctorargs):
        raise NotImplementedError()

    def _on_value_enum(self, value):
        return str(value)

    def _on_value_nvector(self, value):
        return self._on_value_list(value.components)

    # Lottie

    # Public

    def module_start(self, name):
        self.out = open(os.path.join(self.outpath, self.filename(name)), "w")
        self._on_module_start(name)

    def module_close(self, name):
        self._on_module_close(name)
        self.out.close()
        self.out = None

    def global_start(self):
        self._on_global_start()

    def global_close(self):
        self._on_global_close()

    def filename(self, base):
        return "%s.%s" % (base, self.extension)

    def module_dependencies(self, classes):
        depdict = {}
        for cls in classes:
            mod = cls.__module__.split(".")[-1]
            name = cls.__name__
            if mod not in depdict:
                depdict[mod] = [name]
            else:
                depdict[mod].append(name)
        self._on_module_dependencies(depdict)

    def class_open(self, cls, name, docs, bases):
        self._on_class_open(cls, name, docs.rstrip(), bases)

    def class_attribute(self, prop):
        self._on_class_attribute(prop)

    def class_init(self, name, valuedict, props):
        vd = {
            prop.name: valuedict.get(prop.name, None)
            for prop in props
        }
        self._on_class_init(name, vd, props)

    def class_to_lottie(self, name, props):
        self._on_class_to_lottie(name, props)

    def class_close(self):
        self._on_class_close()

    def enum_open(self, name, docs):
        self._on_enum_open(name, docs)

    def enum_value(self, name, value):
        self._on_enum_value(name, self.convert_value(value))

    def enum_close(self):
        self._on_enum_close()

    def wl(self, text, indent=0):
        self.out.write("%s%s\n" % (" " * (indent*4), text))

    def convert_value(self, value):
        if value is None:
            return self._on_value_null()
        if isinstance(value, LottieEnum):
            return self._on_value_enum(value)
        if isinstance(value, bool):
            return self._on_value_bool(value)
        if isinstance(value, (float, int)):
            return self._on_value_number(value)
        if isinstance(value, str):
            return self._on_value_string(value)
        if isinstance(value, list):
            return self._on_value_list(value)
        if isinstance(value, (Value, MultiDimensional)):
            return self._on_value_object(value, [self.convert_value(value.value)])
        if isinstance(value, LottieObject):
            return self._on_value_object(value, [])
        if isinstance(value, NVector):
            return self._on_value_nvector(value)
        raise NotImplementedError("%s" % value)


class JsBind(LanguageBind):
    extension = "js"

    def _on_global_start(self):
        self.all = {}

    def _on_global_close(self):
        with open(os.path.join(self.outpath, self.filename("all")), "w") as allf:
            for k, v in self.all.items():
                allf.write("export { %s } from './%s.js';\n" % (", ".join(v), k))

    def _on_module_start(self, name):
        self.all[name] = []
        self.all_current = self.all[name]
        self.wl("import { value_to_lottie, value_from_lottie, LottieObject } from '../base.js';")

    def _on_module_dependencies(self, depdict):
        for module, values in depdict.items():
            if module == "base":
                continue
            self.wl("import { %s } from './%s.js';" % (", ".join(values), module))
        self.wl("")

    def _on_class_open(self, cls, name, docs, bases):
        self.current_class = cls
        self.all_current.append(name)
        self.wl("/*{docs}\n*/\nexport class {name} extends {base}\n{{"
            .format(name=name, docs=docs, base=bases[-1].__name__))

    def _on_class_attribute(self, prop):
        self.wl(prop.name + ";", 1)

    def _on_class_close(self):
        self.wl("}\n")

    def _on_class_init(self, name, valuedict, props):
        self.wl("")

        skip = set()

        if name in ["MultiDimensional", "Value"]:
            self.wl("constructor(value=null)", 1)
            skip.add("value");
        else:
            self.wl("constructor()", 1)

        self.wl("{", 1)
        self.wl("super();", 2)

        if issubclass(self.current_class, lottie.objects.Layer) or issubclass(self.current_class, lottie.objects.ShapeElement):
            if self.current_class.type:
                self.wl("this.type = %r;" % self.current_class.type, 2)
                skip.add("type")

        if name in ["MultiDimensional", "Value"]:
            self.wl("this.value = value;", 2)

        for propname, value in valuedict.items():
            if propname not in skip:
                self.wl("this.%s = %s;" % (propname, self.convert_value(value)), 2)


        self.wl("}", 1)

    def _on_value_null(self):
        return "null"

    def _on_class_to_lottie(self, name, props):
        self.wl("")
        self.wl("to_lottie()", 1)
        self.wl("{", 1)
        self.wl("var arr = {};", 2)
        #self.wl("var arr = super.to_lottie();", 2)
        for prop in props:
            self.wl("if ( this.%s !== null )" % prop.name, 2)
            self.out.write(" "*4*3)
            self.out.write('arr["%s"] = value_to_lottie(' % prop.lottie)
            if prop.list is PseudoList:
                self.out.write("[")
            if prop.type is PseudoBool:
                self.out.write("Number(")
            self.out.write("this.%s" % prop.name)
            if prop.type is PseudoBool:
                self.out.write(")")
            if prop.list is PseudoList:
                self.out.write("]")
            self.out.write(");\n")
        self.wl("return arr;", 2)
        self.wl("}", 1)

        self.wl("")
        self.wl("static from_lottie(arr)", 1)
        self.wl("{", 1)
        self.wl("var obj = new %s();" % name, 2)
        for prop in props:
            self.wl('if ( arr["%s"] !== undefined )' % prop.lottie, 2)
            self.out.write(" "*4*3)
            self.out.write("obj.%s = value_from_lottie(" % prop.name)
            if prop.type is PseudoBool:
                self.out.write("Boolean(")
            self.out.write('arr["%s"]' % prop.lottie)
            if prop.type is PseudoBool:
                self.out.write(")")
            if prop.list is PseudoList:
                self.out.write("[0]")
            self.out.write(");\n")

        self.wl("return obj;", 2)
        self.wl("}", 1)

    def _on_enum_open(self, name, docs):
        self.all_current.append(name)
        self.wl("/*{docs}\n*/\nexport const {name} = Object.freeze({{".format(name=name, docs=docs))

    def _on_enum_value(self, name, value):
        self.wl("%s: %s," % (name, value), 1)

    def _on_enum_close(self):
        self.wl("});")

    # Values

    def _on_value_object(self, value, ctorargs):
        return "new %s(%s)" % (
            value.__class__.__name__,
            ", ".join(ctorargs)
        )

    def _on_value_enum(self, value):
        return str(value)


class PhpBind(LanguageBind):
    extension = "php"

    def _on_module_start(self, name):
        self.wl("<?php\n")

    def _on_module_dependencies(self, depdict):
        for module in depdict.keys():
            self.wl("require_once(\"%s.php\");" % module)
        self.wl("")

    def _on_class_open(self, cls, name, docs, bases):
        self.wl("/*{docs}\n*/\nclass {name} extends {base}\n{{".format(name=name, docs=docs, base=bases[0].__name__))

    def _on_class_attribute(self, prop):
        self.wl("public ${prop.name};".format(prop=prop), 1)

    def _on_class_close(self):
        self.wl("}\n")

    def _on_class_init(self, name, valuedict, props):
        self.wl("")
        self.wl("function __construct()", 1)
        self.wl("{", 1)
        for name, value in valuedict.items():
            self.wl("$this->%s = %s;" % (name, self.convert_value(value)), 2)
        self.wl("}", 1)

    def _on_value_null(self):
        return "null"

    def _on_class_to_lottie(self, name, props):
        self.wl("")
        self.wl("function to_lottie()", 1)
        self.wl("{", 1)
        self.wl("$arr = [];", 2)
        for prop in props:
            self.wl("if ( $this->%s !== null )" % prop.name, 2)
            self.out.write(" "*4*3)
            self.out.write('$arr["%s"] = self::value_to_lottie(' % prop.lottie)
            if prop.list is PseudoList:
                self.out.write("[")
            if prop.type is PseudoBool:
                self.out.write("(int)")
            self.out.write("$this->%s" % prop.name)
            if prop.list is PseudoList:
                self.out.write("]")
            self.out.write(");\n")
        self.wl("return $arr;", 2)
        self.wl("}", 1)

        self.wl("")
        self.wl("static function from_lottie($arr)", 1)
        self.wl("{", 1)
        self.wl("$obj = new %s();" % name, 2)
        for prop in props:
            self.wl('if ( isset($arr["%s"]) )' % prop.lottie, 2)
            self.out.write(" "*4*3)
            self.out.write("$obj->%s = self::value_from_lottie(" % prop.name)
            if prop.type is PseudoBool:
                self.out.write("(bool)")
            self.out.write('$arr["%s"]' % prop.lottie)
            if prop.list is PseudoList:
                self.out.write("[0]")
            self.out.write(");\n")
        self.wl("return $obj;", 2)
        self.wl("}", 1)

    def _on_enum_open(self, name, docs):
        self._on_class_open(name, docs, [LottieEnum])

    def _on_enum_value(self, name, value):
        self.wl("const %s = %s;" % (name, value), 1)

    def _on_enum_close(self):
        return self._on_class_close()

    # Values

    def _on_value_object(self, value, ctorargs):
        return "new %s(%s)" % (
            value.__class__.__name__,
            ", ".join(ctorargs)
        )

    def _on_value_enum(self, value):
        return str(value).replace(".", "::")


class ClassWrapper:
    def __init__(self, cls):
        self.cls = cls
        self.deps = set()
        self.external_deps = set()
        self._load_deps()

    def bind(self, binder):
        raise NotImplementedError()

    def _load_deps(self):
        for base in self.cls.__bases__:
            self._apply_dep(base)

    def _apply_dep(self, dep):
        if not isinstance(dep, type) or not issubclass(dep, LottieBase):
            return
        if dep.__module__ != self.cls.__module__:
            self.external_deps.add(dep)
        else:
            self.deps.add(dep)

    def deps_satisfied(self, deps):
        return self.deps.issubset(deps)


class ObjectWrapper(ClassWrapper):
    def __init__(self, cls):
        self.objprops = cls().__dict__
        super().__init__(cls)

    def bind(self, binder):
        binder.class_open(self.cls, self.cls.__name__, self.cls.__doc__ or "", self.cls.__bases__)
        for p in self.cls._props:
            binder.class_attribute(p)
        binder.class_init(self.cls.__name__, self.objprops, self.cls._props)
        binder.class_to_lottie(self.cls.__name__, self.cls._props)
        binder.class_close()

    def _load_deps(self):
        super()._load_deps()

        for p in self.cls._props:
            self._apply_dep(p.type)

        for v in self.objprops.values():
            self._apply_dep(type(v))


class EnumWrapper(ClassWrapper):
    def bind(self, binder):
        binder.enum_open(self.cls.__name__, self.cls.__doc__ or "")
        for p in self.cls.__members__.values():
            binder.enum_value(p.name, p.value)
        binder.enum_close()


binds = {
    "php": PhpBind,
    "js": JsBind,
}

parser = argparse.ArgumentParser()
parser.add_argument(
    "--output",
    "-o",
    default="/tmp/out/",
)
parser.add_argument(
    "language",
    choices=list(binds.keys()),
)


ns = parser.parse_args()

os.makedirs(ns.output, exist_ok=True)


bind = binds[ns.language](ns.output)

bind.global_start()

for _, modname, _ in pkgutil.iter_modules(lottie.objects.__path__):
    if modname == "base":
        continue

    full_modname = "lottie.objects." + modname
    module = importlib.import_module(full_modname)

    bind.module_start(modname)
    classes = []

    for clsname, cls in inspect.getmembers(module):
        if inspect.isclass(cls) and issubclass(cls, LottieBase) and cls.__module__ == full_modname:
            if issubclass(cls, LottieEnum):
                classes.append(EnumWrapper(cls))
            else:
                classes.append(ObjectWrapper(cls))

    external_deps = reduce(lambda a, b: a | b, (x.external_deps for x in classes))
    bind.module_dependencies(external_deps)

    sorted_classes = []
    deps = set()
    nclasses = len(classes)
    while classes:
        nc = []
        for cls in classes:
            if cls.deps_satisfied(deps):
                sorted_classes.append(cls)
                deps.add(cls.cls)
            else:
                nc.append(cls)
        if len(nc) == nclasses:
            sorted_classes += nc
            sys.stderr.write(
                "Couldn't satisfy dependencies for: %s\n" % (
                    ", ".join(cls.cls.__name__ for cls in nc)
                )
            )
            break
        else:
            classes = nc

    for cls in sorted_classes:
        cls.bind(bind)

    bind.module_close(modname)

bind.global_close()
