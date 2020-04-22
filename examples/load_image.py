#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.utils import script
from tgs import objects
from tgs import Point, Color


image_filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "blep.png"
)

last_frame = 60
an = objects.Animation(last_frame)

image = objects.assets.Image().load(image_filename)
an.assets.append(image)

an.add_layer(objects.ImageLayer(image.id))

script.script_main(an)
