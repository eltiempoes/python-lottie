#!/usr/bin/env python3
import sys
import os
import random
import math

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.utils import script
from lottie import objects
from lottie.objects import easing
from lottie import Point, Color, Size, PolarVector
from lottie.utils import animation as anutils


last_frame = 120
an = objects.Animation(last_frame)
layer = objects.ShapeLayer()
an.insert_layer(0, layer)

color1 = Color(1, 0.98, 0.282)
color2 = Color(1, 0.341, 0.016)
color3 = Color(0.698, 0.114, 0.02)
particle_start = Point(256, 256)
particle_size = Point(20, 20)
particle_end = Point(256, -particle_size.y*2)
start_len_min = 0
start_len_max = 128
opacity_start = 100
opacity_end = 20


def particle():
    g = layer.add_shape(objects.Group())
    b = g.add_shape(objects.Ellipse())
    fill = objects.Fill()
    g.add_shape(fill)
    t = random.random()

    if t < 1/2:
        lf = t * 2
        fill.color.add_keyframe(0, color1.lerp(color2, lf))
        fill.color.add_keyframe(last_frame*t, color2)
        fill.color.add_keyframe((1 - t) * last_frame, color3, easing.Jump())
        fill.color.add_keyframe((1 - t) * last_frame+1, color1)
        fill.color.add_keyframe(last_frame, color1.lerp(color2, lf))
    else:
        lf = (t-0.5) * 2
        tf = (1-lf)/2
        fill.color.add_keyframe(0, color2.lerp(color3, lf))
        fill.color.add_keyframe(last_frame*tf, color3, easing.Jump())
        fill.color.add_keyframe(last_frame*tf+1, color1)
        fill.color.add_keyframe((.5 + tf) * last_frame, color2)
        fill.color.add_keyframe(last_frame, color2.lerp(color3, lf))

    fill.opacity.add_keyframe(0, opacity_start + (opacity_end - opacity_start) * t)
    fill.opacity.add_keyframe((1 - t) * last_frame, opacity_end)
    fill.opacity.add_keyframe((1 - t) * last_frame+1, opacity_start)
    fill.opacity.add_keyframe(last_frame, opacity_start + (opacity_end - opacity_start) * t)

    bezier = objects.Bezier()
    outp = PolarVector(random.uniform(start_len_min, start_len_max), random.random() * math.pi)
    inp = Point(0,  random.random() * (particle_end.y - particle_start.y) / 3)
    bezier.add_point(particle_start, outp=outp)
    bezier.add_point(particle_end, outp)

    b.size.value = particle_size
    anutils.follow_path(b.position, bezier, 0, last_frame, 10, start_t=t)

for i in range(100):
    particle()

script.script_main(an)

