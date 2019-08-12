import os
import sys
import math
from dataclasses import dataclass

sys.path.append(os.path.dirname(__file__))
import tgs
from tgs import NVector

import bpy
import bpy_extras
import mathutils


@dataclass
class RenderOptions:
    scene: bpy.types.Scene
    line_width: float = 0
    camera_angles: NVector = NVector(0, 0, 0)

    @property
    def camera(self):
        return scene.camera

    def vector_to_camera_norm(self, vector):
        return NVector(*bpy_extras.object_utils.world_to_camera_view(
            self.scene,
            self.scene.camera,
            vector
        ))

    def vpix3d(self, vector):
        v3d = self.vector_to_camera_norm(vector)
        v3d.x *= self.scene.render.resolution_x
        v3d.y *= -self.scene.render.resolution_y
        return v3d

    def vpix(self, vector):
        v2d = self.vpix3d(vector)
        v2d.components.pop()
        return v2d

    def vpix3d_r(self, obj, vector):
        return (
            self.vpix3d(obj.matrix_world @ vector)
        )

    def vpix_r(self, obj, vector):
        v2d = self.vpix3d_r(obj, vector)
        v2d.components.pop()
        return v2d


class AnimatedProperty:
    def __init__(self, wrapper, name):
        self.wrapper = wrapper
        self.name = name

    @property
    def is_animated(self):
        return self.name in self.wrapper.animation

    @property
    def value(self):
        return self.wrapper.object.path_resolve(self.name)

    @property
    def keyframes(self):
        return self.wrapper.animation[self.name]

    def to_lottie_prop(self, value_transform, animatable=tgs.objects.MultiDimensional):
        md = animatable()
        if self.is_animated:
            for keyframe in self.keyframes:
                md.add_keyframe(
                    keyframe.time,
                    value_transform(keyframe.to_vector()),
                    keyframe.easing()
                )
        else:
            md.value = value_transform(self.value)
        return md


class AnimationKeyframe:
    def __init__(self, fc, kf):
        self.time = kf.co.x
        self.value = {
            fc.array_index: kf.co.y
        }

    def __setitem__(self, key, value):
        self.value[key] = value

    def to_vector(self):
        return mathutils.Vector([v for k, v in sorted(self.value.items())])

    # TODO pull easing
    def easing(self):
        return tgs.objects.easing.Linear()


class AnimationWrapper:
    def __init__(self, object):
        self.object = object
        self.animation = {}
        if object.animation_data:
            for fc in object.animation_data.action.fcurves:
                if fc.data_path not in self.animation:
                    self.animation[fc.data_path] = [
                        AnimationKeyframe(fc, kf)
                        for kf in fc.keyframe_points
                    ]
                else:
                    for internal, kf in zip(self.animation[fc.data_path], fc.keyframe_points):
                        internal[fc.array_index] = kf.co.y

    def __getattr__(self, name):
        return self.property(name)

    def property(self, name):
        return AnimatedProperty(self, name)

    def keyframe_times(self):
        kft = set()
        for kfl in self.animation.values():
            kft |= set(kf.time for kf in kfl)
        return kft


def scene_to_tgs(scene):
    initial_frame = scene.frame_current
    try:
        animation = tgs.objects.Animation()
        animation.in_point = scene.frame_start
        animation.out_point = scene.frame_end
        animation.framerate = scene.render.fps
        animation.width = scene.render.resolution_x
        animation.height = scene.render.resolution_y
        animation.name = scene.name
        layer = animation.add_layer(tgs.objects.ShapeLayer())

        ro = RenderOptions(scene)
        if scene.render.use_freestyle:
            ro.line_width = scene.render.line_thickness
        else:
            ro.line_width = 0
        ro.camera_angles = NVector(*scene.camera.rotation_euler) * 180 / math.pi

        collection_to_group(scene.collection, layer, ro)
        adjust_animation(scene, animation, ro)

        return animation
    finally:
        scene.frame_set(initial_frame)


def adjust_animation(scene, animation, ro):
    layer = animation.layers[0]
    layer.transform.position.value.y += animation.height
    layer.shapes = list(sorted(layer.shapes, key=lambda x: x._z))
    layer._z = sum(x._z for x in layer.shapes) / len(layer.shapes)


def collection_to_group(collection, parent, ro: RenderOptions):
    g = parent

    for obj in collection.children:
        collection_to_group(obj, g, ro)

    for obj in collection.objects:
        object_to_shape(obj, g, ro)

    return g


def object_to_shape(obj, parent, ro):
    g = None

    if obj.type == "CURVE":
        g = curve_to_shape(obj, parent, ro)

    if g:
        ro.scene.frame_set(0)
        g._z = ro.vpix3d(obj.location).z


def curve_to_shape(obj, parent, ro: RenderOptions):
    g = parent.add_shape(tgs.objects.Group())
    g.name = obj.name
    beziers = []

    animated = AnimationWrapper(obj)
    for spline in obj.data.splines:
        sh = tgs.objects.Path()
        g.add_shape(sh)
        sh.shape.value = curve_get_bezier(spline, obj, ro)
        beziers.append(sh.shape.value)

    times = animated.keyframe_times()
    shapekeys = None
    if obj.data.shape_keys:
        shapekeys = AnimationWrapper(obj.data.shape_keys)
        times |= shapekeys.keyframe_times()

    times = list(sorted(times))
    for time in times:
        ro.scene.frame_set(time)
        if not shapekeys:
            for spline, sh in zip(obj.data.splines, g.shapes):
                sh.shape.add_keyframe(time, curve_get_bezier(spline, obj, ro))
        else:
            obj.shape_key_add(from_mix=True)
            shape_key = obj.data.shape_keys.key_blocks[-1]
            start = 0
            for spline, sh, bezier in zip(obj.data.splines, g.shapes, beziers):
                end = start + len(bezier.vertices)
                bez = tgs.objects.Bezier()
                bez.closed = bezier.closed
                for i in range(start, end):
                    add_point_to_bezier(bez, shape_key.data[i], ro, obj)
                sh.shape.add_keyframe(time, bez)
                start = end
            obj.shape_key_remove(shape_key)

    curve_apply_material(obj, g, ro)
    return g


def curve_apply_material(obj, g, ro):
    if obj.data.fill_mode != "NONE":
        # TODO animation
        fillc = obj.active_material.diffuse_color
        fill = tgs.objects.Fill(NVector(*fillc[:-1]))
        fill.opacity.value = fillc[-1] * 100
        g.add_shape(fill)

    if ro.line_width > 0:
        # TODO animation
        strokec = obj.active_material.line_color
        stroke = tgs.objects.Stroke(NVector(*strokec[:-1]), ro.line_width)
        stroke.opacity.value = fillc[-1] * 100
        g.add_shape(stroke)


def curve_get_bezier(spline, obj, ro):
    bez = tgs.objects.Bezier()
    bez.closed = spline.use_cyclic_u
    if spline.type == "BEZIER":
        for point in spline.bezier_points:
            add_point_to_bezier(bez, point, ro, obj)
    else:
        for point in spline.points:
            add_point_to_poly(bez, point, ro, obj)
    return bez


def add_point_to_bezier(bez, point, ro: RenderOptions, obj):
    vert = ro.vpix_r(obj, point.co)
    in_t = ro.vpix_r(obj, point.handle_left) - vert
    out_t = ro.vpix_r(obj, point.handle_right) - vert
    bez.add_point(vert, in_t, out_t)


def add_point_to_poly(bez, point, ro, obj):
    bez.add_point(ro.vpix_r(obj, point.co))
