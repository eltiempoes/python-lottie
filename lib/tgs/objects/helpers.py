from .base import TgsObject, TgsProp, TgsEnum
from .properties import MultiDimensional, Value, NVector, ShapeProperty


## \ingroup Lottie
class Transform(TgsObject):
    """!
    Layer transform
    """
    _props = [
        TgsProp("anchor_point", "a", MultiDimensional, False),
        TgsProp("position", "p", MultiDimensional, False),
        TgsProp("scale", "s", MultiDimensional, False),
        TgsProp("rotation", "r", Value, False),
        TgsProp("opacity", "o", Value, False),
        #TgsProp("position_x", "px", Value, False),
        #TgsProp("position_y", "py", Value, False),
        #TgsProp("position_z", "pz", Value, False),
        TgsProp("skew", "sk", Value, False),
        TgsProp("skew_axis", "sa", Value, False),
    ]

    def __init__(self):
        ## Transform Anchor Point
        self.anchor_point = MultiDimensional(NVector(0, 0))
        ## Transform Position
        self.position = MultiDimensional(NVector(0, 0))
        ## Transform Scale
        self.scale = MultiDimensional(NVector(100, 100))
        ## Transform Rotation
        self.rotation = Value(0)
        ## Transform Opacity
        self.opacity = Value(100)

        """
        # Transform Position X
        #self.position_x = Value()
        ## Transform Position Y
        #self.position_y = Value()
        ## Transform Position Z
        #self.position_z = Value()
        """

        ## Transform Skew
        self.skew = Value(0)
        ## Transform Skew Axis.
        ## An angle, if 0 skews on the X axis, if 90 skews on the Y axis
        self.skew_axis = Value(0)


## \ingroup Lottie
class MaskMode(TgsEnum):
    """!
    How masks interact with each other
    \see https://helpx.adobe.com/after-effects/using/alpha-channels-masks-mattes.html
    """
    No = "n"
    Add = "a"
    Subtract = "s"
    Intersect = "i"
    ## @note Not in lottie web
    Lightent = "l"
    ## @note Not in lottie web
    Darken = "d"
    ## @note Not in lottie web
    Difference = "f"


## \ingroup Lottie
## \todo Implement SVG/SIF I/O
class Mask(TgsObject):
    _props = [
        TgsProp("inverted", "inv", bool, False),
        TgsProp("name", "nm", str, False),
        TgsProp("shape", "pt", ShapeProperty, False),
        TgsProp("opacity", "o", Value, False),
        TgsProp("mode", "mode", MaskMode, False),
        TgsProp("dilate", "x", Value, False),
    ]

    def __init__(self):
        ## Inverted Mask flag
        self.inverted = False
        ## Mask name. Used for expressions and effects.
        self.name = None
        ## Mask vertices
        self.shape = ShapeProperty()
        ## Mask opacity.
        self.opacity = Value(100)
        ## Mask mode. Not all mask types are supported.
        self.mode = MaskMode.Intersect
        self.dilate = Value(0)
