from .base import TgsObject, todo_func, TgsProp
from .properties import Value, MultiDimensional

load_effect = todo_func

## \ingroup Lottie


## \ingroup Lottie
## \todo check
class FillEffect(TgsObject):
    _props = [
        TgsProp("effect_index", "ix", float, False),
        TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", float, False),
        TgsProp("effects", "ef", load_effect, True),
    ]

    def __init__(self):
        ## Effect Index. Used for expressions.
        self.effect_index = 0
        ## After Effect's Match Name. Used for expressions.
        self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = ""
        ## Effect type.
        self.type = 21
        ## Effect List of properties.
        self.effects = [] # PointEffect, DropDownEffect, ColorEffect, DropDownEffect, SliderEffect, SliderEffect, SliderEffect


##\ingroup Lottie
## \todo check
class StrokeEffect(TgsObject):
    _props = [
        TgsProp("effect_index", "ix", float, False),
        TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", float, False),
        TgsProp("effects", "ef", load_effect, True),
    ]

    def __init__(self):
        ## Effect Index. Used for expressions.
        self.effect_index = 0
        ## After Effect's Match Name. Used for expressions.
        self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = ""
        ## Effect type.
        self.type = 22
        ## Effect List of properties.
        self.effects = [] # ColorEffect, CheckboxEffect, CheckboxEffect, ColorEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, DropDownEffect, DropDownEffect


##\ingroup Lottie
## \todo check
class DropDownEffect(TgsObject):
    _props = [
        TgsProp("effect_index", "ix", float, False),
        TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", float, False),
        TgsProp("value", "v", Value, False),
    ]

    def __init__(self):
        ## Effect Index. Used for expressions.
        self.effect_index = 0
        ## After Effect's Match Name. Used for expressions.
        self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = ""
        ## Effect type.
        self.type = 7
        ## Effect value.
        self.value = Value()


##\ingroup Lottie
## \todo check
class TritoneEffect(TgsObject):
    _props = [
        TgsProp("effect_index", "ix", float, False),
        TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", float, False),
        TgsProp("effects", "ef", load_effect, True),
    ]

    def __init__(self):
        ## Effect Index. Used for expressions.
        self.effect_index = 0
        ## After Effect's Match Name. Used for expressions.
        self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = ""
        ## Effect type.
        self.type = 23
        ## Effect List of properties.
        self.effects = [] # ColorEffect, ColorEffect, ColorEffect, SliderEffect


##\ingroup Lottie
## \todo check
class GroupEffect(TgsObject):
    _props = [
        TgsProp("effect_index", "ix", float, False),
        TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", float, False),
        TgsProp("effects", "ef", load_effect, True),
        TgsProp("enabled", "en", float, False),
    ]

    def __init__(self):
        ## Effect Index. Used for expressions.
        self.effect_index = 0
        ## After Effect's Match Name. Used for expressions.
        self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = ""
        ## Effect type.
        self.type = 5
        ## Effect List of properties.
        self.effects = [] # IndexEffect
        ## Enabled AE property value
        self.enabled = 0


##\ingroup Lottie
## \todo check
class ColorEffect(TgsObject):
    _props = [
        TgsProp("effect_index", "ix", float, False),
        TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", float, False),
        TgsProp("value", "v", MultiDimensional, False),
    ]

    def __init__(self):
        ## Effect Index. Used for expressions.
        self.effect_index = 0
        ## After Effect's Match Name. Used for expressions.
        self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = ""
        ## Effect type.
        self.type = 2
        ## Effect value.
        self.value = MultiDimensional()


##\ingroup Lottie
## \todo check
class ProLevelsEffect(TgsObject):
    _props = [
        TgsProp("effect_index", "ix", float, False),
        TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", float, False),
        TgsProp("effects", "ef", load_effect, True),
    ]

    def __init__(self):
        ## Effect Index. Used for expressions.
        self.effect_index = 0
        ## After Effect's Match Name. Used for expressions.
        self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = ""
        ## Effect type.
        self.type = 23
        ## ffect List of properties.
        self.effects = [] # DropDownEffect, NoValueEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect


##\ingroup Lottie
## \todo check
class AngleEffect(TgsObject):
    _props = [
        TgsProp("effect_index", "ix", float, False),
        TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", float, False),
        TgsProp("value", "v", Value, False),
    ]

    def __init__(self):
        ## Effect Index. Used for expressions. NOT USED. EQUALS SLIDER.
        self.effect_index = 0
        ## After Effect's Match Name. Used for expressions.
        self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = ""
        ## Effect type.
        self.type = 1
        ## Effect value.
        self.value = Value()


##\ingroup Lottie
## \todo check
class SliderEffect(TgsObject):
    _props = [
        TgsProp("effect_index", "ix", float, False),
        TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", float, False),
        TgsProp("value", "v", Value, False),
    ]

    def __init__(self):
        ## Effect Index. Used for expressions.
        self.effect_index = 0
        ## After Effect's Match Name. Used for expressions.
        self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = ""
        ## Effect type.
        self.type = 0
        ## Effect value.
        self.value = Value()


##\ingroup Lottie
## \todo check
class CheckBoxEffect(TgsObject):
    _props = [
        TgsProp("effect_index", "ix", float, False),
        TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", float, False),
        TgsProp("value", "v", Value, False),
    ]

    def __init__(self):
        ## Effect Index. Used for expressions.
        self.effect_index = 0
        ## After Effect's Match Name. Used for expressions.
        self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = ""
        ## Effect type.
        self.type = 7
        ## Effect value.
        self.value = Value()


##\ingroup Lottie
## \todo check
class PointEffect(TgsObject):
    _props = [
        TgsProp("effect_index", "ix", float, False),
        TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", float, False),
        TgsProp("value", "v", todo_func, True),
    ]

    def __init__(self):
        ## Effect Index. Used for expressions.
        self.effect_index = 0
        ## After Effect's Match Name. Used for expressions.
        self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = ""
        ## Effect type.
        self.type = 2
        ## Effect value.
        self.value = []


##\ingroup Lottie
## \todo check
class TintEffect(TgsObject):
    _props = [
        TgsProp("effect_index", "ix", float, False),
        TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", float, False),
        TgsProp("effects", "ef", load_effect, True),
    ]

    def __init__(self):
        ## Effect Index. Used for expressions.
        self.effect_index = 0
        ## After Effect's Match Name. Used for expressions.
        self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = ""
        ## Effect type.
        self.type = 20
        ## Effect List of properties.
        self.effects = [] # ColorEffect, ColorEffect, SliderEffect


##\ingroup Lottie
## \todo check
class LayerEffect(TgsObject):
    _props = [
        TgsProp("effect_index", "ix", float, False),
        TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", float, False),
        TgsProp("value", "v", Value, False),
    ]

    def __init__(self):
        ## Effect Index. Used for expressions. NOT USED. EQUALS SLIDER.
        self.effect_index = 0
        ## After Effect's Match Name. Used for expressions.
        self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = ""
        ## Effect type.
        self.type = 0
        ## Effect value.
        self.value = Value()
