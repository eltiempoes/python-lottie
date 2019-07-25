import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs import Point, Color


image_filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "blep.png"
)

last_frame = 60
an = objects.Animation(last_frame)

image = objects.Image().load(image_filename)
an.assets.append(image)

an.add_layer(objects.ImageLayer(image.id))

exporters.multiexport(an, "/tmp/load_image")
