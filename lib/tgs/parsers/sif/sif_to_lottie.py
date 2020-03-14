from ... import objects
from . import api
from ... import NVector


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
        else:
            return

        parent.add_shape(shape)

    def _convert_group(self, layer: api.GroupLayer):
        shape = objects.Group()
        shape.transform.anchor_point.value = shape.transform.position.value = self.target_size / 2
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
        #if layer.regular_polygon:
            #shape.star_type = objects.StarType.Polygon
        return shape

    def _mix_animations(self, v1: objects.properties.AnimatableMixin, v2: objects.properties.AnimatableMixin):
        self._force_animated(v1)
        self._force_animated(v2)
        times = set()
        for kf in v1.keyframes + v2.keyframes:
            times.add(kf.time)

        for time in sorted(times):
            yield time, v1.get_value(time), v2.get_value(time)

    def _force_animated(self, lottieval):
        if not lottieval:
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
        return self._adjust_animated(lottieval, lambda x: x*60)

    def _adjust_coords(self, lottieval: objects.MultiDimensional):
        return self._adjust_animated(lottieval, self._coord)

    def _coord(self, val: NVector):
        return NVector(
            self.target_size.x * (val.x / (self.view_p2.x - self.view_p1.x) + 0.5),
            self.target_size.y * (val.y / (self.view_p2.y - self.view_p1.y) + 0.5),
        )
