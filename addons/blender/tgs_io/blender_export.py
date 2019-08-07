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

    def v_relative(self, obj, vector):
        return (
            self.vpix3d(obj.matrix_world @ vector) -
            self.vpix3d(obj.matrix_world @ mathutils.Vector([0, 0, 0]))
        )

    def get_xyz(self, vector):
        x = 0
        y = 1
        z = 2
        # TODO handle this properly
        if round(self.camera_angles.x) == 90:
            y, z = z, y
        return NVector(vector[x], vector[y], vector[z])

    def get_xy(self, vector):
        return NVector(*self.get_xyz(vector).components[:2])


class BlenderTgsExporter:
    def adjust_animation(self, scene, animation, ro):
        pass

    def adjust_collection(self, scene, animation, ro):
        pass

    def adjust_shape(self, obj, g, ro):
        pass

    def add_point_to_bezier(self, bez, point, ro):
        pass

    def add_point_to_poly(self, bez, point, ro):
        pass

    def curve_to_shape(self, obj, parent, ro: RenderOptions):
        g = parent.add_shape(tgs.objects.Group())
        g.name = obj.name

        for spline in obj.data.splines:
            sh = tgs.objects.Path()
            g.add_shape(sh)
            if not obj.data.shape_keys:
                bez = sh.shape.value = tgs.objects.Bezier()
                bez.closed = spline.use_cyclic_u
                if spline.type == "BEZIER":
                    for point in spline.bezier_points:
                        self.add_point_to_bezier(bez, point, ro)
                else:
                    for point in spline.points:
                        self.add_point_to_poly(bez, point, ro)
            else:
                beziers = []
                keyframes = []
                animation = AnimationWrapper(obj.data.shape_keys)
                # ShapeKey
                for kb in obj.data.shape_keys.key_blocks:
                    bez = tgs.objects.Bezier()
                    bez.closed = spline.use_cyclic_u
                    # ShapeKeyBezierPoint
                    for point in kb.data:
                        self.add_point_to_bezier(bez, point, ro)
                    beziers.append(bez)
                    propname = repr(kb)[len(repr(kb.id_data))+1:] + ".value"
                    prop = animation.property(propname)
                    if prop.is_animated:
                        for keyframe in prop.keyframes:
                            keyframes.append((
                                keyframe.time,
                                keyframe.value[0],
                                len(beziers)-1
                            ))

                sh.shape.add_keyframe(ro.scene.frame_start, beziers[0])
                for time, value, bezid in sorted(keyframes, key=lambda x: (x[0], -x[1])):
                    if time != sh.shape.keyframes[0].time:
                        # TODO interpolate when not 1/0 values
                        if value == 1:
                            sh.shape.add_keyframe(time, beziers[bezid])
                        elif value == 0:
                            sh.shape.add_keyframe(time, beziers[0])

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

        return g

    def object_to_shape(self, obj, parent, ro):
        g = None

        if obj.type == "CURVE":
            g = self.curve_to_shape(obj, parent, ro)

        if g:
            self.adjust_shape(obj, g, ro)

    def collection_make_group(self, collection, parent, ro):
        g = tgs.objects.Group()
        parent.add_shape(g)
        g.name = collection.name
        return g

    def collection_to_group(self, collection, parent, ro: RenderOptions):
        g = self.collection_make_group(collection, parent, ro)

        for obj in collection.children:
            self.collection_to_group(obj, g, ro)

        for obj in collection.objects:
            self.object_to_shape(obj, g, ro)

        self.adjust_collection(collection, g, ro)

        return g

    def scene_to_tgs(self, scene):
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

        self.collection_to_group(scene.collection, layer, ro)
        self.adjust_animation(scene, animation, ro)

        return animation


class BlenderTgsExporterKeepStructure(BlenderTgsExporter):
    def add_point_to_bezier(self, bez, point, ro):
        vert = point.co
        in_t = point.handle_left - vert
        out_t = point.handle_right - vert
        bez.add_point(NVector(*vert[:]), NVector(*in_t[:]), NVector(*out_t[:]))

    def add_point_to_poly(self, bez, point, ro):
        bez.add_point(NVector(*point.co[:]))

    def adjust_collection(self, collection, g, ro):
        transf = g.shapes.pop()
        g.shapes = list(sorted(g.shapes, key=lambda x: x._z))
        g._z = sum(x._z for x in g.shapes) / len(g.shapes)
        g.shapes.append(transf)

    def adjust_animation(self, scene, animation, ro):
        view_frame = scene.camera.data.view_frame(scene=scene)
        camera_p1 = NVector(*view_frame[0][:-1])
        camera_size = camera_p1 - NVector(*view_frame[2][:-1])
        layer = animation.layers[0]
        layer.transform.scale.value.x *= scene.render.resolution_x / (camera_size.x or 1)
        layer.transform.scale.value.y *= -scene.render.resolution_y / (camera_size.y or 1)
        layer.transform.position.value.y += animation.height
        layer.transform.position.value += ro.vpix(mathutils.Vector([0, 0, 0]))

    def adjust_shape(self, obj, g, ro):
        animated = AnimationWrapper(obj)
        g.transform.position = animated.location.to_lottie_prop(ro.get_xy)
        g.transform.scale = animated.scale.to_lottie_prop(lambda v: NVector(v[0], v[1]) * 100)
        g.transform.rotation = animated.rotation_euler.to_lottie_prop(
            lambda v: -ro.get_xyz(v).z/math.pi*180,
            tgs.objects.Value
        )
        g._z = ro.get_xyz(obj.location).z


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


def scene_to_tgs(scene):
    return BlenderTgsExporterKeepStructure().scene_to_tgs(scene)
