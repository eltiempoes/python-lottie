import operator


def vop(op, a, b):
    return list(map(op, a, b))


class NVector():
    def __init__(self, *components):
        self.components = list(components)

    def __str__(self):
        return str(self.components)

    def __repr__(self):
        return "<NVector %s>" % self

    def __len__(self):
        return len(self.components)

    def to_list(self):
        return list(self.components)

    def __add__(self, other):
        return NVector(*vop(operator.add, self.components, other.components))

    def __sub__(self, other):
        return NVector(*vop(operator.sub, self.components, other.components))

    def __mul__(self, scalar):
        return NVector(*(c * scalar for c in self.components))

    def __truediv__(self, scalar):
        return NVector(*(c / scalar for c in self.components))

    def __iadd__(self, other):
        self.components = vop(operator.add, self.components, other.components)
        return self

    def __isub__(self, other):
        self.components = vop(operator.sub, self.components, other.components)
        return self

    def __imul__(self, scalar):
        self.components = [c * scalar for c in self.components]
        return self

    def __itruediv__(self, scalar):
        self.components = [c / scalar for c in self.components]
        return self

    def __neg__(self):
        return NVector(*(-c for c in self.components))

    def __getitem__(self, key):
        return self.components[key]

    def __setitem__(self, key, value):
        self.components[key] = value
