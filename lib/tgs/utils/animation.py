import random
import math
from .nvector import NVector
from ..objects.shapes import Shape


def shake(position_prop, x_radius, y_radius, start_time, end_time, n_frames):
    if not isinstance(position_prop, list):
        position_prop = [position_prop]

    n_frames = int(round(n_frames))
    frame_time = (end_time - start_time) / n_frames
    startpoints = list(map(
        lambda pp: pp.get_value(start_time),
        position_prop
    ))

    for i in range(n_frames):
        x = (random.random() * 2 - 1) * x_radius
        y = (random.random() * 2 - 1) * y_radius
        for pp, start in zip(position_prop, startpoints):
            px = start[0] + x
            py = start[1] + y
            pp.add_keyframe(start_time + i * frame_time, [px, py])

    for pp, start in zip(position_prop, startpoints):
        pp.add_keyframe(end_time, start)


def rot_shake(rotation_prop, angles, start_time, end_time, n_frames):
    frame_time = (end_time - start_time) / n_frames
    start = rotation_prop.get_value(start_time)

    first = 0
    for i in range(0, n_frames):
        a = angles[i % len(angles)] * math.sin(i/n_frames * math.pi)
        rotation_prop.add_keyframe(start_time + i * frame_time, start + a)
    rotation_prop.add_keyframe(end_time, start)


def spring_pull(position_prop, point, start_time, end_time, falloff=15, oscillations=7):
    start = NVector(*position_prop.get_value(start_time))
    point = NVector(*point)
    d = start-point

    delta = (end_time - start_time) / oscillations

    for i in range(oscillations):
        time_x = i / oscillations
        factor = math.cos(time_x * math.pi * oscillations) * (1-time_x**(1/falloff))
        p = point + d * factor
        position_prop.add_keyframe(start_time + delta * i, p.to_list())

    position_prop.add_keyframe(end_time, point.to_list())


def follow_path(position_prop, bezier, start_time, end_time, n_keyframes, reverse=False):
    delta = (end_time - start_time) / n_keyframes
    for i in range(n_keyframes):
        time = start_time + i * delta
        fact = i / (n_keyframes-1)
        if reverse:
            fact = 1 - fact
        position_prop.add_keyframe(time, bezier.point_at(fact).to_list())


def generate_path_appear(bezier, appear_start, appear_end, n_keyframes, reverse=False):
    obj = Shape()
    beziers = []
    maxp = 0

    time_delta = (appear_end - appear_start) / n_keyframes
    for i in range(n_keyframes+1):
        time = appear_start + i * time_delta
        t2 = (time - appear_start) / (appear_end - appear_start)

        if reverse:
            t2 = 1 - t2
            segment = bezier.segment(t2, 1)
            segment.reverse()
        else:
            segment = bezier.segment(0, t2)

        beziers.append(segment)
        if len(segment.vertices) > maxp:
            maxp = len(segment.vertices)

        obj.vertices.add_keyframe(time, segment)

    for segment in beziers:
        deltap = maxp - len(segment.vertices)
        if deltap > 0:
            segment.vertices += [segment.vertices[-1]] * deltap
            segment.in_point += [[0,0]] * deltap
            segment.out_point += [[0,0]] * deltap

    return obj


def generate_path_disappear(bezier, disappear_start, disappear_end, n_keyframes, reverse=False):
    obj = Shape()
    beziers = []
    maxp = 0

    time_delta = (disappear_end - disappear_start) / n_keyframes
    for i in range(n_keyframes+1):
        time = disappear_start + i * time_delta
        t1 = (time - disappear_start) / (disappear_end - disappear_start)
        if reverse:
            t1 = 1 - t1
            segment = bezier.segment(0, t1)
        else:
            segment = bezier.segment(1, t1)
            segment.reverse()

        beziers.append(segment)
        if len(segment.vertices) > maxp:
            maxp = len(segment.vertices)

        obj.vertices.add_keyframe(time, segment)

    for segment in beziers:
        deltap = maxp - len(segment.vertices)
        if deltap > 0:
            segment.vertices += [segment.vertices[-1]] * deltap
            segment.in_point += [[0,0]] * deltap
            segment.out_point += [[0,0]] * deltap

    return obj


def generate_path_segment(bezier, appear_start, appear_end, disappear_start, disappear_end, n_keyframes, reverse=False):
    obj = Shape()
    beziers = []
    maxp = 0

    # HACK: For some reson reversed works better
    if not reverse:
        bezier.reverse()

    time_delta = (appear_end - appear_start) / n_keyframes
    for i in range(n_keyframes+1):
        time = appear_start + i * time_delta
        t1 = (time - disappear_start) / (disappear_end - disappear_start)
        t2 = (time - appear_start) / (appear_end - appear_start)

        t1 = max(0, min(1, t1))
        t2 = max(0, min(1, t2))

        #if reverse:
        if True:
            t1 = 1 - t1
            t2 = 1 - t2
            segment = bezier.segment(t2, t1)
            segment.reverse()
        #else:
            #segment = bezier.segment(t1, t2)
            #segment.reverse()

        beziers.append(segment)
        if len(segment.vertices) > maxp:
            maxp = len(segment.vertices)

        obj.vertices.add_keyframe(time, segment)

    for segment in beziers:
        deltap = maxp - len(segment.vertices)
        if deltap > 0:
            segment.split_self_chunks(deltap+1)

    # HACK: Restore
    if not reverse:
        bezier.reverse()
    return obj
