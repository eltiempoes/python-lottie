from .base import TgsObject, TgsProp, todo_func
from .properties import Value, MultiDimensional
from .enums import LineCap, LineJoin, Composite, StarType
from .helpers import Transform


def load_shape(lottiedict):
    shapes = {
        'sh': Shape,
        'rc': Rect,
        'el': Ellipse,
        'sr': Star,
        'fl': Fill,
        'gf': GFill,
        'gs': GStroke,
        'st': Stroke,
        'mm': Merge,
        'tm': Trim,
        'gr': Group,
        'rp': Repeater,
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


class Fill(TgsObject):
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("opacity", "o", Value, False),
        TgsProp("color", "c", MultiDimensional, False),
    ]

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = None
        # Shape content type.
        self.type = 'fl'
        # Fill Opacity
        self.opacity = Value(100)
        # Fill Color
        self.color = MultiDimensional([1, 1, 1])


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


class Repeater(TgsObject): # TODO check
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("copies", "c", Value, False),
        TgsProp("offset", "o", Value, False),
        TgsProp("composite", "m", float, False),
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
        self.composite = Composite.default()
        # Transform values for each repeater copy
        self.transform = Transform()


class GFill(TgsObject): # TODO check
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("opacity", "o", Value, False),
        TgsProp("start_point", "s", MultiDimensional, False),
        TgsProp("end_point", "e", MultiDimensional, False),
        TgsProp("gradient_type", "t", float, False),
        TgsProp("highlight_length", "h", Value, False),
        TgsProp("highlight_angle", "a", Value, False),
        TgsProp("gradient_colors", "g", float, False),
    ]

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = None
        # Shape content type.
        self.type = 'gf'
        # Fill Opacity
        self.opacity = Value() # Value, ValueKeyframed
        # Gradient Start Point
        self.start_point = MultiDimensional() # MultiDimensional, MultiDimensionalKeyframed
        # Gradient End Point
        self.end_point = MultiDimensional() # MultiDimensional, MultiDimensionalKeyframed
        # Gradient Type
        self.gradient_type = 1 # 1: Linear, 2: Radial
        # Gradient Highlight Length. Only if type is Radial
        self.highlight_length = Value() # Value, ValueKeyframed
        # Highlight Angle. Only if type is Radial
        self.highlight_angle = Value() # Value, ValueKeyframed
        # Gradient Colors
        self.gradient_colors = None


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

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = None
        # Shape content type.
        self.type = 'st'
        # Stroke Line Cap
        self.line_cap = LineCap.default()
        # Stroke Line Join
        self.line_join = LineJoin.default()
        # Stroke Miter Limit. Only if Line Join is set to Miter.
        self.miter_limit = 0
        # Stroke Opacity
        self.opacity = Value(100)
        # Stroke Width
        self.width = Value(1)
        # Stroke Color
        self.color = MultiDimensional([0, 0, 0])


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


class Shape(TgsObject): # TODO check
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("direction", "d", float, False),
        TgsProp("type", "ty", str, False),
        TgsProp("vertices", "ks", todo_func, False),
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
        self.vertices = ShapeProperty() # ShapeProperty, ShapePropertyKeyframed


class TransformShape(TgsObject): # TODO check
    _props = [
        TgsProp("name", "nm", str, False),
        TgsProp("anchor_point", "a", MultiDimensional, False),
        TgsProp("position", "p", MultiDimensional, False),
        TgsProp("scale", "s", MultiDimensional, False),
        TgsProp("rotation", "r", Value, False),
        TgsProp("opacity", "o", Value, False),
        TgsProp("skew", "sk", Value, False),
        TgsProp("skew_axis", "sa", Value, False),
    ]

    def __init__(self):
        # After Effect's Name. Used for expressions.
        self.name = None
        # Shape Transform Anchor Point
        self.anchor_point = MultiDimensional() # MultiDimensional, MultiDimensionalKeyframed
        # Shape Transform Position
        self.position = MultiDimensional() # MultiDimensional, MultiDimensionalKeyframed
        # Shape Transform Scale
        self.scale = MultiDimensional() # MultiDimensional, MultiDimensionalKeyframed
        # Shape Transform Rotation
        self.rotation = Value() # Value, ValueKeyframed
        # Shape Transform Opacity
        self.opacity = Value() # Value, ValueKeyframed
        # Shape Transform Skew
        self.skew = Value() # Value, ValueKeyframed
        # Shape Transform Skew Axis
        self.skew_axis = Value() # Value, ValueKeyframed


class Group(TgsObject): # TODO check
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("number_of_properties", "np", float, False),
        TgsProp("shapes", "it", load_shape, True), # shapes?
    ]

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = None
        # Shape content type.
        self.type = 'gr'
        # Group number of properties. Used for expressions.
        self.number_of_properties = 0
        # Group list of items
        self.shapes = [] # Shape, Rect, Ellipse, Star, Fill, GFill, GStroke, Stroke, Merge, Trim, Group, RoundedCorners, TransformShape


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
        TgsProp("star_type", "sy", float, False),
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


class GStroke(TgsObject): # TODO check
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("opacity", "o", Value, False),
        TgsProp("start_point", "s", MultiDimensional, False),
        TgsProp("end_point", "e", MultiDimensional, False),
        TgsProp("gradient_type", "t", float, False),
        TgsProp("highlight_length", "h", Value, False),
        TgsProp("highlight_angle", "a", Value, False),
        TgsProp("gradient_colors", "g", float, False),
        TgsProp("stroke_width", "w", Value, False),
        TgsProp("line_cap", "lc", float, False),
        TgsProp("line_join", "lj", float, False),
        TgsProp("miter_limit", "ml", float, False),
    ]

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = None
        # Shape content type.
        self.type = 'gs'
        # Stroke Opacity
        self.opacity = Value() # Value, ValueKeyframed
        # Gradient Start Point
        self.start_point = MultiDimensional() # MultiDimensional, MultiDimensionalKeyframed
        # Gradient End Point
        self.end_point = MultiDimensional() # MultiDimensional, MultiDimensionalKeyframed
        # Gradient Type
        self.gradient_type = 1 # 1: Linear, 2: Radial
        # Gradient Highlight Length. Only if type is Radial
        self.highlight_length = Value() # Value, ValueKeyframed
        # Highlight Angle. Only if type is Radial
        self.highlight_angle = Value() # Value, ValueKeyframed
        # Gradient Colors
        self.gradient_colors = None
        # Gradient Stroke Width
        self.stroke_width = Value() # Value, ValueKeyframed
        # Gradient Stroke Line Cap
        self.line_cap = LineCap.default()
        # Gradient Stroke Line Join
        self.line_join = LineJoin.default()
        # Gradient Stroke Miter Limit. Only if Line Join is set to Miter.
        self.miter_limit = 0
