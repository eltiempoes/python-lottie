import random
import math
from .nvector import NVector
from ..objects.shapes import Shape
from .. import objects


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
    start = position_prop.get_value(start_time)
    d = start-point

    delta = (end_time - start_time) / oscillations

    for i in range(oscillations):
        time_x = i / oscillations
        factor = math.cos(time_x * math.pi * oscillations) * (1-time_x**(1/falloff))
        p = point + d * factor
        position_prop.add_keyframe(start_time + delta * i, p)

    position_prop.add_keyframe(end_time, point)


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
            segment.in_point += [NVector(0,0)] * deltap
            segment.out_point += [NVector(0,0)] * deltap

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
            segment.in_point += [NVector(0,0)] * deltap
            segment.out_point += [NVector(0,0)] * deltap

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


def sine_displace(
    prop,
    wavelength,
    amplitude,
    time_start,
    time_end,
    n_frames,
    speed=1,
    axis=90,
):
    """
    Displaces a position property as if it were following a sine wave

    prop        Multidimensional property to animate
    wavelength  Distance between consecutive peaks
    amplitude   Distance from a peak to the original position
    time_start  When the animation shall start
    time_end    When the animation shall end
    n_frames    Number of keyframes to add
    speed       Number of peaks a point will go through in the given time
                If negative, it will go the other way
    axis        Wave peak direction
    """
    speed_f = math.pi * 2 * speed
    time_delta = (time_end - time_start) / n_frames
    axis = axis / 180 * math.pi

    startpos = prop.get_value(time_start)
    for f in range(n_frames+1):
        p = _sine_displace(startpos, wavelength, amplitude, f, n_frames, speed_f, axis)
        prop.add_keyframe(f * time_delta + time_start, p)


def _sine_displace(startpos, wavelength, amplitude, f, n_frames, speed_f, axis):
        off = -math.sin(startpos[0]/wavelength*math.pi*2-f*speed_f/n_frames) * amplitude
        x = startpos[0] + off * math.cos(axis)
        y = startpos[1] + off * math.sin(axis)
        return NVector(x, y)


def sine_displace_bezier(
    prop,
    wavelength,
    amplitude,
    time_start,
    time_end,
    n_frames,
    speed=1,
    axis=90,
):
    """
    Same as sine_displace but for paths
    """
    speed_f = math.pi * 2 * speed
    time_delta = (time_end - time_start) / n_frames
    axis = axis / 180 * math.pi

    initial = prop.get_value(time_start)
    for f in range(n_frames+1):
        bezier = objects.Bezier()
        bezier.closed = initial.closed

        for pi in range(len(initial.vertices)):
            startpos = initial.vertices[pi]

            p = _sine_displace(startpos, wavelength, amplitude, f, n_frames, speed_f, axis)
            t1sp = initial.in_point[pi] + startpos
            t1abs = _sine_displace(t1sp, wavelength, amplitude, f, n_frames, speed_f, axis)
            t2sp = initial.out_point[pi] + startpos
            t2abs = _sine_displace(t2sp, wavelength, amplitude, f, n_frames, speed_f, axis)

            bezier.add_point(p, t1abs - p, t2abs - p)

        prop.add_keyframe(f * time_delta + time_start, bezier)
