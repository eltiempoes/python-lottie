from ..objects.base import TgsObject
from ..objects.bezier import Bezier
from..nvector import NVector


def strip(tgs_object):
    if isinstance(tgs_object, Bezier):
        tgs_object.shape = [NVector(x.x, x.y) for x in tgs_object.shape]
        tgs_object.in_tangents = [NVector(x.x, x.y) for x in tgs_object.in_tangents]
        tgs_object.out_tangents = [NVector(x.x, x.y) for x in tgs_object.out_tangents]

    for p in tgs_object._props:
        pval = p.get(tgs_object)
        if isinstance(pval, TgsObject):
            strip(pval)
        elif isinstance(pval, list) and pval and isinstance(pval[0], TgsObject):
            for c in pval:
                strip(c)
        elif p.lottie in {"ind", "ix", "nm", "mn"}:
            p.set(tgs_object, None)
