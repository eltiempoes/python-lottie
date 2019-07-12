# NOTE: requires pillow, pypotrace>=0.2, numpy, scipy to be installed
from PIL import Image
import potrace
import numpy
from scipy.cluster.vq import kmeans
from .. import objects




def quantize(data, n_colors):
    if n_colors <= 1:
        mono_data = numpy.zeros(data.shape[:2])
        color = [0, 0, 0, 255]
        for row in range(data.shape[0]):
            for column in range(data.shape[1]):
                mono_data[row][column] = int(data[row][column][3] == 255)
        return [(color, mono_data)]

    colors = []
    for row in range(data.shape[0]):
        for column in range(data.shape[1]):
            if data[row][column][3] == 255:
                colors.append(data[row][column])

    colors = numpy.array(colors, numpy.float)
    codebook = kmeans(colors, n_colors)[0]
    mono_data = []
    for c in codebook:
        mono_data.append((c, numpy.zeros(data.shape[:2])))

    for row in range(data.shape[0]):
        for column in range(data.shape[1]):
            if data[row][column][3] == 255:
                min_norm = 511 # (norm of [255, 255, 255, 255]) + 1
                best = None
                for color, bitmap in mono_data:
                    norm = numpy.linalg.norm(data[row][column] - color)
                    if norm < min_norm:
                        min_norm = norm
                        best = bitmap
                        if norm == 0:
                            break
                best[row][column] = 1

    return mono_data



def raster_to_shapes(parent, filename, n_colors=1):
    image = Image.open(filename)
    data = numpy.array(image)

    mono_data = quantize(data, n_colors)

    for color, bitmap in mono_data:
        group = parent.add_shape(objects.Group())
        shape = group.add_shape(objects.Shape())
        group.add_shape(objects.Fill(list(color/255)))
        raster_to_bezier(shape.vertices.value, bitmap)


def raster_to_bezier(bezier, mono_data):
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


def raster_to_animation(filename, n_colors=1):
    anim = objects.Animation(60)
    layer = anim.add_layer(objects.ShapeLayer())
    raster_to_shapes(layer, filename, n_colors)
    return anim


from ..exporters import multiexport, export_svg
an = raster_to_animation("/tmp/bitmap.png", 2)
multiexport(an, "/tmp/out")
export_svg(an, "/tmp/out.svg")
