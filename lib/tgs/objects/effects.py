from .base import TgsObject, TgsProp, PseudoBool
from .properties import Value, MultiDimensional


def load_effect(lottiedict):
    layers = {
        0: SliderEffect,
        1: AngleEffect,
        2: ColorEffect,
        3: PointEffect,
        4: CheckboxEffect,
        #5: EffectsManager,
        7: DropDownEffect,
        10: LayerEffect,
        #11: MaskEffect,
        20: TintEffect,
        21: FillEffect,
        22: StrokeEffect,
        23: TritoneEffect,
        24: ProLevelsEffect,
        25: DropShadowEffect,
        28: Matte3Effect,
        29: GaussianBlurEffect,
    }
    #NoValueEffect ?
    return layers[lottiedict["ty"]].load(lottiedict)


## \ingroup Lottie
class Effect(TgsObject):
    ## %Effect type.
    type = None

    _props = [
        TgsProp("effect_index", "ix", int, False),
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", int, False),
    ]

    def __init__(self, ty):
        ## Effect Index. Used for expressions.
        self.effect_index = None
        ## After Effect's Name. Used for expressions.
        self.name = None

        """
        ## After Effect's Match Name. Used for expressions.
        self.match_name = ""
        """


## \ingroup Lottie
## \todo check
class FillEffect(Effect):
    _props = [
        TgsProp("effects", "ef", load_effect, True),
    ]
    ## %Effect type.
    type = 21

    def __init__(self):
        Effect.__init__(self)
        ## Effect List of properties.
        self.effects = [] # PointEffect, DropDownEffect, ColorEffect, DropDownEffect, SliderEffect, SliderEffect, SliderEffect


##\ingroup Lottie
## \todo check
class StrokeEffect(Effect):
    _props = [
        TgsProp("effects", "ef", load_effect, True),
    ]
    ## %Effect type.
    type = 22

    def __init__(self):
        Effect.__init__(self)
        ## Effect List of properties.
        self.effects = [] # ColorEffect, CheckboxEffect, CheckboxEffect, ColorEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, DropDownEffect, DropDownEffect


##\ingroup Lottie
## \todo check
class DropDownEffect(Effect):
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
        TgsProp("effects", "ef", load_effect, True),
    ]
    ## %Effect type.
    type = 23

    def __init__(self):
        Effect.__init__(self)
        ## Effect List of properties.
        self.effects = [] # ColorEffect, ColorEffect, ColorEffect, SliderEffect


##\ingroup Lottie
## \todo check
class GroupEffect(Effect):
    _props = [
        TgsProp("effects", "ef", load_effect, True),
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
class ColorEffect(Effect):
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
        TgsProp("effects", "ef", load_effect, True),
    ]
    ## %Effect type.
    type = 24

    def __init__(self):
        Effect.__init__(self)
        ## ffect List of properties.
        self.effects = [] # DropDownEffect, NoValueEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect


##\ingroup Lottie
## \todo check
class AngleEffect(Effect):
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
class SliderEffect(Effect):
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
class CheckboxEffect(Effect):
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
class PointEffect(Effect):
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
        TgsProp("effects", "ef", load_effect, True),
    ]
    ## %Effect type.
    type = 20

    def __init__(self):
        Effect.__init__(self)
        ## Effect List of properties.
        self.effects = [] # ColorEffect, ColorEffect, SliderEffect


##\ingroup Lottie
## \todo check
class LayerEffect(Effect):
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
        TgsProp("effects", "ef", load_effect, True),
    ]
    ## %Effect type.
    type = 29

    def __init__(self, sigma=0, dimensions=0, wrap=0):
        Effect.__init__(self)
        self.effects = [SliderEffect(sigma), SliderEffect(dimensions), CheckboxEffect(wrap)]

    @property
    def sigma(self):
        return self.effects[0].value

    @property
    def dimensions(self):
        return self.effects[1].value

    @property
    def wrap(self):
        return bool(self.effects[2].value)
