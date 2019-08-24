from PIL import Image
from .. import objects
from .. import NVector, Color


def pixel_add_layer(animation, raster):
    raster = raster.convert("RGBA")
    layer = animation.add_layer(objects.ShapeLayer())
    last_rects = {}
    groups = {}

    def merge_up():
        if last_rect and last_rect._start in last_rects:
            yrect = last_rects[last_rect._start]
            if yrect.size.value.x == last_rect.size.value.x and yrect._color == last_rect._color:
                groups[last_rect._color].remove(last_rect)
                yrect.position.value.y += 0.5
                yrect.size.value.y += 1
                rects[last_rect._start] = yrect

    def group(colort):
        return groups.setdefault(colort, set())

    for y in range(raster.height):
        rects = {}
        last_color = None
        last_rect = None
        for x in range(raster.width):
            colort = raster.getpixel((x, y))
            if colort[-1] == 0:
                continue
            yrect = last_rects.get(x, None)
            if colort == last_color:
                last_rect.position.value.x += 0.5
                last_rect.size.value.x += 1
            elif yrect and colort == yrect._color and yrect.size.value.x == 1:
                yrect.position.value.y += 0.5
                yrect.size.value.y += 1
                rects[x] = yrect
                last_color = last_rect = colort = None
            else:
                merge_up()
                g = group(colort)
                last_rect = objects.Rect()
                g.add(last_rect)
                last_rect.size.value = NVector(1, 1)
                last_rect.position.value = NVector(x + 0.5, y + 0.5)
                rects[x] = last_rect
                last_rect._start = x
                last_rect._color = colort
            last_color = colort
        merge_up()
        last_rects = rects

    for colort, rects in groups.items():
        g = layer.add_shape(objects.Group())
        g.shapes = list(rects) + g.shapes
        g.name = "".join("%02x" % c for c in colort)
        fill = g.add_shape(objects.Fill())
        fill.color.value = Color.from_uint8(*colort[:3])
        fill.opacity.value = colort[-1] / 255 * 100
        stroke = g.add_shape(objects.Stroke(fill.color.value, 0.1))
        stroke.opacity.value = fill.opacity.value
    return layer


def _vectorizing_func(filenames, frame_delay, framerate, callback):
    if not isinstance(filenames, list):
        filenames = [filenames]

    animation = objects.Animation(0, framerate)
    nframes = 0

    for filename in filenames:
        raster = Image.open(filename)
        if nframes == 0:
            animation.width = raster.width
            animation.height = raster.height
        if not getattr(raster, "is_animated", False):
            raster.n_frames = 1
            raster.seek = lambda x: None
        for frame in range(raster.n_frames):
            raster.seek(frame)
            callback(animation, raster, nframes + frame)
        nframes += raster.n_frames

    animation.out_point = frame_delay * nframes
    animation._nframes = nframes

    return animation


def pixel_to_animation(filenames, frame_delay=1, framerate=60):
    def callback(animation, raster, frame):
        layer = pixel_add_layer(animation, raster)
        layer.in_point = frame * frame_delay
        layer.out_point = layer.in_point + frame_delay

    return _vectorizing_func(filenames, frame_delay, framerate, callback)
