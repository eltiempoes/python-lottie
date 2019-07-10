import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.utils.linediff import difflines
from tgs.parsers.svg import parse_svg_file


#an = parse_svg_file(os.path.join(
    #os.path.dirname(os.path.abspath(__file__)),
    #"examples",
    #"blep.svg"
#))

an = objects.Animation(60)


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


layer = objects.ShapeLayer()
an.add_layer(layer)

circle = layer.add_shape(objects.Ellipse())
circle.size.value = [100, 100]
circle.position.value = [256, 256]
shake(circle, 10, 15, 0, 60, 25)


fill = layer.add_shape(objects.Fill([1, 1, 0]))

exporters.multiexport(an, "/tmp/out")

#import json
#latest = None
#latest_stat = 0
#for entry in os.scandir(os.path.dirname(os.path.abspath(__file__))):
    #if entry.name.endswith(".json"):
        #stat = entry.stat().st_mtime_ns
        #if stat > latest_stat:
            #latest_stat = stat
            #latest = entry.path
#from shutil import copyfile
#copyfile(latest, "/tmp/source.json")
#open("/tmp/source.html", "w").write(exporters.lottie_display_html("/tmp/source.json"))

