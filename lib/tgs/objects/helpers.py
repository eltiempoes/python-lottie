from .base import TgsObject, TgsProp, todo_func
from .properties import MultiDimensional, Value, NVector


##\ingroup Lottie
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
        self.anchor_point = MultiDimensional(NVector(0, 0, 0))
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
        self.skew = Value()
        ## Transform Skew Axis.
        ## An angle, if 0 skews on the X axis, if 90 skews on the Y axis
        self.skew_axis = Value()


##\ingroup Lottie
## \todo check
class Mask(TgsObject):
    _props = [
        TgsProp("inverted", "inv", float, False),
        TgsProp("name", "nm", str, False),
        TgsProp("points", "pt", todo_func, False),
        TgsProp("opacity", "o", todo_func, False),
        TgsProp("mode", "mode", str, False),
    ]

    def __init__(self):
        ## Inverted Mask flag
        self.inverted = None
        ## Mask name. Used for expressions and effects.
        self.name = ""
        ## Mask vertices
        self.points = ShapeProperty() # ShapeProperty, ShapePropertyKeyframed
        ## Mask opacity.
        self.opacity = Value(100) # Const, ConstKeyframed
        ## Mask mode. Not all mask types are supported.
        self.mode = ""
