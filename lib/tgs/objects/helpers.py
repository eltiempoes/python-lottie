from .base import TgsObject, TgsProp, todo_func
from .properties import MultiDimensional, Value


class Transform(TgsObject):
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
        # Transform Anchor Point
        self.anchor_point = MultiDimensional([0, 0, 0]) # MultiDimensional, MultiDimensionalKeyframed
        # Transform Position
        self.position = MultiDimensional([0, 0]) # MultiDimensional, MultiDimensionalKeyframed
        # Transform Scale
        self.scale = MultiDimensional([100, 100, 100]) # MultiDimensional, MultiDimensionalKeyframed
        # Transform Rotation
        self.rotation = Value(0) # Value, ValueKeyframed
        # Transform Opacity
        self.opacity = Value(100) # Value, ValueKeyframed
        # Transform Position X
        #self.position_x = Value() # Value, ValueKeyframed
        ## Transform Position Y
        #self.position_y = Value() # Value, ValueKeyframed
        ## Transform Position Z
        #self.position_z = Value() # Value, ValueKeyframed
        # Transform Skew
        self.skew = Value() # Value, ValueKeyframed
        # Transform Skew Axis
        self.skew_axis = Value() # Value, ValueKeyframed


class Mask(TgsObject): # TODO check
    _props = [
        TgsProp("inverted", "inv", float, False),
        TgsProp("name", "nm", str, False),
        TgsProp("points", "pt", todo_func, False),
        TgsProp("opacity", "o", todo_func, False),
        TgsProp("mode", "mode", str, False),
    ]

    def __init__(self):
        # Inverted Mask flag
        self.inverted = None
        # Mask name. Used for expressions and effects.
        self.name = ""
        # Mask vertices
        self.points = ShapeProperty() # ShapeProperty, ShapePropertyKeyframed
        # Mask opacity.
        self.opacity = Value(100) # Const, ConstKeyframed
        # Mask mode. Not all mask types are supported.
        self.mode = ""
