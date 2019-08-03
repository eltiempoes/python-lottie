from .base import TgsObject, TgsProp, PseudoBool
from .properties import Value, MultiDimensional
from ..nvector import NVector


#5: EffectsManager,
#11: MaskEffect,
class EffectValue(TgsObject):
    """!
    Value for an effect
    """
    ## %Effect value type.
    type = None
    _classses = {}

    _props = [
        TgsProp("effect_index", "ix", int, False),
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", int, False),
    ]

    def __init__(self):
        ## Effect Index. Used for expressions.
        self.effect_index = None
        ## After Effect's Name. Used for expressions.
        self.name = None

        """
        ## After Effect's Match Name. Used for expressions.
        self.match_name = ""
        """

    @classmethod
    def _load_get_class(cls, lottiedict):
        if not EffectValue._classses:
            EffectValue._classses = {
                sc.type: sc
                for sc in EffectValue.__subclasses__()
            }
        return EffectValue._classses[lottiedict["ty"]]


## \ingroup Lottie
class Effect(TgsObject):
    """!
    Layer effect
    """
    ## %Effect type.
    type = None
    _classses = {}

    _props = [
        TgsProp("effect_index", "ix", int, False),
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", int, False),
        TgsProp("effects", "ef", EffectValue, True),
    ]
    _effects = []

    def __init__(self, *args, **kwargs):
        ## Effect Index. Used for expressions.
        self.effect_index = None
        ## After Effect's Name. Used for expressions.
        self.name = None
        ## Effect parameters
        self.effects = self._load_values(*args, **kwargs)

        """
        ## After Effect's Match Name. Used for expressions.
        self.match_name = ""
        """

    @classmethod
    def _load_get_class(cls, lottiedict):
        if not Effect._classses:
            Effect._classses = {
                sc.type: sc
                for sc in Effect.__subclasses__()
            }
        type = lottiedict["ty"]

        if type in Effect._classses:
            return Effect._classses[type]
        else:
            return Effect

    def _load_values(self, *args, **kwargs):
        values = []
        for i, (name, type) in enumerate(self._effects):
            val = []
            if len(args) > i:
                val = [args[i]]
            if name in kwargs:
                val = [kwargs[name]]
            values.append(type(*val))
        return values

    def __getattr__(self, key):
        for i, (name, type) in enumerate(self._effects):
            if name == key:
                return self.effects[i].value
        return super().__getattr__(key)


## \ingroup Lottie
class EffectValueAngle(EffectValue):
    _props = [
        TgsProp("value", "v", Value, False),
    ]
    ## %Effect type.
    type = 1

    def __init__(self, angle=0):
        EffectValue.__init__(self)
        ## Effect value.
        self.value = Value(angle)


## \ingroup Lottie
## \ingroup LottieCheck
class EffectNoValue(EffectValue):
    _props = []


## \ingroup Lottie
class EffectValueSlider(EffectValue):
    _props = [
        TgsProp("value", "v", Value, False),
    ]
    ## %Effect type.
    type = 0

    def __init__(self, value=0):
        EffectValue.__init__(self)
        ## Effect value.
        self.value = Value(value)


## \ingroup Lottie
class EffectValueCheckbox(EffectValue):
    _props = [
        TgsProp("value", "v", Value, False),
    ]
    ## %Effect type.
    type = 4

    def __init__(self, value=0):
        EffectValue.__init__(self)
        ## Effect value.
        self.value = Value(value)


## \ingroup Lottie
class EffectValuePoint(EffectValue):
    _props = [
        TgsProp("value", "v", MultiDimensional, False),
    ]
    ## %Effect type.
    type = 3

    def __init__(self, value=NVector(0, 0)):
        EffectValue.__init__(self)
        ## Effect value.
        self.value = MultiDimensional(value)


## \ingroup Lottie
## \ingroup LottieCheck
class EffectValueDropDown(EffectValue):
    _props = [
        TgsProp("value", "v", Value, False),
    ]
    ## %Effect type.
    type = 7

    def __init__(self, value=0):
        EffectValue.__init__(self)
        ## Effect value.
        self.value = Value(value)


## \ingroup Lottie
## \ingroup LottieCheck
class EffectValueLayer(EffectValue):
    _props = [
        TgsProp("value", "v", Value, False),
    ]
    ## %Effect type.
    type = 10

    def __init__(self):
        EffectValue.__init__(self)
        ## Effect value.
        self.value = Value()


## \ingroup Lottie
class EffectValueColor(EffectValue):
    _props = [
        TgsProp("value", "v", MultiDimensional, False),
    ]
    ## %Effect type.
    type = 2

    def __init__(self, value=NVector(0, 0, 0)):
        EffectValue.__init__(self)
        ## Effect value.
        self.value = MultiDimensional(value)


## \ingroup Lottie
class FillEffect(Effect):
    """!
    Replaces the whole layer with the given color
    @note Opacity is in [0, 1]
    """
    _effects = [
        ("00", EffectValuePoint),
        ("01", EffectValueDropDown),
        ("color", EffectValueColor),
        ("03", EffectValueDropDown),
        ("04", EffectValueSlider),
        ("05", EffectValueSlider),
        ("opacity", EffectValueSlider),
    ]
    ## %Effect type.
    type = 21


## \ingroup Lottie
class StrokeEffect(Effect):
    _effects = [
        ("00", EffectValueColor),
        ("01", EffectValueCheckbox),
        ("02", EffectValueCheckbox),
        ("color", EffectValueColor),
        ("04", EffectValueSlider),
        ("05", EffectValueSlider),
        ("06", EffectValueSlider),
        ("07", EffectValueSlider),
        ("08", EffectValueSlider),
        ("09", EffectValueDropDown),
        ("type", EffectValueDropDown),
    ]
    ## %Effect type.
    type = 22


## \ingroup Lottie
class TritoneEffect(Effect):
    """!
    Maps layers colors based on bright/mid/dark colors
    """
    _effects = [
        ("bright", EffectValueColor),
        ("mid", EffectValueColor),
        ("dark", EffectValueColor),
    ]
    ## %Effect type.
    type = 23


"""
## \ingroup Lottie
## \ingroup LottieCheck
class GroupEffect(Effect):
    _props = [
        TgsProp("enabled", "en", PseudoBool, False),
    ]

    def __init__(self):
        Effect.__init__(self)
        ## Enabled AE property value
        self.enabled = True
"""


## \ingroup Lottie
## \ingroup LottieCheck
class ProLevelsEffect(Effect):
    _effects = [
        ("00", EffectValueDropDown),
        ("01", EffectNoValue),
        ("02", EffectNoValue),
        ("comp_inblack", EffectValueSlider),
        ("comp_inwhite", EffectValueSlider),
        ("comp_gamma", EffectValueSlider),
        ("comp_outblack", EffectValueSlider),
        ("comp_outwhite", EffectNoValue),
        ("08", EffectNoValue),
        ("09", EffectValueSlider),
        ("r_inblack", EffectValueSlider),
        ("r_inwhite", EffectValueSlider),
        ("r_gamma", EffectValueSlider),
        ("r_outblack", EffectValueSlider),
        ("r_outwhite", EffectNoValue),
        ("15", EffectValueSlider),
        ("16", EffectValueSlider),
        ("g_inblack", EffectValueSlider),
        ("g_inwhite", EffectValueSlider),
        ("g_gamma", EffectValueSlider),
        ("g_outblack", EffectValueSlider),
        ("g_outwhite", EffectNoValue),
        ("22", EffectValueSlider),
        ("b3", EffectValueSlider),
        ("b_inblack", EffectValueSlider),
        ("b_inwhite", EffectValueSlider),
        ("b_gamma", EffectValueSlider),
        ("b_outblack", EffectValueSlider),
        ("b_outwhite", EffectNoValue),
        ("29", EffectValueSlider),
        ("a_inblack", EffectValueSlider),
        ("a_inwhite", EffectValueSlider),
        ("a_gamma", EffectValueSlider),
        ("a_outblack", EffectValueSlider),
        ("a_outwhite", EffectNoValue),
    ]
    ## %Effect type.
    type = 24


## \ingroup Lottie
class TintEffect(Effect):
    """!
    Colorizes the layer
    @note Opacity is in [0, 100]
    """
    _effects = [
        ("color_black", EffectValueColor),
        ("color_white", EffectValueColor),
        ("opacity", EffectValueSlider),
    ]
    ## %Effect type.
    type = 20


## \ingroup Lottie
class DropShadowEffect(Effect):
    """!
    Adds a shadow to the layer
    @note Opacity is in [0, 255]
    """
    _effects = [
        ("color", EffectValueColor),
        ("opacity", EffectValueSlider),
        ("angle", EffectValueAngle),
        ("distance", EffectValueSlider),
        ("blur", EffectValueSlider),
    ]
    ## %Effect type.
    type = 25


## \ingroup Lottie
## \ingroup LottieCheck
class Matte3Effect(Effect):
    _effects = [
        ("index", EffectValueSlider),
    ]
    ## %Effect type.
    type = 28


## \ingroup Lottie
class GaussianBlurEffect(Effect):
    """!
    Gaussian blur
    """
    _effects = [
        ("sigma", EffectValueSlider),
        ("dimensions", EffectValueSlider),
        ("wrap", EffectValueCheckbox),
    ]
    ## %Effect type.
    type = 29


## \ingroup Lottie
## \todo check
class ChangeColorEffect(Effect):
    """!
    Gaussian blur
    """
    _effects = [
        ("view", EffectValueDropDown),
        ("hue", EffectValueSlider),
        ("lightness", EffectValueSlider),
        ("saturation", EffectValueSlider),
        ("color_to_change", EffectValueColor),
        ("tolerance", EffectValueSlider),
        ("softness", EffectValueSlider),
        ("match", EffectValueDropDown),
        ("invert_mask", EffectValueDropDown),
    ]
    ## %Effect type.
    type = 29
