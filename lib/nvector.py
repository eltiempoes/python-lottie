class NVectorMeta(type):
    def __new__(cls, name, bases, attrs):
        for vop in attrs["vops"]:
            attrs[vop] = cls.v_op_factory(vop)
        for sop in attrs["sops"]:
            attrs[sop] = cls.s_op_factory(sop)
        return type.__new__(cls, name, bases, attrs)

    @classmethod
    def v_op(cls, op, a, b):
        return type(a)(
            *map(
                lambda x: getattr(x[0], op)(x[1]),
                zip(a.components, b.components)
            )
        )

    @classmethod
    def v_op_factory(cls, op):
        return lambda a, b: cls.v_op(op, a, b)

    @classmethod
    def s_op(cls, op, a, b):
        b = float(b)
        return type(a)(
            *map(
                lambda x: getattr(float(x), op)(b),
                a.components
            )
        )

    @classmethod
    def s_op_factory(cls, op):
        return lambda a, b: cls.s_op(op, a, b)


class NVector(metaclass=NVectorMeta):
    vops = ["__add__", "__sub__"]
    sops = ["__mul__", "__truediv__"]

    def __init__(self, *components):
        self.components = components

    def __str__(self):
        return str(self.components)

    def __len__(self):
        return len(self.components)

    def to_list(self):
        return list(self.components)
