import enum
import inspect
from ..utils.nvector import NVector


class Tgs:
    """!
    Base class for TGS/Lottie JSON objects bindings
    """
    def to_dict(self):
        """!
        Serializes into a JSON object fit for the Lottie format
        """
        raise NotImplementedError

    @classmethod
    def load(cls, lottiedict):
        """!
        Loads from a JSON object
        \returns An instance of the class
        """
        raise NotImplementedError


class TgsEnum(Tgs, enum.Enum):
    """!
    Base class for enum-like types in the Lottie JSON structure
    """
    def to_dict(self):
        return self.value

    @classmethod
    def load(cls, lottieint):
        return cls(lottieint)


class PseudoList:
    """!
    List tag for some weird values in the Lottie JSON
    """
    pass


class TgsConverter:
    """!
    Factory for property types that require special conversions
    """
    def __init__(self, py, lottie, name=None):
        self.py = py
        self.lottie = lottie
        self.name = name or "%s but displayed as %s" % (self.py.__name__, self.lottie.__name__)

    def py_to_lottie(self, val):
        return self.lottie(val)

    def lottie_to_py(self, val):
        return self.py(val)

    @property
    def __name__(self):
        return self.name


## For values in Lottie that are bools but ints in the JSON
PseudoBool = TgsConverter(bool, int, "0-1 int")


class TgsProp:
    """!
    Lottie <-> Python property mapper
    """
    def __init__(self, name, lottie, type=float, list=False, cond=None):
        ## Name of the Python property
        self.name = name
        ## Name of the Lottie JSON property
        self.lottie = lottie
        ## Type of the property
        ## \see TgsConverter, PseudoBool
        self.type = type
        ## Whether the property is a list of self.type
        ## \see PseudoList
        self.list = list
        ## Condition on when the property is loaded from the Lottie JSON
        self.cond = cond

    def get(self, obj):
        """!
        Returns the value of the property from a Python object
        """
        return getattr(obj, self.name)

    def set(self, obj, value):
        """!
        Sets the value of the property from a Python object
        """
        return setattr(obj, self.name, value)

    def load_from_parent(self, lottiedict):
        """!
        Returns the value for this property from a JSON dict representing the parent object
        \returns The loaded value or \c None if the property is not in \p lottiedict
        """
        if self.lottie in lottiedict:
            return self.load(lottiedict[self.lottie])
        return None

    def load_into(self, lottiedict, obj):
        """!
        Loads from a Lottie dict into an object
        """
        if self.cond and not self.cond(lottiedict):
            return
        self.set(obj, self.load_from_parent(lottiedict))

    def load(self, lottieval):
        """!
        Loads the property from a JSON value
        \returns the Python equivalent of the JSON value
        """
        if self.list is PseudoList and isinstance(lottieval, list):
            return self._load_scalar(lottieval[0])
        elif self.list is True:
            return [
                self._load_scalar(it)
                for it in lottieval
            ]
        return self._load_scalar(lottieval)

    def _load_scalar(self, lottieval):
        if inspect.isclass(self.type) and issubclass(self.type, Tgs):
            return self.type.load(lottieval)
        elif isinstance(self.type, type) and isinstance(lottieval, self.type):
            return lottieval
        elif isinstance(self.type, TgsConverter):
            return self.type.lottie_to_py(lottieval)
        elif self.type is NVector:
            return NVector(*lottieval)
        return self.type(lottieval)

    def to_dict(self, obj):
        """!
        Converts the value of the property as from \p obj into a JSON value
        \param obj TgsObject with this property
        """
        val = self._basic_to_dict(self.get(obj))
        if self.list is PseudoList:
            val = [val]
        elif isinstance(self.type, TgsConverter):
            val = self._basic_to_dict(self.type.py_to_lottie(val))
        return val

    def _basic_to_dict(self, v):
        if isinstance(v, Tgs):
            return v.to_dict()
        elif isinstance(v, NVector):
            return list(map(self._basic_to_dict, v.components))
        elif isinstance(v, list):
            return list(map(self._basic_to_dict, v))
        elif isinstance(v, (int, str, bool)):
            return v
        elif isinstance(v, float):
            if v % 1 == 0:
                return int(v)
            return round(v, 3)
        else:
            raise Exception("Unknown value %r" % v)

    def __repr__(self):
        return "<TgsProp %s:%s>" % (self.name, self.lottie)


class TgsObject(Tgs):
    """!
    \brief Base class for mapping Python classes into Lottie JSON objects
    """
    def to_dict(self):
        return {
            prop.lottie: prop.to_dict(self)
            for prop in self._props
            if prop.get(self) is not None
        }

    @classmethod
    def load(cls, lottiedict):
        obj = cls()
        for prop in cls._props:
            prop.load_into(lottiedict, obj)
        return obj

    def find(self, search, propname="name"):
        """!
        \param search   The value of the property to search
        \param propname The name of the property used to search
        \brief Recursively searches for child objects with a matching property
        """
        if getattr(self, propname, None) == search:
            return self
        for prop in self._props:
            v = prop.get(self)
            if isinstance(v, TgsObject):
                found = v.find(search, propname)
                if found:
                    return found
            elif isinstance(v, list) and v and isinstance(v[0], TgsObject):
                for obj in v:
                    found = obj.find(search, propname)
                    if found:
                        return found
        return None


class Index:
    """!
    \brief Simple iterator to generate increasing integers
    """
    def __init__(self):
        self._i = -1

    def __next__(self):
        self._i += 1
        return self._i


def todo_func(x):
    """!
    Placeholder for TgsObjects loaders that haven't been implemented
    """
    raise NotImplementedError()
