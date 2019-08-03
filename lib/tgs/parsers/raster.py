# NOTE: requires pillow, pypotrace>=0.2, numpy, scipy to be installed
from PIL import Image
import potrace
import numpy
import enum
from scipy.cluster.vq import kmeans
from .. import objects
from ..nvector import NVector


class QuanzationMode(enum.Enum):
    Nearest = 1
    Exact = 2


class RasterImage:
    def __init__(self, data):
        self.data = data

    @classmethod
    def from_pil(cls, image):
        return cls(numpy.array(image))

    @classmethod
    def open(cls, filename):
        return cls.from_pil(Image.open(filename))

    def k_means(self, n_colors):
        """!
        Returns a list of centroids
        """
        colors = []
        for row in range(self.data.shape[0]):
            for column in range(self.data.shape[1]):
                if self.get_alpha(row, column) == 255:
                    colors.append(self.data[row][column])

        colors = numpy.array(colors, numpy.float)
        return kmeans(colors, n_colors+1)[0]

    def get_alpha(self, row, column):
        if self.data.shape[2] >= 4:
            return self.data[row][column][3]
        return 255

    def quantize(self, codebook, quantization_mode=QuanzationMode.Nearest):
        """!
        Returns a list of tuple [color, data] where for each color in codebook
        data is a bit mask for the image

        You can get codebook from k_means
        """
        if codebook is None or len(codebook) == 0:
            return [(numpy.array([0., 0., 0., 255.]), self.mono())]

        mono_data = []
        for c in codebook:
            mono_data.append((c, numpy.zeros(self.data.shape[:2])))

        for row in range(self.data.shape[0]):
            for column in range(self.data.shape[1]):
                if self.get_alpha(row, column) == 255:
                    if quantization_mode == QuanzationMode.Nearest:
                        min_norm = 511 # (norm of [255, 255, 255, 255]) + 1
                        best = None
                        for color, bitmap in mono_data:
                            norm = numpy.linalg.norm(self.data[row][column] - color)
                            if norm < min_norm:
                                min_norm = norm
                                best = bitmap
                                if norm == 0:
                                    break
                        best[row][column] = 1
                    else:
                        for color, bitmap in mono_data:
                            if numpy.array_equal(color, self.data[row][column]):
                                bitmap[row][column] = 1
                                break

        return mono_data

    def mono(self):
        """!
        Returns a bit mask of opaque pixels
        """
        mono_data = numpy.zeros(self.data.shape[:2])
        for row in range(self.data.shape[0]):
            for column in range(self.data.shape[1]):
                mono_data[row][column] = int(self.data[row][column][3] == 255)
        return mono_data


class Vectorizer:
    def __init__(self, *a, **kw):
        self.animation = objects.Animation(*a, **kw)
        self.palette = None
        self.layers = {}

    def _create_layer(self, layer_name):
        layer = self.animation.add_layer(objects.ShapeLayer())
        if layer_name:
            self.layers[layer_name] = layer
            layer.name = layer_name
        return layer

    def prepare_layer(self, layer_name=None):
        layer = self._create_layer(layer_name)
        layer._max_verts = {}
        if self.palette is None:
            group = layer.add_shape(objects.Group())
            group.name = "bitmap"
            layer._max_verts[group.name] = 0
            group.add_shape(objects.Path())
            group.add_shape(objects.Fill(NVector(0, 0, 0)))
        else:
            for color in self.palette:
                group = layer.add_shape(objects.Group())
                group.name = "color_%s" % "".join("%02x" % int(c) for c in color)
                layer._max_verts[group.name] = 0
                fcol = color/255
                fill = group.add_shape(objects.Fill(NVector(*fcol)))
                if len(fcol) > 3 and fcol[3] < 1:
                    fill.opacity.value = fcol[3] * 100
        return layer

    def raster_to_layer(self, raster, layer_name=None, mode=QuanzationMode.Nearest):
        layer = self.prepare_layer()
        mono_data = raster.quantize(self.palette, mode)
        for (color, bitmap), group in zip(mono_data, layer.shapes):
            self.raster_to_bezier(group, bitmap)

    def raster_to_bezier(self, group, mono_data):
        bmp = potrace.Bitmap(mono_data)
        path = bmp.trace()
        shapes = []
        for curve in path:
            shape = group.insert_shape(0, objects.Path())
            shapes.append(shape)
            bezier = shape.shape.value
            bezier.add_point(NVector(*curve.start_point))
            for segment in curve:
                if segment.is_corner:
                    bezier.add_point(NVector(*segment.c))
                    bezier.add_point(NVector(*segment.end_point))
                else:
                    sp = NVector(*bezier.vertices[-1])
                    ep = NVector(*segment.end_point)
                    c1 = NVector(*segment.c1) - sp
                    c2 = NVector(*segment.c2) - ep
                    bezier.out_tangents[-1] = c1
                    bezier.add_point(ep, c2)
        return shapes

    def raster_to_frame(self, raster, layer_name, time, mode=QuanzationMode.Nearest):
        if layer_name not in self.layers:
            layer = self.prepare_layer(layer_name)
        else:
            layer = self.layers[layer_name]

        mono_data = raster.quantize(self.palette, mode)
        for (color, bitmap), group in zip(mono_data, layer.shapes):
            shapes = self.raster_to_bezier(group, bitmap)
            if shapes:
                # TODO handle multiple shapes
                nverts = len(shapes[0].shape.value.vertices)
                if nverts > layer._max_verts[group.name]:
                    layer._max_verts[group.name] = nverts
                for shape in shapes:
                    bezier = shape.shape.value
                    shape.shape.add_keyframe(time, bezier)

    def adjust_missing_vertices(self, layer_name):
        layer = self.layers[layer_name]
        for group in layer.shapes:
            # TODO handle multiple shapes
            shape = group.shapes[0]
            nverts = layer._max_verts[group.name]
            for kf in shape.shape.keyframes:
                bezier = kf.start
                count = nverts - len(bezier.vertices)
                bezier.vertices += [bezier.vertices[-1]] * count
                bezier.in_tangents += [NVector(0, 0)] * count
                bezier.out_tangents += [NVector(0, 0)] * count

    def duplicate_start_frame(self, layer_name, time):
        layer = self.layers[layer_name]
        for group in layer.shapes:
            shape = group.shapes[0]
            bezier = shape.shape.keyframes[0].start
            group.shapes[0].shape.add_keyframe(time, bezier)


def raster_to_animation(filename, n_colors=1, palette=[], mode=QuanzationMode.Nearest):
    vc = Vectorizer(60)
    raster = RasterImage.open(filename)
    if palette:
        vc.palette = palette
    elif n_colors > 1:
        vc.palette = raster.k_means(n_colors)

    vc.raster_to_layer(raster, None, mode)
    return vc.animation


def color2numpy(vcolor):
    l = (vcolor * 255).components
    if len(l) == 3:
        l.append(255)
    return numpy.array(l, numpy.uint8)


def raster_frames_to_animation(files, n_colors=1, frame_delay=1, start_time=0,
                               looping=True, framerate=60, palette=[], mode=QuanzationMode.Nearest):
    nframes = len(files)
    if not looping:
        nframes -= 1
    vc = Vectorizer(start_time + frame_delay * nframes, framerate=framerate)

    raster = RasterImage.open(files.pop(0))
    if palette:
        vc.palette = [color2numpy(c) for c in palette]
    elif n_colors > 1:
        vc.palette = raster.k_means(n_colors)

    time = start_time
    vc.raster_to_frame(raster, "anim", time, mode)

    for filename in files:
        raster = RasterImage.open(filename)
        time += frame_delay
        vc.raster_to_frame(raster, "anim", time, mode)

    vc.adjust_missing_vertices("anim")
    if looping:
        vc.duplicate_start_frame("anim", time + frame_delay)

    return vc.animation
