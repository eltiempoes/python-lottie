import enum


def _to_dict(v):
    if isinstance(v, Tgs):
        return v.to_dict()
    elif isinstance(v, bool):
        return int(v)
    elif isinstance(v, list):
        return list(map(_to_dict, v))
    elif isinstance(v, (int, float, str)):
        return v
    else:
        raise Exception("Unknown value %r" % v)


class Tgs:
    def to_dict(self):
        raise NotImplementedError


class TgsEnum(Tgs, enum.Enum):
    def to_dict(self):
        return self.value


class TgsObject(Tgs):
    def to_dict(self):
        return {
            exp: _to_dict(getattr(self, name))
            for name, exp in self._props.items()
            if getattr(self, name) is not None
        }


class Index:
    def __init__(self):
            self._i = -1

    def __next__(self):
            self._i += 1
            return self._i


class Animation(TgsObject):
    _props = {
        "tgs": "tgs",
        "in_point": "ip",
        "out_point": "op",
        "frame_rate": "fr",
        "width": "w",
        "threedimensional": "ddd",
        "height": "h",
        "version": "v",
        "name": "nm",
        "layers": "layers",
        "assets": "assets",
        #"chars": "chars",
    }

    def __init__(self):
        self.tgs = 1
        # In Point of the Time Ruler. Sets the initial Frame of the animation.
        self.in_point = 0
        # Out Point of the Time Ruler. Sets the final Frame of the animation
        self.out_point = 0
        # Frame Rate
        self.frame_rate = 60
        # Composition Width
        self.width = 512
        # Composition has 3-D layers
        self.threedimensional = False
        # Composition Height
        self.height = 512
        # Bodymovin Version
        self.version = "5.5.2"
        # Composition name
        self.name = ""
        # List of Composition Layers
        self.layers = [] # ShapeLayer, SolidLayer, CompLayer, ImageLayer, NullLayer, TextLayer
        # source items that can be used in multiple places. Comps and Images for now.
        self.assets = [] # Image, Precomp
        # source chars for text layers
        #self.chars = [] # Chars


class FillEffect(TgsObject):
    _props = {
        "effect_index": "ix",
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "effects": "ef",
    }

    def __init__(self):
        # Effect Index. Used for expressions.
        self.effect_index = 0
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Effect type.
        self.type = 21
        # Effect List of properties.
        self.effects = [] # PointEffect, DropDownEffect, ColorEffect, DropDownEffect, SliderEffect, SliderEffect, SliderEffect


class StrokeEffect(TgsObject):
    _props = {
        "effect_index": "ix",
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "effects": "ef",
    }

    def __init__(self):
        # Effect Index. Used for expressions.
        self.effect_index = 0
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Effect type.
        self.type = 22
        # Effect List of properties.
        self.effects = [] # ColorEffect, CheckboxEffect, CheckboxEffect, ColorEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, DropDownEffect, DropDownEffect


class DropDownEffect(TgsObject):
    _props = {
        "effect_index": "ix",
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "value": "v",
    }

    def __init__(self):
        # Effect Index. Used for expressions.
        self.effect_index = 0
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Effect type.
        self.type = 7
        # Effect value.
        self.value = Value() # Value, ValueKeyframed


class TritoneEffect(TgsObject):
    _props = {
        "effect_index": "ix",
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "effects": "ef",
    }

    def __init__(self):
        # Effect Index. Used for expressions.
        self.effect_index = 0
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Effect type.
        self.type = 23
        # Effect List of properties.
        self.effects = [] # ColorEffect, ColorEffect, ColorEffect, SliderEffect


class GroupEffect(TgsObject):
    _props = {
        "effect_index": "ix",
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "effects": "ef",
        "enabled": "en",
    }

    def __init__(self):
        # Effect Index. Used for expressions.
        self.effect_index = 0
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Effect type.
        self.type = 5
        # Effect List of properties.
        self.effects = [] # IndexEffect
        # Enabled AE property value
        self.enabled = 0


class ColorEffect(TgsObject):
    _props = {
        "effect_index": "ix",
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "value": "v",
    }

    def __init__(self):
        # Effect Index. Used for expressions.
        self.effect_index = 0
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Effect type.
        self.type = 2
        # Effect value.
        self.value = MultiDimensional() # MultiDimensional, MultiDimensionalKeyframed


class ProLevelsEffect(TgsObject):
    _props = {
        "effect_index": "ix",
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "effects": "ef",
    }

    def __init__(self):
        # Effect Index. Used for expressions.
        self.effect_index = 0
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Effect type.
        self.type = 23
        # ffect List of properties.
        self.effects = [] # DropDownEffect, NoValueEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, NoValueEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect, SliderEffect


class AngleEffect(TgsObject):
    _props = {
        "effect_index": "ix",
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "value": "v",
    }

    def __init__(self):
        # Effect Index. Used for expressions. NOT USED. EQUALS SLIDER.
        self.effect_index = 0
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Effect type.
        self.type = 1
        # Effect value.
        self.value = Value() # Value, ValueKeyframed


class SliderEffect(TgsObject):
    _props = {
        "effect_index": "ix",
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "value": "v",
    }

    def __init__(self):
        # Effect Index. Used for expressions.
        self.effect_index = 0
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Effect type.
        self.type = 0
        # Effect value.
        self.value = Value() # Value, ValueKeyframed


class CheckBoxEffect(TgsObject):
    _props = {
        "effect_index": "ix",
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "value": "v",
    }

    def __init__(self):
        # Effect Index. Used for expressions.
        self.effect_index = 0
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Effect type.
        self.type = 7
        # Effect value.
        self.value = Value() # Value, ValueKeyframed


class PointEffect(TgsObject):
    _props = {
        "effect_index": "ix",
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "value": "v",
    }

    def __init__(self):
        # Effect Index. Used for expressions.
        self.effect_index = 0
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Effect type.
        self.type = 2
        # Effect value.
        self.value = [] # MultiDimensional, MultiDimensionalKeyframed


class TintEffect(TgsObject):
    _props = {
        "effect_index": "ix",
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "effects": "ef",
    }

    def __init__(self):
        # Effect Index. Used for expressions.
        self.effect_index = 0
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Effect type.
        self.type = 20
        # Effect List of properties.
        self.effects = [] # ColorEffect, ColorEffect, SliderEffect


class LayerEffect(TgsObject):
    _props = {
        "effect_index": "ix",
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "value": "v",
    }

    def __init__(self):
        # Effect Index. Used for expressions. NOT USED. EQUALS SLIDER.
        self.effect_index = 0
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Effect type.
        self.type = 0
        # Effect value.
        self.value = Value()


class Image(TgsObject):
    _props = {
        "height": "h",
        "width": "w",
        "id": "id",
        "image_name": "p",
        "image_path": "u",
    }

    def __init__(self):
        # Image Height
        self.height = 0
        # Image Width
        self.width = 0
        # Image ID
        self.id = ""
        # Image name
        self.image_name = ""
        # Image path
        self.image_path = ""


class Chars(TgsObject):
    _props = {
        "character": "ch",
        "font_family": "fFamily",
        "font_size": "size",
        "font_style": "style",
        "width": "w",
        "character_data": "data",
    }

    def __init__(self):
        # Character Value
        self.character = ""
        # Character Font Family
        self.font_family = ""
        # Character Font Size
        self.font_size = ""
        # Character Font Style
        self.font_style = ""
        # Character Width
        self.width = 0
        # Character Data
        self.character_data = None


class Precomp(TgsObject):
    _props = {
        "id": "id",
        "layers": "layers",
    }

    def __init__(self):
        # Precomp ID
        self.id = ""
        # List of Precomp Layers
        self.layers = [] # ShapeLayer, SolidLayer, CompLayer, ImageLayer, NullLayer, TextLayer


class ShapeKeyframed(TgsObject):
    _props = {
        "keyframes": "k",
        "expression": "x",
        "property_index": "ix",
        "in_tangent": "ti",
        "out_tangent": "to",
    }

    def __init__(self):
        # Property Value keyframes
        self.keyframes = [] # ShapePropKeyframe
        # Property Expression. An AE expression that modifies the value.
        self.expression = ""
        # Property Index. Used for expressions.
        self.property_index = 0
        # In Spatial Tangent. Only for spatial properties. Array of numbers.
        self.in_tangent = []
        # Out Spatial Tangent. Only for spatial properties. Array of numbers.
        self.out_tangent = []


class Shape(TgsObject):
    _props = {
        "value": "k",
        "expression": "x",
        "property_index": "ix",
        "animated": "a",
    }

    def __init__(self):
        # Property Value
        self.value = ShapeProp()
        # Property Expression. An AE expression that modifies the value.
        self.expression = ""
        # Property Index. Used for expressions.
        self.property_index = 0
        # Defines if property is animated
        self.animated = 0


class OffsetKeyframe(TgsObject):
    _props = {
        "start": "s",
        "time": "t",
        "in_value": "i",
        "out_value": "o",
    }

    def __init__(self):
        # Start value of keyframe segment.
        self.start = [] # number
        # Start time of keyframe segment.
        self.time = 0
        # Bezier curve interpolation in value.
        self.in_value = None
        # Bezier curve interpolation out value.
        self.out_value = None


class DoubleKeyframe(TgsObject):
    _props = {
        "start": "s",
        "time": "t",
        "in_value": "i",
        "out_value": "o",
    }

    def __init__(self):
        # Start value of keyframe segment.
        self.start = 0
        # Start time of keyframe segment.
        self.time = 0
        # Bezier curve interpolation in value.
        self.in_value = None
        # Bezier curve interpolation out value.
        self.out_value = None


class ValueKeyframe(TgsObject):
    _props = {
        "start": "s",
        "time": "t",
        "in_value": "i",
    }

    def __init__(self):
        # Start value of keyframe segment.
        self.start = 0
        # Start time of keyframe segment.
        self.time = 0
        # Bezier curve interpolation in value.
        self.in_value = None


class MultiDimensionalKeyframed(TgsObject):
    _props = {
        "keyframes": "k",
        "expression": "x",
        "property_index": "ix",
        "in_tangent": "ti",
        "out_tangent": "to",
    }

    def __init__(self):
        # Property Value keyframes
        self.keyframes = [] # OffsetKeyframe
        # Property Expression. An AE expression that modifies the value.
        self.expression = ""
        # Property Index. Used for expressions.
        self.property_index = 0
        # In Spatial Tangent. Only for spatial properties. Array of numbers.
        self.in_tangent = []
        # Out Spatial Tangent. Only for spatial properties. Array of numbers.
        self.out_tangent = []


class ShapePropKeyframe(TgsObject):
    _props = {
        "start": "s",
        "time": "t",
        "in_value": "i",
        "out_value": "o",
    }

    def __init__(self):
        # Start value of keyframe segment.
        self.start = [] # ShapeProp
        # Start time of keyframe segment.
        self.time = 0
        # Bezier curve interpolation in value.
        self.in_value = None
        # Bezier curve interpolation out value.
        self.out_value = None


class ShapeProp(TgsObject):
    _props = {
        "closed": "c",
        "in_point": "i",
        "out_point": "o",
        "vertices": "v",
    }

    def __init__(self):
        # Closed property of shape
        self.closed = None
        # Bezier curve In points. Array of 2 dimensional arrays.
        self.in_point = [] # array
        # Bezier curve Out points. Array of 2 dimensional arrays.
        self.out_point = [] # array
        # Bezier curve Vertices. Array of 2 dimensional arrays.
        self.vertices = [] # array


class Value(TgsObject):
    _props = {
        "value": "k",
        #"expression": "x",
        "property_index": "ix",
        "animated": "a",
    }

    def __init__(self, value=0):
        # Property Value
        self.value = value
        # Property Expression. An AE expression that modifies the value.
        self.expression = ""
        # Property Index. Used for expressions.
        self.property_index = 0
        self.animated = False


class ValueKeyframed(TgsObject):
    _props = {
        "keyframes": "k",
        "expression": "x",
        "property_index": "ix",
    }

    def __init__(self):
        # Property Value keyframes
        self.keyframes = [] # ValueKeyframe
        # Property Expression. An AE expression that modifies the value.
        self.expression = ""
        # Property Index. Used for expressions.
        self.property_index = 0


class MultiDimensional(TgsObject):
    _props = {
        "value": "k",
        #"expression": "x",
        "property_index": "ix",
        "animated": "a",
    }

    def __init__(self, value=None):
        # Property Value
        self.value = value or []
        # Property Expression. An AE expression that modifies the value.
        self.expression = ""
        # Property Index. Used for expressions.
        self.property_index = 0
        self.animated = False


class Rect(TgsObject):
    _props = {
        "match_name": "mn",
        "name": "nm",
        "direction": "d",
        "type": "ty",
        "position": "p",
        "size": "s",
        "rounded_corners": "r",
    }

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # After Effect's Direction. Direction how the shape is drawn. Used for trim path for example.
        self.direction = 0
        # Shape content type.
        self.type = 'rc'
        # Rect's position
        self.position = MultiDimensional() # MultiDimensional, MultiDimensionalKeyframed
        # Rect's size
        self.size = MultiDimensional() # MultiDimensional, MultiDimensionalKeyframed
        # Rect's rounded corners
        self.rounded_corners = Value() # Value, ValueKeyframed


class Fill(TgsObject):
    _props = {
        #"match_name": "mn",
        #"name": "nm",
        "type": "ty",
        "opacity": "o",
        "color": "c",
    }

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Shape content type.
        self.type = 'fl'
        # Fill Opacity
        self.opacity = Value(100) # Value, ValueKeyframed
        # Fill Color
        self.color = MultiDimensional() # MultiDimensional, MultiDimensionalKeyframed


class Trim(TgsObject):
    _props = {
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "start": "s",
        "end": "e",
        "offset": "o",
    }

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Shape content type.
        self.type = 'tm'
        # Trim Start.
        self.start = Value() # Value, ValueKeyframed
        # Trim End.
        self.end = Value() # Value, ValueKeyframed
        # Trim Offset.
        self.offset = Value() # Value, ValueKeyframed


class Repeater(TgsObject):
    _props = {
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "copies": "c",
        "offset": "o",
        "composite": "m",
        "transform": "tr",
    }

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
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


class GFill(TgsObject):
    _props = {
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "opacity": "o",
        "start_point": "s",
        "end_point": "e",
        "gradient_type": "t",
        "highlight_length": "h",
        "highlight_angle": "a",
        "gradient_colors": "g",
    }

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Shape content type.
        self.type = 'gf'
        # Fill Opacity
        self.opacity = Value(100) # Value, ValueKeyframed
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
    _props = {
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "line_cap": "lc",
        "line_join": "lj",
        "miter_limit": "ml",
        "opacity": "o",
        "width": "w",
        "color": "c",
    }

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Shape content type.
        self.type = 'st'
        # Stroke Line Cap
        self.line_cap = LineCap.default()
        # Stroke Line Join
        self.line_join = LineJoin.default()
        # Stroke Miter Limit. Only if Line Join is set to Miter.
        self.miter_limit = 0
        # Stroke Opacity
        self.opacity = Value(100) # Value, ValueKeyframed
        # Stroke Width
        self.width = Value() # Value, ValueKeyframed
        # Stroke Color
        self.color = MultiDimensional() # MultiDimensional, MultiDimensionalKeyframed


class Round(TgsObject):
    _props = {
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "radius": "r",
    }

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Shape content type.
        self.type = 'rd'
        # Rounded Corner Radius
        self.radius = Value() # Value, ValueKeyframed


class Shape(TgsObject):
    _props = {
        "match_name": "mn",
        "name": "nm",
        "direction": "d",
        "type": "ty",
        "vertices": "ks",
    }

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # After Effect's Direction. Direction how the shape is drawn. Used for trim path for example.
        self.direction = 0
        # Shape content type.
        self.type = 'sh'
        # Shape's vertices
        self.vertices = Shape() # Shape, ShapeKeyframed


class TransformShape(TgsObject):
    _props = {
        "name": "nm",
        "anchor_point": "a",
        "position": "p",
        "scale": "s",
        "rotation": "r",
        "opacity": "o",
        "skew": "sk",
        "skew_axis": "sa",
    }

    def __init__(self):
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Shape Transform Anchor Point
        self.anchor_point = MultiDimensional([0, 0, 0]) # MultiDimensional, MultiDimensionalKeyframed
        # Shape Transform Position
        self.position = MultiDimensional([0, 0]) # MultiDimensional, MultiDimensionalKeyframed
        # Shape Transform Scale
        self.scale = MultiDimensional([1, 1, 1]) # MultiDimensional, MultiDimensionalKeyframed
        # Shape Transform Rotation
        self.rotation = Value(0) # Value, ValueKeyframed
        # Shape Transform Opacity
        self.opacity = Value(1001) # Value, ValueKeyframed
        # Shape Transform Skew
        self.skew = Value(0) # Value, ValueKeyframed
        # Shape Transform Skew Axis
        self.skew_axis = Value(0) # Value, ValueKeyframed


class Group(TgsObject):
    _props = {
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "number_of_properties": "np",
        "items": "it",
    }

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Shape content type.
        self.type = 'gr'
        # Group number of properties. Used for expressions.
        self.number_of_properties = 0
        # Group list of items
        self.items = [] # Shape, Rect, Ellipse, Star, Fill, GFill, GStroke, Stroke, Merge, Trim, Group, RoundedCorners, Transform


class Star(TgsObject):
    _props = {
        "match_name": "mn",
        "name": "nm",
        "direction": "d",
        "type": "ty",
        "position": "p",
        "inner_radius": "ir",
        "inner_roundness": "is",
        "outer_radius": "or",
        "outer_roundness": "os",
        "rotation": "r",
        "points": "pt",
        "star_type": "sy",
    }

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # After Effect's Direction. Direction how the shape is drawn. Used for trim path for example.
        self.direction = 0
        # Shape content type.
        self.type = 'sr'
        # Star's position
        self.position = MultiDimensional() # MultiDimensional, MultiDimensionalKeyframed
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
        self.points = Value() # Value, ValueKeyframed
        # Star's type. Polygon or Star.
        self.star_type = 1 # 1: Star, 2: Polygon


class Ellipse(TgsObject):
    _props = {
        #"match_name": "mn",
        #"name": "nm",
        "index": "ix",
        "direction": "d",
        "type": "ty",
        "position": "p",
        "size": "s",
    }

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # After Effect's Direction. Direction how the shape is drawn. Used for trim path for example.
        self.direction = 0
        # Shape content type.
        self.type = 'el'
        # Ellipse's position
        self.position = MultiDimensional() # MultiDimensional, MultiDimensionalKeyframed
        # Ellipse's size
        self.size = MultiDimensional() # MultiDimensional, MultiDimensionalKeyframed
        self.index = 0


class Merge(TgsObject):
    _props = {
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "merge_mode": "mm",
    }

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Shape content type. THIS FEATURE IS NOT SUPPORTED. It's exported because if you export it, they will come.
        self.type = 'mm'
        # Merge Mode
        self.merge_mode = 0


class GStroke(TgsObject):
    _props = {
        "match_name": "mn",
        "name": "nm",
        "type": "ty",
        "opacity": "o",
        "start_point": "s",
        "end_point": "e",
        "gradient_type": "t",
        "highlight_length": "h",
        "highlight_angle": "a",
        "gradient_colors": "g",
        "stroke_width": "w",
        "line_cap": "lc",
        "line_join": "lj",
        "miter_limit": "ml",
    }

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        self.match_name = ""
        # After Effect's Name. Used for expressions.
        self.name = ""
        # Shape content type.
        self.type = 'gs'
        # Stroke Opacity
        self.opacity = Value(100) # Value, ValueKeyframed
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


class NullLayer(TgsObject):
    _props = {
        "type": "ty",
        "transform": "ks",
        "auto_orient": "ao",
        "threedimensional": "ddd",
        "index": "ind",
        "css_class": "cl",
        "layer_html_id": "ln",
        "in_point": "ip",
        "out_point": "op",
        "start_time": "st",
        "name": "nm",
        "effects": "ef",
        "stretch": "sr",
        "parent": "parent",
    }

    def __init__(self):
        # Type of layer: Null.
        self.type = 3
        # Transform properties
        self.transform = Transform()
        # Auto-Orient along path AE property.
        self.auto_orient = False
        # 3d layer flag
        self.threedimensional = False
        # Layer index in AE. Used for parenting and expressions.
        self.index = 0
        # Parsed layer name used as html class on SVG/HTML renderer
        self.css_class = ""
        # Parsed layer name used as html id on SVG/HTML renderer
        self.layer_html_id = ""
        # In Point of layer. Sets the initial frame of the layer.
        self.in_point = 0
        # Out Point of layer. Sets the final frame of the layer.
        self.out_point = 0
        # Start Time of layer. Sets the start time of the layer.
        self.start_time = 0
        # After Effects Layer Name. Used for expressions.
        self.name = ""
        # List of Effects
        self.effects = [] # IndexEffect
        # Layer Time Stretching
        self.stretch = 0
        # Layer Parent. Uses ind of parent.
        self.parent = None


class TextLayer(TgsObject):
    _props = {
        "type": "ty",
        "transform": "ks",
        "auto_orient": "ao",
        "blend_mode": "bm",
        "threedimensional": "ddd",
        "index": "ind",
        "css_class": "cl",
        "layer_html_id": "ln",
        "in_point": "ip",
        "out_point": "op",
        "start_time": "st",
        "name": "nm",
        "has_masks": "hasMask",
        "masks_properties": "masksProperties",
        "effects": "ef",
        "stretch": "sr",
        "parent": "parent",
        "text_data": "t",
    }

    def __init__(self):
        # Type of layer: Text.
        self.type = 0
        # Transform properties
        self.transform = Transform()
        # Auto-Orient along path AE property.
        self.auto_orient = False
        # Blend Mode
        self.blend_mode = BlendMode.default()
        # 3d layer flag
        self.threedimensional = False
        # Layer index in AE. Used for parenting and expressions.
        self.index = 0
        # Parsed layer name used as html class on SVG/HTML renderer
        self.css_class = ""
        # Parsed layer name used as html id on SVG/HTML renderer
        self.layer_html_id = ""
        # In Point of layer. Sets the initial frame of the layer.
        self.in_point = 0
        # Out Point of layer. Sets the final frame of the layer.
        self.out_point = 0
        # Start Time of layer. Sets the start time of the layer.
        self.start_time = 0
        # After Effects Layer Name. Used for expressions.
        self.name = 0
        # Boolean when layer has a mask. Will be deprecated in favor of checking masksProperties.
        self.has_masks = 0
        # List of Masks
        self.masks_properties = [] # Mask
        # Auto-Orient along path AE property.
        self.effects = False
        # Layer Time Stretching
        self.stretch = 0
        # Layer Parent. Uses ind of parent.
        self.parent = None
        # Text Data
        self.text_data = None


class ShapeLayer(TgsObject):
    _props = {
        "type": "ty",
        "transform": "ks",
        "auto_orient": "ao",
        "blend_mode": "bm",
        "threedimensional": "ddd",
        "index": "ind",
        #"css_class": "cl",
        #"layer_html_id": "ln",
        "in_point": "ip",
        "out_point": "op",
        "start_time": "st",
        "name": "nm",
        #"has_masks": "hasMask",
        #"masks_properties": "masksProperties",
        #"effects": "ef",
        "stretch": "sr",
        "parent": "parent",
        "items": "shapes", # "it" in the JSON schema...
        "markers": "markers", # ?
    }

    def __init__(self):
        # Type of layer: Shape.
        self.type = 4
        # Transform properties
        self.transform = Transform()
        # Auto-Orient along path AE property.
        self.auto_orient = False
        # Blend Mode
        self.blend_mode = BlendMode.default()
        # 3d layer flag
        self.threedimensional = False
        # Layer index in AE. Used for parenting and expressions.
        self.index = 0
        # Parsed layer name used as html class on SVG/HTML renderer
        self.css_class = ""
        # Parsed layer name used as html id on SVG/HTML renderer
        self.layer_html_id = ""
        # In Point of layer. Sets the initial frame of the layer.
        self.in_point = 0
        # Out Point of layer. Sets the final frame of the layer.
        self.out_point = 0
        # Start Time of layer. Sets the start time of the layer.
        self.start_time = 0
        # After Effects Layer Name. Used for expressions.
        self.name = ""
        # Boolean when layer has a mask. Will be deprecated in favor of checking masksProperties.
        self.has_masks = 0
        # List of Masks
        self.masks_properties = [] # Mask
        # List of Effects
        self.effects = [] # IndexEffect
        # Layer Time Stretching
        self.stretch = 1
        # Layer Parent. Uses ind of parent.
        self.parent = None
        # Shape list of items
        self.items = [] # Shape, Rect, Ellipse, Star, Fill, GFill, GStroke, Stroke, Merge, Trim, Group, RoundedCorners, Repeater
        self.markers = []


class ImageLayer(TgsObject):
    _props = {
        "type": "ty",
        "transform": "ks",
        "auto_orient": "ao",
        "blend_mode": "bm",
        "threedimensional": "ddd",
        "index": "ind",
        "css_class": "cl",
        "layer_html_id": "ln",
        "in_point": "ip",
        "out_point": "op",
        "start_time": "st",
        "name": "nm",
        "has_masks": "hasMask",
        "masks_properties": "masksProperties",
        "effects": "ef",
        "stretch": "sr",
        "parent": "parent",
        "reference_id": "refId",
    }

    def __init__(self):
        # Type of layer: Image.
        self.type = 2
        # Transform properties
        self.transform = Transform()
        # Auto-Orient along path AE property.
        self.auto_orient = False
        # Blend Mode
        self.blend_mode = BlendMode.default()
        # 3d layer flag
        self.threedimensional = False
        # Layer index in AE. Used for parenting and expressions.
        self.index = 0
        # Parsed layer name used as html class on SVG/HTML renderer
        self.css_class = ""
        # Parsed layer name used as html id on SVG/HTML renderer
        self.layer_html_id = ""
        # In Point of layer. Sets the initial frame of the layer.
        self.in_point = 0
        # Out Point of layer. Sets the final frame of the layer.
        self.out_point = 0
        # Start Time of layer. Sets the start time of the layer.
        self.start_time = 0
        # After Effects Layer Name. Used for expressions.
        self.name = 0
        # Boolean when layer has a mask. Will be deprecated in favor of checking masksProperties.
        self.has_masks = 0
        # List of Masks
        self.masks_properties = [] # Mask
        # List of Effects
        self.effects = [] # IndexEffect
        # Layer Time Stretching
        self.stretch = 0
        # Layer Parent. Uses ind of parent.
        self.parent = None
        # id pointing to the source image defined on 'assets' object
        self.reference_id = ""


class PreCompLayer(TgsObject):
    _props = {
        "type": "ty",
        "transform": "ks",
        "auto_orient": "ao",
        "blend_mode": "bm",
        "threedimensional": "ddd",
        "index": "ind",
        "css_class": "cl",
        "layer_html_id": "ln",
        "in_point": "ip",
        "out_point": "op",
        "start_time": "st",
        "name": "nm",
        "has_masks": "hasMask",
        "masks_properties": "masksProperties",
        "effects": "ef",
        "stretch": "sr",
        "parent": "parent",
        "reference_id": "refId",
        "time_remapping": "tm",
    }

    def __init__(self):
        # Type of layer: Precomp.
        self.type = 0
        # Transform properties
        self.transform = Transform()
        # Auto-Orient along path AE property.
        self.auto_orient = False
        # Blend Mode
        self.blend_mode = BlendMode.default()
        # 3d layer flag
        self.threedimensional = False
        # Layer index in AE. Used for parenting and expressions.
        self.index = 0
        # Parsed layer name used as html class on SVG/HTML renderer
        self.css_class = ""
        # Parsed layer name used as html id on SVG/HTML renderer
        self.layer_html_id = ""
        # In Point of layer. Sets the initial frame of the layer.
        self.in_point = 0
        # Out Point of layer. Sets the final frame of the layer.
        self.out_point = 0
        # Start Time of layer. Sets the start time of the layer.
        self.start_time = 0
        # After Effects Layer Name. Used for expressions.
        self.name = 0
        # Boolean when layer has a mask. Will be deprecated in favor of checking masksProperties.
        self.has_masks = 0
        # List of Masks
        self.masks_properties = [] # Mask
        # List of Effects
        self.effects = [] # IndexEffect
        # Layer Time Stretching
        self.stretch = 0
        # Layer Parent. Uses ind of parent.
        self.parent = None
        # id pointing to the source composition defined on 'assets' object
        self.reference_id = ""
        # Comp's Time remapping
        self.time_remapping = ValueKeyframed.default()


class SolidLayer(TgsObject):
    _props = {
        "type": "ty",
        "transform": "ks",
        "auto_orient": "ao",
        "blend_mode": "bm",
        "threedimensional": "ddd",
        "index": "ind",
        "css_class": "cl",
        "layer_html_id": "ln",
        "in_point": "ip",
        "out_point": "op",
        "start_time": "st",
        "name": "nm",
        "has_masks": "hasMask",
        "masks_properties": "masksProperties",
        "effects": "ef",
        "stretch": "sr",
        "parent": "parent",
        "solid_color": "sc",
        "solid_height": "sh",
        "solid_width": "sw",
    }

    def __init__(self):
        # Type of layer: Solid.
        self.type = 0
        # Transform properties
        self.transform = Transform()
        # Auto-Orient along path AE property.
        self.auto_orient = False
        # Blend Mode
        self.blend_mode = BlendMode.default()
        # 3d layer flag
        self.threedimensional = False
        # Layer index in AE. Used for parenting and expressions.
        self.index = 0
        # Parsed layer name used as html class on SVG/HTML renderer
        self.css_class = ""
        # Parsed layer name used as html id on SVG/HTML renderer
        self.layer_html_id = ""
        # In Point of layer. Sets the initial frame of the layer.
        self.in_point = 0
        # Out Point of layer. Sets the final frame of the layer.
        self.out_point = 0
        # Start Time of layer. Sets the start time of the layer.
        self.start_time = 0
        # After Effects Layer Name. Used for expressions.
        self.name = 0
        # Boolean when layer has a mask. Will be deprecated in favor of checking masksProperties.
        self.has_masks = 0
        # List of Masks
        self.masks_properties = [] # Mask
        # Auto-Orient along path AE property.
        self.effects = False
        # Layer Time Stretching
        self.stretch = 0
        # Layer Parent. Uses ind of parent.
        self.parent = None
        # Color of the solid in hex
        self.solid_color = ""
        # Height of the solid.
        self.solid_height = 0
        # Width of the solid.
        self.solid_width = 0


class LineJoin(TgsEnum):
    Miter = 1
    Round = 2
    Bevel = 3

    @classmethod
    def default(cls):
        return cls.Round


class TestBased(TgsEnum):
    Characters = 1
    CharacterExcludingSpaces = 2
    Words = 3
    Lines = 4

    @classmethod
    def default(cls):
        return cls.Characters


class Composite(TgsEnum):
    Above = 1
    Below = 2

    @classmethod
    def default(cls):
        return cls.Above


class Transform(TgsObject):
    _props = {
        "anchor_point": "a",
        "position": "p",
        "scale": "s",
        "rotation": "r",
        "opacity": "o",
        #"position_x": "px",
        #"position_y": "py",
        #"position_z": "pz",
        #"skew": "sk",
        #"skew_axis": "sa",
    }

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
        self.position_x = Value(0) # Value, ValueKeyframed
        # Transform Position Y
        self.position_y = Value(0) # Value, ValueKeyframed
        # Transform Position Z
        self.position_z = Value(0) # Value, ValueKeyframed
        # Transform Skew
        self.skew = Value(0) # Value, ValueKeyframed
        # Transform Skew Axis
        self.skew_axis = Value(0) # Value, ValueKeyframed


class Mask(TgsObject):
    _props = {
        "inverted": "inv",
        "name": "nm",
        "points": "pt",
        "opacity": "o",
        "mode": "mode",
    }

    def __init__(self):
        # Inverted Mask flag
        self.inverted = None
        # Mask name. Used for expressions and effects.
        self.name = ""
        # Mask vertices
        self.points = Shape() # Shape, ShapeKeyframed
        # Mask opacity.
        self.opacity = Const() # Const, ConstKeyframed
        # Mask mode. Not all mask types are supported.
        self.mode = ""


class TextShape(TgsEnum):
    Square = 1
    RampUp = 2
    RampDown = 3
    Triangle = 4
    Round = 5
    Smooth = 6

    @classmethod
    def default(cls):
        return cls.Square


class LineCap(TgsEnum):
    Butt = 1
    Round = 2
    Square = 3

    @classmethod
    def default(cls):
        return cls.Round


class TextGrouping(TgsEnum):
    Characters = 1
    Word = 2
    Line = 3
    All = 4

    @classmethod
    def default(cls):
        return cls.Characters


class BlendMode(TgsEnum):
    Normal = 0
    Multiply = 1
    Screen = 2
    Overlay = 3
    Darken = 4
    Lighten = 5
    ColorDodge = 6
    ColorBurn = 7
    HardLight = 8
    SoftLight = 9
    Difference = 10
    Exclusion = 11
    Hue = 12
    Saturation = 13
    Color = 14
    Luminosity = 15

    @classmethod
    def default(cls):
        return cls.Normal
