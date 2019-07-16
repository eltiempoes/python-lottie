from ..objects.base import TgsObject
from ..objects.properties import Bezier
from .nvector import NVector


def strip(tgs_object):
    if isinstance(tgs_object, Bezier):
        tgs_object.vertices = [NVector(x.x, x.y) for x in tgs_object.vertices]
        tgs_object.in_point = [NVector(x.x, x.y) for x in tgs_object.in_point]
        tgs_object.out_point = [NVector(x.x, x.y) for x in tgs_object.out_point]

    for p in tgs_object._props:
        pval = p.get(tgs_object)
        if isinstance(pval, TgsObject):
            strip(pval)
        elif isinstance(pval, list) and pval and isinstance(pval[0], TgsObject):
            for c in pval:
                strip(c)
        elif p.lottie in {"ind", "ix", "nm", "mn"}:
            p.set(tgs_object, None)
