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
        ## Effect type.
        self.type = ty

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

    def __init__(self):
        Effect.__init__(self, 21)
        ## Effect List of properties.
        self.effects = [] # PointEffect, DropDownEffect, ColorEffect, DropDownEffect, SliderEffect, SliderEffect, SliderEffect


##\ingroup Lottie
## \todo check
class StrokeEffect(Effect):
    _props = [
        TgsProp("effects", "ef", load_effect, True),
    ]

    def __init__(self):
        Effect.__init__(self, 22)
        ## Effect List of properties.
        self.effects = [] # ColorEffect, CheckboxEffect, CheckboxEffect, ColorEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, DropDownEffect, DropDownEffect


##\ingroup Lottie
## \todo check
class DropDownEffect(Effect):
    _props = [
        TgsProp("value", "v", Value, False),
    ]

    def __init__(self):
        Effect.__init__(self, 7)
        ## Effect value.
        self.value = Value()


##\ingroup Lottie
## \todo check
class TritoneEffect(Effect):
    _props = [
        TgsProp("effects", "ef", load_effect, True),
    ]

    def __init__(self):
        Effect.__init__(self, 23)
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

    def __init__(self):
        Effect.__init__(self, 2)
        ## Effect value.
        self.value = MultiDimensional()


##\ingroup Lottie
## \todo check
class ProLevelsEffect(Effect):
    _props = [
        TgsProp("effects", "ef", load_effect, True),
    ]

    def __init__(self):
        Effect.__init__(self, 24)
        ## ffect List of properties.
        self.effects = [] # DropDownEffect, NoValueEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect


##\ingroup Lottie
## \todo check
class AngleEffect(Effect):
    _props = [
        TgsProp("value", "v", Value, False),
    ]

    def __init__(self):
        Effect.__init__(self, 1)
        ## Effect value.
        self.value = Value()


##\ingroup Lottie
## \todo check
class SliderEffect(Effect):
    _props = [
        TgsProp("value", "v", Value, False),
    ]

    def __init__(self, value=0):
        Effect.__init__(self, 0)
        ## Effect value.
        self.value = Value(value)


##\ingroup Lottie
## \todo check
class CheckboxEffect(Effect):
    _props = [
        TgsProp("value", "v", Value, False),
    ]

    def __init__(self, value=0):
        Effect.__init__(self, 4)
        ## Effect value.
        self.value = Value(value)


##\ingroup Lottie
## \todo check
class PointEffect(Effect):
    _props = [
        TgsProp("value", "v", MultiDimensional, False),
    ]

    def __init__(self):
        Effect.__init__(self, 3)
        ## Effect value.
        self.value = MultiDimensional()


##\ingroup Lottie
## \todo check
class TintEffect(Effect):
    _props = [
        TgsProp("effects", "ef", load_effect, True),
    ]

    def __init__(self):
        Effect.__init__(self, 20)
        ## Effect List of properties.
        self.effects = [] # ColorEffect, ColorEffect, SliderEffect


##\ingroup Lottie
## \todo check
class LayerEffect(Effect):
    _props = [
        TgsProp("value", "v", Value, False),
    ]

    def __init__(self):
        Effect.__init__(self, 10)
        ## Effect value.
        self.value = Value()


##\ingroup Lottie
## \todo check
class DropShadowEffect(Effect):
    _props = [
        # ?
    ]

    def __init__(self):
        Effect.__init__(self, 25)


##\ingroup Lottie
## \todo check
class Matte3Effect(Effect):
    _props = [
        # ?
    ]

    def __init__(self):
        Effect.__init__(self, 28)


## \ingroup Lottie
class GaussianBlurEffect(Effect):
    _props = [
        TgsProp("effects", "ef", load_effect, True),
    ]

    def __init__(self, sigma=0, dimensions=0, wrap=0):
        Effect.__init__(self, 29)
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
