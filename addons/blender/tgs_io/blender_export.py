import os
import sys

from . import tgs
from .tgs import NVector

import bpy


class ExportOptions:
    def __init__(self, scale=64, offx=0, offy=0):
        self.scale = scale
        self.offx = offx
        self.offy = offy


def object_to_shape(obj, parent, lt):
    if obj.type == "CURVE":
        g = parent.add_shape(tgs.objects.Group())
        g.name = obj.name

        for spline in obj.data.splines:
            sh = tgs.objects.Path()
            g.add_shape(sh)
            bez = sh.shape.value = tgs.objects.Bezier()
            bez.closed = spline.use_cyclic_u
            if spline.type == "BEZIER":
                for point in spline.bezier_points:
                    vert = point.co
                    in_t = point.handle_left - vert
                    out_t = point.handle_right - vert
                    bez.add_point(NVector(*vert[:]), NVector(*in_t[:]), NVector(*out_t[:]))
            else:
                for point in spline.points:
                    bez.add_point(NVector(*point.co[:]))

        if obj.data.fill_mode != "NONE":
            fillc = obj.active_material.diffuse_color
            fill = tgs.objects.Fill(NVector(*fillc[:-1]))
            fill.opacity.value = fillc[-1] * 100
            g.add_shape(fill)

        if lt > 0:
            strokec = obj.active_material.diffuse_color
            stroke = tgs.objects.Stroke(NVector(*strokec[:-1]), lt)
            stroke.opacity.value = fillc[-1] * 100
            g.add_shape(stroke)


def collection_to_group(collection, parent, lt):
    g = tgs.objects.Group()
    parent.add_shape(g)
    g.name = collection.name

    # TODO sort by z
    for obj in collection.children:
        collection_to_group(obj, g, lt)

    for obj in collection.objects:
        object_to_shape(obj, g, lt)

    return g


def scene_to_tgs(scene, eo=ExportOptions()):
    animation = tgs.objects.Animation()
    animation.in_point = scene.frame_start
    animation.out_point = scene.frame_end
    animation.framerate = scene.render.fps
    animation.width = scene.render.resolution_x
    animation.height = scene.render.resolution_y
    animation.name = scene.name
    layer = animation.add_layer(tgs.objects.ShapeLayer())

    if scene.render.use_freestyle:
        line_thickness = scene.render.line_thickness
    else:
        line_thickness = 0
    g = collection_to_group(scene.collection, layer, line_thickness)
    g.transform.scale.value *= eo.scale
    g.transform.scale.value.y *= -1
    g.transform.position.value.x += eo.offx
    g.transform.position.value.y += eo.offy + animation.height

    return animation
