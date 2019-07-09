from .base import TgsObject, TgsProp, TgsEnum, todo_func
from .properties import Value, MultiDimensional, GradientColors, ShapeProperty
from .helpers import Transform


def load_shape(lottiedict):
    shapes = {
        'sh': Shape,
        'rc': Rect,
        'el': Ellipse,
        'sr': Star,
        'fl': Fill,
        'gf': GradientFill,
        'gs': GradientStroke,
        'st': Stroke,
        'mm': Merge,
        'tm': Trim,
        'gr': Group,
        'rp': Repeater,
        'tr': TransformShape,
        # RoundedCorners? mentioned but not defined
    }
    return shapes[lottiedict["ty"]].load(lottiedict)


class Rect(TgsObject):
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("direction", "d", float, False),
        TgsProp("type", "ty", str, False),
        TgsProp("position", "p", MultiDimensional, False),
        TgsProp("size", "s", MultiDimensional, False),
        TgsProp("rounded_corners", "r", Value, False),
    ]

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = None
        # After Effect's Direction. Direction how the shape is drawn. Used for trim path for example.
        self.direction = 0
        # Shape content type.
        self.type = 'rc'
        # Rect's position
        self.position = MultiDimensional([0, 0])
        # Rect's size
        self.size = MultiDimensional([0, 0])
        # Rect's rounded corners
        self.rounded_corners = Value()


class StarType(TgsEnum):
    Star = 1
    Polygon = 2


class Star(TgsObject):
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("direction", "d", float, False),
        TgsProp("type", "ty", str, False),
        TgsProp("position", "p", MultiDimensional, False),
        TgsProp("inner_radius", "ir", Value, False),
        TgsProp("inner_roundness", "is", Value, False),
        TgsProp("outer_radius", "or", Value, False),
        TgsProp("outer_roundness", "os", Value, False),
        TgsProp("rotation", "r", Value, False),
        TgsProp("points", "pt", Value, False),
        TgsProp("star_type", "sy", StarType, False),
    ]

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = None
        # After Effect's Direction. Direction how the shape is drawn. Used for trim path for example.
        self.direction = 0
        # Shape content type.
        self.type = 'sr'
        # Star's position
        self.position = MultiDimensional([0, 0]) # MultiDimensional, MultiDimensionalKeyframed
        # Star's inner radius. (Star only)
        self.inner_radius = Value() # Value, ValueKeyframed
        # Star's inner roundness. (Star only)
        self.inner_roundness = Value() # Value, ValueKeyframed
        # Star's outer radius.
        self.outer_radius = Value() # Value, ValueKeyframed
        # Star's outer roundness.
        self.outer_roundness = Value() # Value, ValueKeyframed
        # Star's rotation.
        self.rotation = Value() # Value, ValueKeyframed
        # Star's number of points.
        self.points = Value(5) # Value, ValueKeyframed
        # Star's type. Polygon or Star.
        self.star_type = StarType.Star


class Ellipse(TgsObject):
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("direction", "d", float, False),
        TgsProp("type", "ty", str, False),
        TgsProp("position", "p", MultiDimensional, False),
        TgsProp("size", "s", MultiDimensional, False),
    ]

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = None
        # After Effect's Direction. Direction how the shape is drawn. Used for trim path for example.
        self.direction = 1
        # Shape content type.
        self.type = 'el'
        # Ellipse's position
        self.position = MultiDimensional([0, 0])
        # Ellipse's size
        self.size = MultiDimensional([0, 0])


class Shape(TgsObject):
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("direction", "d", float, False),
        TgsProp("type", "ty", str, False),
        TgsProp("vertices", "ks", ShapeProperty, False),
    ]

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = None
        # After Effect's Direction. Direction how the shape is drawn. Used for trim path for example.
        self.direction = 0
        # Shape content type.
        self.type = 'sh'
        # Shape's vertices
        self.vertices = ShapeProperty()


class Group(TgsObject):
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("number_of_properties", "np", float, False),
        TgsProp("shapes", "it", load_shape, True),
        TgsProp("property_index", "ix", int, False),
    ]

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = None
        # Shape content type.
        self.type = 'gr'
        # Group number of properties. Used for expressions.
        self.number_of_properties = None
        # Group list of items
        self.shapes = [TransformShape()]
        self.property_index = None

    def add_shape(self, shape):
        self.shapes.insert(-1, shape)
        return shape

    @property
    def transform(self):
        return self.shapes[-1]


class Fill(TgsObject):
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("opacity", "o", Value, False),
        TgsProp("color", "c", MultiDimensional, False),
    ]

    def __init__(self, color=[1, 1, 1]):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = None
        # Shape content type.
        self.type = 'fl'
        # Fill Opacity
        self.opacity = Value(100)
        # Fill Color
        self.color = MultiDimensional(color)


class GradientType(TgsEnum):
    Linear = 1
    Radial = 2


class GradientFill(TgsObject):
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("opacity", "o", Value, False),
        TgsProp("start_point", "s", MultiDimensional, False),
        TgsProp("end_point", "e", MultiDimensional, False),
        TgsProp("gradient_type", "t", GradientType, False),
        TgsProp("highlight_length", "h", Value, False),
        TgsProp("highlight_angle", "a", Value, False),
        TgsProp("colors", "g", GradientColors, False),
    ]

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = None
        # Shape content type.
        self.type = 'gf'
        # Fill Opacity
        self.opacity = Value(100)
        # Gradient Start Point
        self.start_point = MultiDimensional([0, 0])
        # Gradient End Point
        self.end_point = MultiDimensional([0, 0])
        # Gradient Type
        self.gradient_type = GradientType.Linear
        # Gradient Highlight Length. Only if type is Radial
        self.highlight_length = Value()
        # Highlight Angle. Only if type is Radial
        self.highlight_angle = Value()
        # Gradient Colors
        self.colors = GradientColors()


class LineJoin(TgsEnum):
    Miter = 1
    Round = 2
    Bevel = 3


class LineCap(TgsEnum):
    Butt = 1
    Round = 2
    Square = 3


class Stroke(TgsObject):
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("line_cap", "lc", float, False),
        TgsProp("line_join", "lj", float, False),
        TgsProp("miter_limit", "ml", float, False),
        TgsProp("opacity", "o", Value, False),
        TgsProp("width", "w", Value, False),
        TgsProp("color", "c", MultiDimensional, False),
    ]

    def __init__(self, color=[0, 0, 0], width=1):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = None
        # Shape content type.
        self.type = 'st'
        # Stroke Line Cap
        self.line_cap = LineCap.Round
        # Stroke Line Join
        self.line_join = LineJoin.Round
        # Stroke Miter Limit. Only if Line Join is set to Miter.
        self.miter_limit = 0
        # Stroke Opacity
        self.opacity = Value(100)
        # Stroke Width
        self.width = Value(width)
        # Stroke Color
        self.color = MultiDimensional(color)


class GradientStroke(TgsObject):
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("opacity", "o", Value, False),
        TgsProp("start_point", "s", MultiDimensional, False),
        TgsProp("end_point", "e", MultiDimensional, False),
        TgsProp("gradient_type", "t", GradientType, False),
        TgsProp("highlight_length", "h", Value, False),
        TgsProp("highlight_angle", "a", Value, False),
        TgsProp("colors", "g", GradientColors, False),
        TgsProp("stroke_width", "w", Value, False),
        TgsProp("line_cap", "lc", float, False),
        TgsProp("line_join", "lj", float, False),
        TgsProp("miter_limit", "ml", float, False),
    ]

    def __init__(self, stroke_width=1):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = None
        # Shape content type.
        self.type = 'gs'
        # Stroke Opacity
        self.opacity = Value(100)
        # Gradient Start Point
        self.start_point = MultiDimensional([0, 0])
        # Gradient End Point
        self.end_point = MultiDimensional([0, 0])
        # Gradient Type
        self.gradient_type = GradientType.Linear
        # Gradient Highlight Length. Only if type is Radial
        self.highlight_length = Value()
        # Highlight Angle. Only if type is Radial
        self.highlight_angle = Value()
        # Gradient Colors
        self.colors = GradientColors()
        # Gradient Stroke Width
        self.stroke_width = Value(stroke_width)
        # Gradient Stroke Line Cap
        self.line_cap = LineCap.Round
        # Gradient Stroke Line Join
        self.line_join = LineJoin.Round
        # Gradient Stroke Miter Limit. Only if Line Join is set to Miter.
        self.miter_limit = 0


class TransformShape(TgsObject):
    _props = [
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),

        TgsProp("anchor_point", "a", MultiDimensional, False),
        TgsProp("position", "p", MultiDimensional, False),
        TgsProp("scale", "s", MultiDimensional, False),
        TgsProp("rotation", "r", Value, False),
        TgsProp("opacity", "o", Value, False),
        TgsProp("skew", "sk", Value, False),
        TgsProp("skew_axis", "sa", Value, False),
    ]

    def __init__(self):
        self.name = None
        self.type = 'tr'
        # Transform Anchor Point
        self.anchor_point = MultiDimensional([0, 0])
        # Transform Position
        self.position = MultiDimensional([0, 0])
        # Transform Scale
        self.scale = MultiDimensional([100, 100])
        # Transform Rotation
        self.rotation = Value(0)
        # Transform Opacity
        self.opacity = Value(100)
        # Transform Skew
        self.skew = Value(0)
        # Transform Skew Axis
        self.skew_axis = Value(0)


class Trim(TgsObject): # TODO check
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("start", "s", Value, False),
        TgsProp("end", "e", Value, False),
        TgsProp("offset", "o", Value, False),
    ]

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = None
        # Shape content type.
        self.type = 'tm'
        # Trim Start.
        self.start = Value() # Value, ValueKeyframed
        # Trim End.
        self.end = Value() # Value, ValueKeyframed
        # Trim Offset.
        self.offset = Value() # Value, ValueKeyframed


class Composite(TgsEnum):
    Above = 1
    Below = 2


class Repeater(TgsObject): # TODO check
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("copies", "c", Value, False),
        TgsProp("offset", "o", Value, False),
        TgsProp("composite", "m", Composite, False),
        TgsProp("transform", "tr", Transform, False),
    ]

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = None
        # Shape content type.
        self.type = 'rp'
        # Number of Copies
        self.copies = Value() # Value, ValueKeyframed
        # Offset of Copies
        self.offset = Value() # Value, ValueKeyframed
        # Composite of copies
        self.composite = Composite.Above
        # Transform values for each repeater copy
        self.transform = Transform()


class Round(TgsObject): # TODO check
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("radius", "r", Value, False),
    ]

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = None
        # Shape content type.
        self.type = 'rd'
        # Rounded Corner Radius
        self.radius = Value() # Value, ValueKeyframed


class Merge(TgsObject): # TODO check
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("merge_mode", "mm", float, False),
    ]

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = None
        # Shape content type. THIS FEATURE IS NOT SUPPORTED. It's exported because if you export it, they will come.
        self.type = 'mm'
        # Merge Mode
        self.merge_mode = 0
