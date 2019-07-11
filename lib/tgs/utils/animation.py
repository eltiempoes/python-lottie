import random
import math


def shake(position_prop, x_radius, y_radius, start_time, end_time, n_frames):
    frame_time = (end_time - start_time) / n_frames
    if not position_prop.animated:
        start_x, start_y = position_prop.value
    else:
        start_x, start_y = position_prop.keyframes[-1].start

    for i in range(n_frames):
        x = start_x + (random.random() * 2 - 1) * x_radius
        y = start_y + (random.random() * 2 - 1) * y_radius
        position_prop.add_keyframe(start_time + i * frame_time, [x, y])


def random_rot_shake(rotation_prop, min_angle, max_angle, start_time, end_time, n_frames):
    frame_time = (end_time - start_time) / n_frames
    if not rotation_prop.animated:
        start = rotation_prop.value
    else:
        start = rotation_prop.keyframes[-1].start
    delta = max_angle - min_angle

    first = 0
    rotation_prop.add_keyframe(start_time, start)
    for i in range(1, n_frames):
        a = start + min_angle + (random.random() * delta)
        rotation_prop.add_keyframe(start_time + i * frame_time, a)
    rotation_prop.add_keyframe(end_time, start)


def random_rot_shake(rotation_prop, min_angle, max_angle, start_time, end_time, n_frames):
    frame_time = (end_time - start_time) / n_frames
    if not rotation_prop.animated:
        start = rotation_prop.value
    else:
        start = rotation_prop.keyframes[-1].start
    delta = max_angle - min_angle

    first = 0
    rotation_prop.add_keyframe(start_time, start)
    for i in range(1, n_frames):
        a = start + min_angle + (random.random() * delta)
        rotation_prop.add_keyframe(start_time + i * frame_time, a)
    rotation_prop.add_keyframe(end_time, start)


def rot_shake(rotation_prop, angles, start_time, end_time, n_frames):
    frame_time = (end_time - start_time) / n_frames
    if not rotation_prop.animated:
        start = rotation_prop.value
    else:
        start = rotation_prop.keyframes[-1].start

    first = 0
    for i in range(0, n_frames):
        a = angles[i % len(angles)] * math.sin(i/n_frames * math.pi)
        rotation_prop.add_keyframe(start_time + i * frame_time, start + a)
    rotation_prop.add_keyframe(end_time, start)
