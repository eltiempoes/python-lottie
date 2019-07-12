# NOTE: requires pillow, pypotrace>=0.2, numpy, scipy to be installed
from PIL import Image
import potrace
import numpy
from scipy.cluster.vq import kmeans
from .. import objects


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
        """
        Returns a list of centroids
        """
        colors = []
        for row in range(self.data.shape[0]):
            for column in range(self.data.shape[1]):
                if self.get_alpha(row, column) == 255:
                    colors.append(self.data[row][column])

        colors = numpy.array(colors, numpy.float)
        return kmeans(colors, n_colors)[0]

    def get_alpha(self, row, column):
        if self.data.shape[2] >= 4:
            return self.data[row][column][3]
        return 255

    def quantize(self, codebook):
        """
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

        return mono_data

    def mono(self):
        """
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
            group.add_shape(objects.Shape())
            group.add_shape(objects.Fill([0, 0, 0]))
        else:
            for color in self.palette:
                group = layer.add_shape(objects.Group())
                group.name = "color_%s" % "".join("%02x" % int(c) for c in color)
                layer._max_verts[group.name] = 0
                group.add_shape(objects.Shape())
                fcol = color/255
                fill = group.add_shape(objects.Fill(list(fcol)))
                if len(fcol) > 3 and fcol[3] < 1:
                    fill.opacity.value = fcol[3] * 100
        return layer

    def raster_to_layer(self, raster, layer_name=None):
        layer = self.prepare_layer()
        mono_data = raster.quantize(self.palette)
        for (color, bitmap), group in zip(mono_data, layer.shapes):
            shape = group.shapes[0]
            self.raster_to_bezier(shape.vertices.value, bitmap)

    def raster_to_bezier(self, bezier, mono_data):
        bmp = potrace.Bitmap(mono_data)
        path = bmp.trace()
        for curve in path:
            bezier.add_point(list(curve.start_point))
            for segment in curve:
                if segment.is_corner:
                    bezier.add_point(list(segment.c))
                    bezier.add_point(list(segment.end_point))
                else:
                    sp = bezier.vertices[-1]
                    ep = list(segment.end_point)
                    c1 = [segment.c1[0] - sp[0], segment.c1[1] - sp[1]]
                    c2 = [segment.c2[0] - ep[0], segment.c2[1] - ep[1]]
                    bezier.out_point[-1] = c1
                    bezier.add_point(ep, c2)

    def raster_to_frame(self, raster, layer_name, time):
        if layer_name not in self.layers:
            layer = self.prepare_layer(layer_name)
        else:
            layer = self.layers[layer_name]

        mono_data = raster.quantize(self.palette)
        for (color, bitmap), group in zip(mono_data, layer.shapes):
            bezier = objects.Bezier()
            self.raster_to_bezier(bezier, bitmap)
            group.shapes[0].vertices.add_keyframe(time, bezier)
            nverts = len(bezier.vertices)
            if nverts > layer._max_verts[group.name]:
                layer._max_verts[group.name] = nverts

    def adjust_missing_vertices(self, layer_name):
        layer = self.layers[layer_name]
        for group in layer.shapes:
            shape = group.shapes[0]
            nverts = layer._max_verts[group.name]
            for kf in shape.vertices.keyframes:
                bezier = kf.start
                count = nverts - len(bezier.vertices)
                bezier.vertices += [bezier.vertices[-1]] * count
                bezier.in_point += [[0, 0]] * count
                bezier.out_point += [[0, 0]] * count

    def duplicate_start_frame(self, layer_name, time):
        layer = self.layers[layer_name]
        for group in layer.shapes:
            shape = group.shapes[0]
            bezier = shape.vertices.keyframes[0].start
            group.shapes[0].vertices.add_keyframe(time, bezier)


def raster_to_animation(filename, n_colors=1):
    vc = Vectorizer(60)
    raster = RasterImage.open(filename)
    if n_colors > 1:
        vc.palette = raster.k_means(n_colors)

    vc.raster_to_layer(raster)
    return vc.animation


def raster_frames_to_animation(files, n_colors=1, frame_delay=1, start_time=0, looping=True, framerate=60):
    nframes = len(files)
    if not looping:
        nframes -= 1
    vc = Vectorizer(start_time + frame_delay * nframes, framerate=framerate)

    raster = RasterImage.open(files.pop(0))
    if n_colors > 1:
        vc.palette = raster.k_means(n_colors)

    time = start_time
    vc.raster_to_frame(raster, "anim", time)

    for filename in files:
        raster = RasterImage.open(filename)
        time += frame_delay
        vc.raster_to_frame(raster, "anim", time)

    vc.adjust_missing_vertices("anim")
    if looping:
        vc.duplicate_start_frame("anim", time + frame_delay)

    return vc.animation
