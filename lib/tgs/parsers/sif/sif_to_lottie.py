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
        for layer in canvas.layers:
            self._convert_layer(layer, self.shape_layer)
        return self.animation

    def _time(self, t: api.FrameTime):
        return self.canvas.time_to_frames(t)

    def _convert_layer(self, layer: api.Layer, parent):
        if isinstance(layer, api.GroupLayer):
            shape = objects.Group()
            for sub in layer.canvas:
                self._convert_layer(sub, shape)
        elif isinstance(layer, api.RectangleLayer):
            rect = objects.Rect()
            p1 = self._adjust_coords(self._convert_vector(layer.point1))
            p2 = self._adjust_coords(self._convert_vector(layer.point2))
            if p1.animated or p2.animated:
                # TODO
                pass
            else:
                rect.position.value = (p1.value + p2.value) / 2
                rect.size.value = abs(p2.value - p1.value)
            rect.rounded = self._convert_scalar(layer.bevel)
            shape = objects.Group()
            shape.add_shape(rect)
            fill = objects.Fill()
            fill.color = self._convert_vector(layer.color)
            shape.add_shape(fill)
        else:
            return

        parent.add_shape(shape)

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

    def _adjust_coords(self, lottieval: objects.MultiDimensional):
        if lottieval.animated:
            for kf in lottieval.keyframes:
                if kf.start is not None:
                    kf.start = self._coord(kf.start)
                if kf.end is not None:
                    kf.end = self._coord(kf.end)
        else:
            lottieval.value = self._coord(lottieval.value)
        return lottieval

    def _coord(self, val: NVector):
        return NVector(
            self.target_size.x * (val.x / (self.view_p2.x - self.view_p1.x) + 0.5),
            self.target_size.y * (val.y / (self.view_p2.y - self.view_p1.y) + 0.5),
        )

