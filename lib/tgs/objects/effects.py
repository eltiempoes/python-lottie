from .base import TgsObject, TgsProp, PseudoBool
from .properties import Value, MultiDimensional


#NoValueEffect ?
#5: EffectsManager,
#11: MaskEffect,
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
        if not Effect._classses:
            Effect._classses = {
                sc.type: sc
                for sc in Effect.__subclasses__()
            }
        return Effect._classses[lottiedict["ty"]]


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
## \todo check
class FillEffect(Effect):
    _props = [
        TgsProp("effects", "ef", EffectValue, True),
    ]
    ## %Effect type.
    type = 21

    def __init__(self):
        Effect.__init__(self)
        ## Effect List of properties.
        self.effects = [] # EffectValuePoint, EffectValueDropDown, EffectValueColor, EffectValueDropDown, EffectValueSlider, EffectValueSlider, EffectValueSlider


##\ingroup Lottie
## \todo check
class StrokeEffect(Effect):
    _props = [
        TgsProp("effects", "ef", EffectValue, True),
    ]
    ## %Effect type.
    type = 22

    def __init__(self):
        Effect.__init__(self)
        ## Effect List of properties.
        self.effects = [] # EffectValueColor, EffectValueCheckbox, EffectValueCheckbox, EffectValueColor, EffectValueSlider, EffectValueSlider, EffectValueSlider, EffectValueSlider, EffectValueSlider, EffectValueDropDown, EffectValueDropDown


##\ingroup Lottie
## \todo check
class EffectValueDropDown(EffectValue):
    _props = [
        TgsProp("value", "v", Value, False),
    ]
    ## %Effect type.
    type = 7

    def __init__(self):
        Effect.__init__(self)
        ## Effect value.
        self.value = Value()


##\ingroup Lottie
## \todo check
class TritoneEffect(Effect):
    _props = [
        TgsProp("effects", "ef", EffectValue, True),
    ]
    ## %Effect type.
    type = 23

    def __init__(self):
        Effect.__init__(self)
        ## Effect List of properties.
        self.effects = [] # EffectValueColor, EffectValueColor, EffectValueColor, EffectValueSlider


##\ingroup Lottie
## \todo check
class GroupEffect(Effect):
    _props = [
        TgsProp("effects", "ef", EffectValue, True),
        TgsProp("enabled", "en", PseudoBool, False),
    ]

    def __init__(self, effects=[]):
        Effect.__init__(self, type)
        ## Effect List of properties.
        self.effects = effects
        ## Enabled AE property value
        self.enabled = True


##\ingroup Lottie
## \todo check
class EffectValueColor(EffectValue):
    _props = [
        TgsProp("value", "v", MultiDimensional, False),
    ]
    ## %Effect type.
    type = 2

    def __init__(self):
        Effect.__init__(self)
        ## Effect value.
        self.value = MultiDimensional()


##\ingroup Lottie
## \todo check
class ProLevelsEffect(Effect):
    _props = [
        TgsProp("effects", "ef", EffectValue, True),
    ]
    ## %Effect type.
    type = 24

    def __init__(self):
        Effect.__init__(self)
        ## ffect List of properties.
        self.effects = [] # EffectValueDropDown, NoValueEffect, NoValueEffect, EffectValueSlider, EffectValueSlider, EffectValueSlider, EffectValueSlider, EffectValueSlider, NoValueEffect, EffectValueSlider, EffectValueSlider, EffectValueSlider, EffectValueSlider, EffectValueSlider, NoValueEffect, EffectValueSlider, EffectValueSlider, EffectValueSlider, EffectValueSlider, EffectValueSlider, NoValueEffect, EffectValueSlider, EffectValueSlider, EffectValueSlider, EffectValueSlider, EffectValueSlider, NoValueEffect, EffectValueSlider, EffectValueSlider, EffectValueSlider, EffectValueSlider, EffectValueSlider


##\ingroup Lottie
## \todo check
class EffectValueAngle(EffectValue):
    _props = [
        TgsProp("value", "v", Value, False),
    ]
    ## %Effect type.
    type = 1

    def __init__(self):
        Effect.__init__(self)
        ## Effect value.
        self.value = Value()


##\ingroup Lottie
## \todo check
class EffectValueSlider(EffectValue):
    _props = [
        TgsProp("value", "v", Value, False),
    ]
    ## %Effect type.
    type = 0

    def __init__(self, value=0):
        Effect.__init__(self)
        ## Effect value.
        self.value = Value(value)


##\ingroup Lottie
## \todo check
class EffectValueCheckbox(EffectValue):
    _props = [
        TgsProp("value", "v", Value, False),
    ]
    ## %Effect type.
    type = 4

    def __init__(self, value=0):
        Effect.__init__(self)
        ## Effect value.
        self.value = Value(value)


##\ingroup Lottie
## \todo check
class EffectValuePoint(EffectValue):
    _props = [
        TgsProp("value", "v", MultiDimensional, False),
    ]
    ## %Effect type.
    type = 3

    def __init__(self):
        Effect.__init__(self)
        ## Effect value.
        self.value = MultiDimensional()


##\ingroup Lottie
## \todo check
class TintEffect(Effect):
    _props = [
        TgsProp("effects", "ef", EffectValue, True),
    ]
    ## %Effect type.
    type = 20

    def __init__(self):
        Effect.__init__(self)
        ## Effect List of properties.
        self.effects = [] # EffectValueColor, EffectValueColor, EffectValueSlider


##\ingroup Lottie
## \todo check
class EffectValueLayer(EffectValue):
    _props = [
        TgsProp("value", "v", Value, False),
    ]
    ## %Effect type.
    type = 10

    def __init__(self):
        Effect.__init__(self)
        ## Effect value.
        self.value = Value()


##\ingroup Lottie
## \todo check
class DropShadowEffect(Effect):
    _props = [
        # ?
    ]
    ## %Effect type.
    type = 25

    def __init__(self):
        Effect.__init__(self)


##\ingroup Lottie
## \todo check
class Matte3Effect(Effect):
    _props = [
        # ?
    ]
    ## %Effect type.
    type = 28

    def __init__(self):
        Effect.__init__(self)


## \ingroup Lottie
class GaussianBlurEffect(Effect):
    _props = [
        TgsProp("effects", "ef", EffectValue, True),
    ]
    ## %Effect type.
    type = 29

    def __init__(self, sigma=0, dimensions=0, wrap=0):
        Effect.__init__(self)
        self.effects = [EffectValueSlider(sigma), EffectValueSlider(dimensions), EffectValueCheckbox(wrap)]

    @property
    def sigma(self):
        return self.effects[0].value

    @property
    def dimensions(self):
        return self.effects[1].value

    @property
    def wrap(self):
        return bool(self.effects[2].value)
