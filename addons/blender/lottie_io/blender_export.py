import os
import sys
import math
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(__file__))
import lottie
from lottie import NVector

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

    def to_lottie_prop(self, value_transform=lambda x: x, animatable=None):
        v = self.value
        if isinstance(v, mathutils.Vector):
            def_animatable = lottie.objects.MultiDimensional
            kf_getter = AnimationKeyframe.to_vector
        else:
            def_animatable = lottie.objects.Value
            kf_getter = AnimationKeyframe.to_scalar

        if animatable is None:
            animatable = def_animatable

        md = animatable()
        if self.is_animated:
            for keyframe in self.keyframes:
                md.add_keyframe(
                    keyframe.time,
                    value_transform(kf_getter(keyframe)),
                    keyframe.easing()
                )
        else:
            md.value = value_transform(v)
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
        return NVector(*(v for k, v in sorted(self.value.items())))

    def to_scalar(self):
        return next(iter(self.value.values()))

    # TODO pull easing
    def easing(self):
        return lottie.objects.easing.Linear()


class AnimationWrapper:
    def __init__(self, object):
        self.object = object
        self.animation = {}
        if object.animation_data and object.animation_data.action:
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


def context_to_tgs(context):
    scene = context.scene
    root = context.view_layer.layer_collection
    initial_frame = scene.frame_current
    try:
        animation = lottie.objects.Animation()
        animation.in_point = scene.frame_start
        animation.out_point = scene.frame_end
        animation.frame_rate = scene.render.fps
        animation.width = scene.render.resolution_x
        animation.height = scene.render.resolution_y
        animation.name = scene.name
        layer = animation.add_layer(lottie.objects.ShapeLayer())

        ro = RenderOptions(scene)
        if scene.render.use_freestyle:
            ro.line_width = scene.render.line_thickness
        else:
            ro.line_width = 0
        ro.camera_angles = NVector(*scene.camera.rotation_euler) * 180 / math.pi

        collection_to_group(root, layer, ro)
        adjust_animation(scene, animation, ro)

        return animation
    finally:
        scene.frame_set(initial_frame)


def adjust_animation(scene, animation, ro):
    layer = animation.layers[0]
    layer.transform.position.value.y += animation.height
    layer.shapes = list(sorted(layer.shapes, key=lambda x: x._z))


def collection_to_group(collection, parent, ro: RenderOptions):
    if collection.exclude or collection.collection.hide_render:
        return

    for obj in collection.children:
        collection_to_group(obj, parent, ro)

    for obj in collection.collection.objects:
        object_to_shape(obj, parent, ro)


def curve_to_shape(obj, parent, ro: RenderOptions):
    g = parent.add_shape(lottie.objects.Group())
    g.name = obj.name
    beziers = []

    animated = AnimationWrapper(obj)
    for spline in obj.data.splines:
        sh = lottie.objects.Path()
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
                bez = lottie.objects.Bezier()
                bez.closed = bezier.closed
                for i in range(start, end):
                    add_point_to_bezier(bez, shape_key.data[i], ro, obj)
                sh.shape.add_keyframe(time, bez)
                start = end
            obj.shape_key_remove(shape_key)

    curve_apply_material(obj, g, ro)
    return g


def get_fill(obj, ro):
    # TODO animation
    fillc = obj.active_material.diffuse_color
    fill = lottie.objects.Fill(NVector(*fillc[:-1]))
    fill.name = obj.active_material.name
    fill.opacity.value = fillc[-1] * 100
    return fill


def curve_apply_material(obj, g, ro):
    if obj.data.fill_mode != "NONE":
        g.add_shape(get_fill(obj, ro))

    if ro.line_width > 0:
        # TODO animation
        strokec = obj.active_material.line_color
        stroke = lottie.objects.Stroke(NVector(*strokec[:-1]), ro.line_width)
        stroke.opacity.value = fillc[-1] * 100
        g.add_shape(stroke)


def curve_get_bezier(spline, obj, ro):
    bez = lottie.objects.Bezier()
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


def mesh_to_shape(obj, parent, ro):
    # TODO concave hull to optimize
    g = parent.add_shape(lottie.objects.Group())
    g.name = obj.name
    verts = list(ro.vpix_r(obj, v.co) for v in obj.data.vertices)
    fill = get_fill(obj, ro)
    animated = AnimationWrapper(obj)
    times = list(sorted(animated.keyframe_times()))

    def f_bez(f):
        bez = lottie.objects.Bezier()
        bez.close()
        for v in f.vertices:
            bez.add_point(verts[v])
        return bez

    for f in obj.data.polygons:
        shp = g.add_shape(lottie.objects.Group())
        sh = shp.add_shape(lottie.objects.Path())
        shp.add_shape(fill)
        sh.shape.value = f_bez(f)

    if times:
        for time in times:
            ro.scene.frame_set(time)
            verts = list(ro.vpix_r(obj, v.co) for v in obj.data.vertices)

            for f, shp in zip(obj.data.polygons, g.shapes):
                sh = shp.shapes[0]
                sh.shape.add_keyframe(time, f_bez(f))

    return g


def gpencil_to_shape(obj, parent, ro):
    # Object / GreasePencil
    gpen = parent.add_shape(lottie.objects.Group())
    gpen.name = obj.name

    animated = AnimationWrapper(obj.data)
    # GPencilLayer
    for layer in reversed(obj.data.layers):
        if layer.hide:
            continue
        glay = gpen.add_shape(lottie.objects.Group())
        glay.name = layer.info
        opacity = animated.property('layers["%s"].opacity' % layer.info)
        glay.transform.opacity = opacity.to_lottie_prop(lambda x: x*100)

        gframe = None
        # GPencilFrame
        for frame in layer.frames:
            if gframe:
                if not gframe.transform.opacity.animated:
                    gframe.transform.opacity.add_keyframe(0, 100, lottie.objects.easing.Jump())
                gframe.transform.opacity.add_keyframe(frame.frame_number, 0)

            gframe = glay.add_shape(lottie.objects.Group())
            gframe.name = "frame %s" % frame.frame_number
            if frame.frame_number != 0:
                gframe.transform.opacity.add_keyframe(0, 0, lottie.objects.easing.Jump())
                gframe.transform.opacity.add_keyframe(frame.frame_number, 100)

            # GPencilStroke
            for stroke in reversed(frame.strokes):
                gstroke = gframe.add_shape(lottie.objects.Group())

                path = gstroke.add_shape(lottie.objects.Path())
                path.shape.value.closed = stroke.draw_cyclic
                pressure = 0
                for p in stroke.points:
                    add_point_to_poly(path.shape.value, p, ro, obj)
                    pressure += p.pressure
                pressure /= len(stroke.points)

                # Material
                matp = obj.data.materials[stroke.material_index]
                # TODO Gradients / animations
                # MaterialGPencilStyle
                material = matp.grease_pencil

                if material.show_fill:
                    fill_sh = gstroke.add_shape(lottie.objects.Fill())
                    fill_sh.name = matp.name
                    fill_sh.color.value = NVector(*material.fill_color[:-1])
                    fill_sh.opacity.value = material.fill_color[-1] * 100

                if material.show_stroke:
                    stroke_sh = lottie.objects.Stroke()
                    gstroke.add_shape(stroke_sh)
                    stroke_sh.name = matp.name
                    if stroke.end_cap_mode == "ROUND":
                        stroke_sh.line_cap = lottie.objects.LineCap.Round
                    elif stroke.end_cap_mode == "FLAT":
                        stroke_sh.line_cap = lottie.objects.LineCap.Butt
                    stroke_w = stroke.line_width * pressure * obj.data.pixel_factor
                    if obj.data.stroke_thickness_space == "WORLDSPACE":
                        # TODO do this properly
                        stroke_w /= 9
                    stroke_sh.width.value = stroke_w
                    stroke_sh.color.value = NVector(*material.color[:-1])
                    stroke_sh.opacity.value = material.color[-1] * 100



    return gpen


def object_to_shape(obj, parent, ro: RenderOptions):
    if obj.hide_render:
        return

    g = None
    ro.scene.frame_set(0)

    if obj.type == "CURVE":
        g = curve_to_shape(obj, parent, ro)
    elif obj.type == "MESH":
        g = mesh_to_shape(obj, parent, ro)
    elif obj.type == "GPENCIL":
        g = gpencil_to_shape(obj, parent, ro)

    if g:
        ro.scene.frame_set(0)
        g._z = ro.vpix3d(obj.location).z
