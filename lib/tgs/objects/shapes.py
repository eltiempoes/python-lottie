import math
from .base import TgsObject, TgsProp, TgsEnum, todo_func, NVector
from .properties import Value, MultiDimensional, GradientColors, ShapeProperty, Bezier
from .helpers import Transform
from ..utils.ellipse import Ellipse as EllipseConverter


class BoundingBox:
    """!
    Shape bounding box
    """
    def __init__(self, x1=None, y1=None, x2=None, y2=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def include(self, x, y):
        """!
        Expands the box to include the point at x, y
        """
        if x is not None:
            if self.x1 is None or self.x1 > x:
                self.x1 = x
            if self.x2 is None or self.x2 < x:
                self.x2 = x
        if y is not None:
            if self.y1 is None or self.y1 > y:
                self.y1 = y
            if self.y2 is None or self.y2 < y:
                self.y2 = y

    def expand(self, other):
        """!
        Expands the bounding box to include another bounding box
        """
        self.include(other.x1, other.y1)
        self.include(other.x2, other.y2)

    def center(self):
        """!
        Center point of the bounding box
        """
        return NVector((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)

    def isnull(self):
        """!
        Whether the box is default-initialized
        """
        return self.x1 is None or self.y2 is None

    def __repr__(self):
        return "<BoundingBox [%s, %s] - [%s, %s]>" % (self.x1, self.y1, self.x2, self.y2)

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1


def load_shape_element(lottiedict):
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


##\ingroup Lottie
class ShapeElement(TgsObject):
    """!
    Base class for all elements of ShapeLayer and Group
    """
    def bounding_box(self, time=0):
        """!
        Bounding box of the shape element at the given time
        """
        return BoundingBox()


##\ingroup Lottie
class Rect(ShapeElement):
    """!
    A simple rectangle shape
    """
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("direction", "d", float, False),
        TgsProp("type", "ty", str, False),
        TgsProp("position", "p", MultiDimensional, False),
        TgsProp("size", "s", MultiDimensional, False),
        TgsProp("rounded", "r", Value, False),
    ]

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""

        ## After Effect's Name. Used for expressions.
        self.name = None
        ## After Effect's Direction. Direction how the shape is drawn. Used for trim path for example.
        self.direction = 0
        ## %Shape type.
        self.type = 'rc'
        ## Rect's position
        self.position = MultiDimensional(NVector(0, 0))
        ## Rect's size
        self.size = MultiDimensional(NVector(0, 0))
        ## Rect's rounded corners
        self.rounded = Value()

    def bounding_box(self, time=0):
        pos = self.position.get_value(time)
        sz = self.size.get_value(time)

        return BoundingBox(
            pos[0] - sz[0]/2,
            pos[1] - sz[1]/2,
            pos[0] + sz[0]/2,
            pos[1] + sz[1]/2,
        )

    def to_bezier(self):
        """!
        Returns a Shape corresponding to this rect
        """
        shape = Shape()
        kft = set()
        if self.position.animated:
            kft |= set(kf.time for kf in self.position.keyframes)
        if self.size.animated:
            kft |= set(kf.time for kf in self.size.keyframes)
        if self.rounded.animated:
            kft |= set(kf.time for kf in self.rounded.keyframes)
        if not kft:
            shape.vertices.value = self._bezier_t(0)
        else:
            for time in sorted(kft):
                shape.vertices.add_keyframe(time, self._bezier_t(time))
        return shape

    def _bezier_t(self, time):
        bezier = Bezier()
        bb = self.bounding_box(time)
        rounded = self.rounded.get_value(time)
        tl = NVector(bb.x1, bb.y1)
        tr = NVector(bb.x2, bb.y1)
        br = NVector(bb.x2, bb.y2)
        bl = NVector(bb.x1, bb.y2)

        if not self.rounded.animated and rounded == 0:
            bezier.add_point(tl)
            bezier.add_point(tr)
            bezier.add_point(br)
            bezier.add_point(bl)
        else:
            hh = NVector(rounded/2, 0)
            vh = NVector(0, rounded/2)
            hd = NVector(rounded, 0)
            vd = NVector(0, rounded)
            bezier.add_point(tl+vd, outp=-vh)
            bezier.add_point(tl+hd, -hh)
            bezier.add_point(tr-hd, outp=hh)
            bezier.add_point(tr+vd, -vh)
            bezier.add_point(br-vd, outp=vh)
            bezier.add_point(br-hd, hh)
            bezier.add_point(bl+hd, outp=-hh)
            bezier.add_point(bl-vd, vh)

        bezier.close()
        return bezier


##\ingroup Lottie
class StarType(TgsEnum):
    Star = 1
    Polygon = 2


##\ingroup Lottie
class Star(ShapeElement):
    """!
    Star shape
    """
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

        ## After Effect's Name. Used for expressions.
        self.name = None
        ## After Effect's Direction. Direction how the shape is drawn. Used for trim path for example.
        self.direction = 0
        ## %Shape type.
        self.type = 'sr'
        ## Star's position
        self.position = MultiDimensional(NVector(0, 0))
        ## Star's inner radius. (Star only)
        self.inner_radius = Value()
        ## Star's inner roundness. (Star only)
        self.inner_roundness = Value()
        ## Star's outer radius.
        self.outer_radius = Value()
        ## Star's outer roundness.
        self.outer_roundness = Value()
        ## Star's rotation.
        self.rotation = Value()
        ## Star's number of points.
        self.points = Value(5)
        ## Star's type. Polygon or Star.
        self.star_type = StarType.Star

    def bounding_box(self, time=0):
        pos = self.position.get_value(time)
        r = self.outer_radius.get_value(time)

        return BoundingBox(
            pos[0] - r,
            pos[1] - r,
            pos[0] + r,
            pos[1] + r,
        )

    def to_bezier(self):
        """!
        Returns a Shape corresponding to this star
        """
        shape = Shape()
        kft = set()
        if self.position.animated:
            kft |= set(kf.time for kf in self.position.keyframes)
        if self.inner_radius.animated:
            kft |= set(kf.time for kf in self.inner_radius.keyframes)
        if self.inner_roundness.animated:
            kft |= set(kf.time for kf in self.inner_roundness.keyframes)
        if self.points.animated:
            kft |= set(kf.time for kf in self.points.keyframes)
        if self.rotation.animated:
            kft |= set(kf.time for kf in self.rotation.keyframes)
        # TODO inner_roundness / outer_roundness
        if not kft:
            shape.vertices.value = self._bezier_t(0)
        else:
            for time in sorted(kft):
                shape.vertices.add_keyframe(time, self._bezier_t(time))
        return shape

    def _bezier_t(self, time):
        bezier = Bezier()
        pos = self.position.get_value(time)
        r1 = self.inner_radius.get_value(time)
        r2 = self.outer_radius.get_value(time)
        rot = (self.rotation.get_value(time)) * math.pi / 180
        p = self.points.get_value(time)
        halfd = math.pi / p

        for i in range(p):
            main_angle = rot + i * halfd * 2
            dx = r2 * math.sin(main_angle)
            dy = r2 * math.cos(main_angle)
            bezier.add_point(NVector(pos.x + dx, pos.y + dy))

            if self.star_type == StarType.Star:
                dx = r1 * math.sin(main_angle+halfd)
                dy = r1 * math.cos(main_angle+halfd)
                bezier.add_point(NVector(pos.x + dx, pos.y + dy))

        bezier.close()
        return bezier


##\ingroup Lottie
class Ellipse(ShapeElement):
    """!
    Ellipse shape
    """
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

        ## After Effect's Name. Used for expressions.
        self.name = None
        ## After Effect's Direction. Direction how the shape is drawn. Used for trim path for example.
        self.direction = 0
        ## %Shape type.
        self.type = 'el'
        ## Ellipse's position
        self.position = MultiDimensional(NVector(0, 0))
        ## Ellipse's size
        self.size = MultiDimensional(NVector(0, 0))

    def bounding_box(self, time=0):
        pos = self.position.get_value(time)
        sz = self.size.get_value(time)

        return BoundingBox(
            pos[0] - sz[0]/2,
            pos[1] - sz[1]/2,
            pos[0] + sz[0]/2,
            pos[1] + sz[1]/2,
        )

    def to_bezier(self):
        """!
        Returns a Shape corresponding to this ellipse
        """
        shape = Shape()
        kft = set()
        if self.position.animated:
            kft |= set(kf.time for kf in self.position.keyframes)
        if self.size.animated:
            kft |= set(kf.time for kf in self.size.keyframes)
        if not kft:
            shape.vertices.value = self._bezier_t(0)
        else:
            for time in sorted(kft):
                shape.vertices.add_keyframe(time, self._bezier_t(time))
        return shape

    def _bezier_t(self, time):
        bezier = Bezier()
        position = self.position.get_value(time)
        radii = self.size.get_value(time) / 2

        el = EllipseConverter(position, radii, 0)
        points = el.to_bezier(0, math.pi*2)
        for point in points[1:]:
            bezier.add_point(point.point, point.in_t, point.out_t)

        bezier.close()
        return bezier


##\ingroup Lottie
class Shape(ShapeElement):
    """!
    Animatable Bezier curve
    """
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

        ## After Effect's Name. Used for expressions.
        self.name = None
        ## After Effect's Direction. Direction how the shape is drawn. Used for trim path for example.
        self.direction = 0
        ## %Shape type.
        self.type = 'sh'
        ## Shape's vertices
        self.vertices = ShapeProperty()

    def bounding_box(self, time=0):
        pos = self.vertices.get_value(time)

        bb = BoundingBox()
        for v in pos.vertices:
            bb.include(*v)

        return bb

    def to_bezier(self):
        return self


##\ingroup Lottie
class Group(ShapeElement):
    """!
    ShapeElement that can contain other shapes
    \note Shapes inside the same group will create "holes" in other shapes
    """
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("number_of_properties", "np", float, False),
        TgsProp("shapes", "it", load_shape_element, True),
        TgsProp("property_index", "ix", int, False),
    ]

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = None
        ## %Shape type.
        self.type = 'gr'
        ## Group number of properties. Used for expressions.
        self.number_of_properties = None
        ## Group list of items
        self.shapes = [TransformShape()]
        self.property_index = None

    def add_shape(self, shape):
        self.shapes.insert(-1, shape)
        return shape

    def insert_shape(self, index, shape):
        self.shapes.insert(index, shape)
        return shape

    @property
    def transform(self):
        return self.shapes[-1]

    def bounding_box(self, time=0):
        bb = BoundingBox()
        for v in self.shapes:
            bb.expand(v.bounding_box(time))

        return bb

    def find_all(self, type=ShapeElement, predicate=None, recursive=True):
        """!
        Returns all the child shapes matching a predicate
        """
        results = []
        for e in self.shapes:
            include = isinstance(e, type)
            if predicate and include:
                include = predicate(e)
            if include:
                results.append(e)
            if recursive and isinstance(e, Group):
                results += e.find_all(type, predicate, recursive)
        return results


##\ingroup Lottie
class Fill(ShapeElement):
    """!
    Solid fill color
    """
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("opacity", "o", Value, False),
        TgsProp("color", "c", MultiDimensional, False),
    ]

    def __init__(self, color=None):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = None
        ## %Shape type.
        self.type = 'fl'
        ## Fill Opacity
        self.opacity = Value(100)
        ## Fill Color
        self.color = MultiDimensional(color or NVector(1, 1, 1))


##\ingroup Lottie
class GradientType(TgsEnum):
    Linear = 1
    Radial = 2


##\ingroup Lottie
class GradientFill(ShapeElement):
    """!
    Gradient fill
    """
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
        #r int
        #bm int
    ]

    def __init__(self, colors=[]):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = None
        ## %Shape type.
        self.type = 'gf'
        ## Fill Opacity
        self.opacity = Value(100)
        ## Gradient Start Point
        self.start_point = MultiDimensional(NVector(0, 0))
        ## Gradient End Point
        self.end_point = MultiDimensional(NVector(0, 0))
        ## Gradient Type
        self.gradient_type = GradientType.Linear
        ## Gradient Highlight Length. Only if type is Radial
        self.highlight_length = Value()
        ## Highlight Angle. Only if type is Radial
        self.highlight_angle = Value()
        ## Gradient Colors
        self.colors = GradientColors(colors)


##\ingroup Lottie
class LineJoin(TgsEnum):
    Miter = 1
    Round = 2
    Bevel = 3


##\ingroup Lottie
class LineCap(TgsEnum):
    Butt = 1
    Round = 2
    Square = 3


##\ingroup Lottie
class Stroke(ShapeElement):
    """!
    Solid stroke
    """
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("line_cap", "lc", LineCap, False),
        TgsProp("line_join", "lj", LineJoin, False),
        TgsProp("miter_limit", "ml", float, False),
        TgsProp("opacity", "o", Value, False),
        TgsProp("width", "w", Value, False),
        TgsProp("color", "c", MultiDimensional, False),
    ]

    def __init__(self, color=None, width=1):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = None
        ## %Shape type.
        self.type = 'st'
        ## Stroke Line Cap
        self.line_cap = LineCap.Round
        ## Stroke Line Join
        self.line_join = LineJoin.Round
        ## Stroke Miter Limit. Only if Line Join is set to Miter.
        self.miter_limit = 0
        ## Stroke Opacity
        self.opacity = Value(100)
        ## Stroke Width
        self.width = Value(width)
        ## Stroke Color
        self.color = MultiDimensional(color or NVector(0, 0, 0))


##\ingroup Lottie
class GradientStroke(ShapeElement):
    """!
    Gradient stroke
    \todo move the common bit together with Stroke to minimize duplication
    """
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
        TgsProp("width", "w", Value, False),
        TgsProp("line_cap", "lc", LineCap, False),
        TgsProp("line_join", "lj", LineJoin, False),
        TgsProp("miter_limit", "ml", float, False),
    ]

    def __init__(self, stroke_width=1):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = None
        ## %Shape type.
        self.type = 'gs'
        ## Stroke Opacity
        self.opacity = Value(100)
        ## Gradient Start Point
        self.start_point = MultiDimensional(NVector(0, 0))
        ## Gradient End Point
        self.end_point = MultiDimensional(NVector(0, 0))
        ## Gradient Type
        self.gradient_type = GradientType.Linear
        ## Gradient Highlight Length. Only if type is Radial
        self.highlight_length = Value()
        ## Highlight Angle. Only if type is Radial
        self.highlight_angle = Value()
        ## Gradient Colors
        self.colors = GradientColors()
        ## Gradient Stroke Width
        self.width = Value(stroke_width)
        ## Gradient Stroke Line Cap
        self.line_cap = LineCap.Round
        ## Gradient Stroke Line Join
        self.line_join = LineJoin.Round
        ## Gradient Stroke Miter Limit. Only if Line Join is set to Miter.
        self.miter_limit = 0

    def bounding_box(self, time=0):
        return BoundingBox()


##\ingroup Lottie
class TransformShape(ShapeElement):
    """!
    Group transform
    \todo Inherit from Transform
    """
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
        ## After Effect's Name. Used for expressions.
        self.name = None
        ## %Shape type.
        self.type = 'tr'
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
        ## Transform Skew
        self.skew = Value(0)
        ## Transform Skew Axis
        self.skew_axis = Value(0)


##\ingroup Lottie
## \todo check
class Trim(ShapeElement):
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
        ## After Effect's Name. Used for expressions.
        self.name = None
        ## %Shape type.
        self.type = 'tm'
        ## Trim Start.
        self.start = Value()
        ## Trim End.
        self.end = Value()
        ## Trim Offset.
        self.offset = Value()


##\ingroup Lottie
class Composite(TgsEnum):
    Above = 1
    Below = 2


##\ingroup Lottie
## \todo check
class Repeater(ShapeElement):
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
        ## After Effect's Name. Used for expressions.
        self.name = None
        ## %Shape type.
        self.type = 'rp'
        ## Number of Copies
        self.copies = Value()
        ## Offset of Copies
        self.offset = Value()
        ## Composite of copies
        self.composite = Composite.Above
        ## Transform values for each repeater copy
        self.transform = Transform()


##\ingroup Lottie
## \todo check
class Round(ShapeElement):
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("radius", "r", Value, False),
    ]

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = None
        ## %Shape type.
        self.type = 'rd'
        ## Rounded Corner Radius
        self.radius = Value()


##\ingroup Lottie
## \todo check
class Merge(ShapeElement):
    _props = [
        #TgsProp("match_name", "mn", str, False),
        TgsProp("name", "nm", str, False),
        TgsProp("type", "ty", str, False),
        TgsProp("merge_mode", "mm", float, False),
    ]

    def __init__(self):
        # After Effect's Match Name. Used for expressions.
        #self.match_name = ""
        ## After Effect's Name. Used for expressions.
        self.name = None
        ## %Shape type. THIS FEATURE IS NOT SUPPORTED. It's exported because if you export it, they will come.
        self.type = 'mm'
        ## Merge Mode
        self.merge_mode = 1
