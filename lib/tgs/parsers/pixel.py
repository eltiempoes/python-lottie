from PIL import Image
from .. import objects
from .. import NVector, Color


def pixel_add_layer(animation, raster):
    raster = raster.convert("RGBA")
    layer = animation.add_layer(objects.ShapeLayer())
    last_rects = {}
    for y in range(raster.height):
        rects = {}
        last_color = None
        last_rect = None
        for x in range(raster.width):
            colort = raster.getpixel((x, y))
            if colort[-1] == 0:
                continue
            yrect, ycol = last_rects.get(x, (None, None))
            if colort == last_color:
                last_rect.position.value.x += 0.5
                last_rect.size.value.x += 1
            elif yrect and colort == ycol and yrect.size.value.x == 1:
                yrect.position.value.y += 0.5
                yrect.size.value.y += 1
                rects[x] = (yrect, colort)
                last_color = last_rect = colort = None
            else:
                g = layer.add_shape(objects.Group())
                last_rect = g.add_shape(objects.Rect())
                last_rect.size.value = NVector(1, 1)
                last_rect.position.value = NVector(x + 0.5, y + 0.5)
                rects[x] = (last_rect, colort)
                fill = g.add_shape(objects.Fill())
                fill.color.value = Color.from_uint8(*colort[:3])
                fill.opacity.value = colort[-1] / 255 * 100
            last_color = colort
        last_rects = rects
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
