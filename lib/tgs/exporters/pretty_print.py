import sys

from ..objects.base import TgsObject, Tgs
from ..objects.properties import MultiDimensional, Value, ShapeProperty
from ..objects.layers import Layer


def _prettyprint_scalar(tgs_object, out=sys.stdout):
    if isinstance(tgs_object, float) and tgs_object == round(tgs_object):
        tgs_object = int(tgs_object)
    return str(tgs_object)


def prettyprint(tgs_object, out=sys.stdout, indent="   ", _i=""):
    if isinstance(tgs_object, TgsObject):
        out.write(tgs_object.__class__.__name__)
        out.write('\n')
        _i += indent
        maxk = max(map(lambda x: len(x.name), tgs_object._props))
        for k in tgs_object._props:
            out.write(_i)
            out.write(k.name.ljust(maxk))
            out.write(' : ')
            prettyprint(k.get(tgs_object), out, indent, _i)
    elif isinstance(tgs_object, (list, tuple)):
        if not tgs_object or (not isinstance(tgs_object[0], Tgs) and len(tgs_object) < 16):
            out.write("[")
            out.write(", ".join(map(_prettyprint_scalar, tgs_object)))
            out.write("]\n")
        else:
            out.write("[\n")
            for k in tgs_object:
                out.write(_i + indent)
                prettyprint(k, out, indent, _i + indent)
            out.write(_i)
            out.write(']\n')
    else:
        out.write(_prettyprint_scalar(tgs_object, out))
        out.write('\n')


def _prettyprint_summary_printable(obj):
    if isinstance(obj, TgsObject):
        return not isinstance(obj, (MultiDimensional, Value, ShapeProperty))
    return obj and isinstance(obj, (list, tuple)) and isinstance(obj[0], TgsObject)


def prettyprint_summary(tgs_object, out=sys.stdout, indent="   ", _i=""):
    if isinstance(tgs_object, TgsObject):
        out.write(tgs_object.__class__.__name__)
        name = getattr(tgs_object, "name", None)
        if name:
            out.write(" %r" % name)
        if isinstance(tgs_object, Layer):
            out.write(" %s -> %s" % (tgs_object.index, tgs_object.parent))
        out.write('\n')
        _i += indent
        for k in tgs_object._props:
            val = k.get(tgs_object)
            if _prettyprint_summary_printable(val):
                out.write(_i)
                out.write(k.name)
                out.write(' : ')
                prettyprint_summary(val, out, indent, _i)
    elif _prettyprint_summary_printable(tgs_object):
            out.write("[\n")
            for k in tgs_object:
                out.write(_i + indent)
                prettyprint_summary(k, out, indent, _i + indent)
            out.write(_i)
            out.write(']\n')
