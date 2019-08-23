from ..objects.base import TgsObject, ObjectVisitor
from ..objects.bezier import Bezier
from..nvector import NVector


class Strip(ObjectVisitor):
    def __init__(self, float_round, remove_attributes={}):
        self.float_round = float_round
        self.remove_attributes = remove_attributes

    def round(self, fl):
        return round(fl, self.float_round)

    def nvector(self, value):
        value.components = list(map(self.round, value.components))
        return value

    def visit_property(self, object, property, value):
        if isinstance(value, Bezier):
            for l in ["vertices", "in_tangents", "out_tangents"]:
                setattr(value, l, [self.nvector(NVector(p.x, p.y)) for p in getattr(value, l)])
        elif property.lottie in self.remove_attributes:
            property.set(object, None)
        elif isinstance(value, float):
            property.set(object, round(value, 3))
        elif isinstance(value, NVector):
            self.nvector(value)


heavy_strip = Strip(3, {"ind", "ix", "nm", "mn"})
float_strip = Strip(3)
