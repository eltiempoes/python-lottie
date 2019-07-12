import random
import math
from .nvector import NVector


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
