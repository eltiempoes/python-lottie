import random


def shake(transformable, x_radius, y_radius, start_time, end_time, n_frames):
    frame_time = (end_time - start_time) / n_frames
    if not transformable.position.animated:
        start_x, start_y = transformable.position.value
    else:
        start_x, start_y = transformable.position.keyframes[-1].start

    for i in range(n_frames):
        x = start_x + (random.random() * 2 - 1) * x_radius
        y = start_y + (random.random() * 2 - 1) * y_radius
        transformable.position.add_keyframe(start_time + i * frame_time, [x, y])
