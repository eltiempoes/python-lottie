import math
from ... import objects
from . import api
from ... import NVector, PolarVector


def convert(canvas: api.Canvas):
    return Converter().convert(canvas)


class Converter:
    def __init__(self):
        pass

    def convert(self, canvas: api.Canvas):
        self.canvas = canvas
        self.animation = objects.Animation(
            self._time(canvas.end_time),
            canvas.fps
        )
        self.animation.in_point = self._time(canvas.begin_time)
        self.animation.width = canvas.width
        self.animation.height = canvas.height
        self.view_p1 = NVector(canvas.view_box[0], canvas.view_box[1])
        self.view_p2 = NVector(canvas.view_box[2], canvas.view_box[3])
        self.target_size = NVector(canvas.width, canvas.height)
        self.shape_layer = self.animation.add_layer(objects.ShapeLayer())
        for layer in reversed(canvas.layers):
            self._convert_layer(layer, self.shape_layer)
        return self.animation

    def _time(self, t: api.FrameTime):
        return self.canvas.time_to_frames(t)

    def _convert_layer(self, layer: api.Layer, parent):
        if isinstance(layer, api.GroupLayer):
            shape = self._convert_group(layer)
        elif isinstance(layer, api.RectangleLayer):
            shape = self._convert_fill(layer, self._convert_rect)
        elif isinstance(layer, api.CircleLayer):
            shape = self._convert_fill(layer, self._convert_circle)
        elif isinstance(layer, api.StarLayer):
            shape = self._convert_fill(layer, self._convert_star)
        elif isinstance(layer, api.PolygonLayer):
            shape = self._convert_fill(layer, self._convert_polygon)
        elif isinstance(layer, api.RegionLayer):
            shape = self._convert_fill(layer, self._convert_bline)
        elif isinstance(layer, api.AbstractOutline):
            shape = self._convert_outline(layer, self._convert_bline)
        else:
            return

        parent.add_shape(shape)

    def _convert_group(self, layer: api.GroupLayer):
        shape = objects.Group()
        shape.transform.anchor_point = self._adjust_coords(self._convert_vector(layer.origin))
        shape.transform.position = self._adjust_coords(self._convert_vector(layer.transformation.offset))
        shape.transform.rotation = self._adjust_animated(
            self._convert_scalar(layer.transformation.angle),
            lambda x: -x
        )
        shape.transform.scale = self._adjust_animated(
            self._convert_vector(layer.transformation.scale),
            lambda x: x * 100
        )
        shape.transform.skew_axis = self._adjust_animated(
            self._convert_scalar(layer.transformation.skew_angle),
            lambda x: -x
        )
        for sub in reversed(layer.canvas):
            self._convert_layer(sub, shape)
        return shape

    def _convert_fill(self, layer, converter):
        shape = objects.Group()
        shape.add_shape(converter(layer))
        fill = objects.Fill()
        fill.color = self._convert_vector(layer.color)
        shape.add_shape(fill)
        return shape

    def _convert_linecap(self, lc: api.LineCap):
        if lc == api.LineCap.Rounded:
            return objects.LineCap.Round
        if lc == api.LineCap.Squared:
            return objects.LineCap.Square
        return objects.LineCap.Butt

    def _convert_cusp(self, lc: api.CuspStyle):
        if lc == api.CuspStyle.Miter:
            return objects.LineJoin.Miter
        if lc == api.CuspStyle.Bevel:
            return objects.LineJoin.Bevel
        return objects.LineJoin.Round

    def _convert_outline(self, layer: api.AbstractOutline, converter):
        shape = objects.Group()
        shape.add_shape(converter(layer))
        stroke = objects.Stroke()
        stroke.color = self._convert_vector(layer.color)
        stroke.line_cap = self._convert_linecap(layer.start_tip)
        stroke.line_join = self._convert_cusp(layer.cusp_type)
        stroke.width = self._adjust_scalar(self._convert_scalar(layer.width))
        shape.add_shape(stroke)
        return shape

    def _convert_rect(self, layer: api.RectangleLayer):
        rect = objects.Rect()
        p1 = self._adjust_coords(self._convert_vector(layer.point1))
        p2 = self._adjust_coords(self._convert_vector(layer.point2))
        if p1.animated or p2.animated:
            for time, p1v, p2v in self._mix_animations(p1, p2):
                rect.position.add_keyframe(time, (p1v + p2v) / 2)
                rect.size.add_keyframe(time, abs(p2v - p1v))
            pass
        else:
            rect.position.value = (p1.value + p2.value) / 2
            rect.size.value = abs(p2.value - p1.value)
        rect.rounded = self._adjust_scalar(self._convert_scalar(layer.bevel))
        return rect

    def _convert_circle(self, layer: api.CircleLayer):
        shape = objects.Ellipse()
        shape.position = self._adjust_coords(self._convert_vector(layer.origin))
        radius = self._adjust_scalar(self._convert_scalar(layer.radius))
        if radius.animated:
            for kf in radius.keyframes:
                shape.size.add_keyframe(kf.time, NVector(kf.start, kf.start) * 2)
                shape.size.keyframes[-1].in_value = kf.in_value
                shape.size.keyframes[-1].out_value = kf.out_value
        else:
            shape.size.value = NVector(radius.value, radius.value) * 2
        return shape

    def _convert_star(self, layer: api.StarLayer):
        shape = objects.Star()
        shape.position = self._adjust_coords(self._convert_vector(layer.origin))
        shape.inner_radius = self._adjust_scalar(self._convert_scalar(layer.radius2))
        shape.outer_radius = self._adjust_scalar(self._convert_scalar(layer.radius1))
        shape.rotation = self._adjust_animated(
            self._convert_scalar(layer.angle),
            lambda x: 90-x
        )
        shape.points = self._convert_scalar(layer.points)
        if layer.regular_polygon:
            shape.star_type = objects.StarType.Polygon
        return shape

    def _mix_animations(self, *animatable):
        times = set()
        for v in animatable:
            self._force_animated(v)
            for kf in v.keyframes:
                times.add(kf.time)

        for time in sorted(times):
            yield [time] + [v.get_value(time) for v in animatable]

    def _force_animated(self, lottieval):
        if not lottieval.animated:
            v = lottieval.value
            lottieval.add_keyframe(0, v)
            lottieval.add_keyframe(self.animation.out_point, v)

    def _convert_animatable(self, v: api.SifAnimatable, lot: objects.properties.AnimatableMixin):
        if v.animated:
            for kf in v.keyframes:
                # TODO easing
                lot.add_keyframe(self._time(kf.time), kf.value)
        else:
            lot.value = v.value
        return lot

    def _convert_vector(self, v: api.SifAnimatable):
        return self._convert_animatable(v, objects.MultiDimensional())

    def _convert_scalar(self, v: api.SifAnimatable):
        return self._convert_animatable(v, objects.Value())

    def _adjust_animated(self, lottieval, transform):
        if lottieval.animated:
            for kf in lottieval.keyframes:
                if kf.start is not None:
                    kf.start = transform(kf.start)
                if kf.end is not None:
                    kf.end = transform(kf.end)
        else:
            lottieval.value = transform(lottieval.value)
        return lottieval

    def _adjust_scalar(self, lottieval: objects.Value):
        return self._adjust_animated(lottieval, self._scalar_mult)

    def _scalar_mult(self, x):
        return x * 60

    def _adjust_coords(self, lottieval: objects.MultiDimensional):
        return self._adjust_animated(lottieval, self._coord)

    def _coord(self, val: NVector):
        return NVector(
            self.target_size.x * (val.x / (self.view_p2.x - self.view_p1.x) + 0.5),
            self.target_size.y * (val.y / (self.view_p2.y - self.view_p1.y) + 0.5),
        )

    def _convert_polygon(self, layer: api.PolygonLayer):
        lot = objects.Path()
        animatables = [self._convert_vector(layer.origin)] + [
            self._convert_vector(p)
            for p in layer.points
        ]
        animated = any(x.animated for x in animatables)
        if not animated:
            lot.shape.value = self._polygon([x.value for x in animatables[1:]], animatables[0].value)
        else:
            for values in self._mix_animations(*animatables):
                time = values[0]
                origin = values[1]
                points = values[2:]
                lot.shape.add_keyframe(time, self._polygon(points, origin))
        return lot

    def _polygon(self, points, origin):
        chunk_size = 5
        bezier = objects.Bezier()
        bezier.closed = True
        for point in points:
            bezier.add_point(self._coord(point+origin))
        return bezier

    def _convert_bline(self, layer: api.AbstractOutline):
        lot = objects.Path()
        closed = layer.bline.loop
        animatables = [
            self._convert_vector(layer.origin)
        ]
        for p in layer.bline.points:
            animatables += [
                self._convert_vector(p.point),
                self._convert_scalar(p.t1.radius),
                self._convert_scalar(p.t1.theta),
                self._convert_scalar(p.t2.radius),
                self._convert_scalar(p.t2.theta)
            ]
        animated = any(x.animated for x in animatables)
        if not animated:
            lot.shape.value = self._bezier(closed, [x.value for x in animatables[1:]], animatables[0].value)
        else:
            for values in self._mix_animations(*animatables):
                time = values[0]
                origin = values[1]
                values = values[2:]
                lot.shape.add_keyframe(time, self._bezier(closed, values, origin))
        return lot

    def _bezier(self, closed, values, origin):
        chunk_size = 5
        bezier = objects.Bezier()
        bezier.closed = closed
        for i in range(0, len(values), chunk_size):
            point, r1, a1, r2, a2 = values[i:i+chunk_size]
            bezier.add_point(self._coord(point+origin), self._polar(r1, a1, 1), self._polar(r2, a2, 2))
        return bezier

    def _polar(self, radius, angle, dir):
        offset_angle = 0
        if dir == 1:
            offset_angle += 180
        return PolarVector(radius*20, (-angle+offset_angle) * math.pi / 180)
