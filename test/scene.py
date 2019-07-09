import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.tgs import exporters
from lib.tgs import objects
from lib.tgs.utils.linediff import difflines


an = objects.Animation()

layer = objects.ShapeLayer()
an.out_point = layer.out_point = 59
an.layers.append(layer)

circle = layer.add_shape(objects.Ellipse())
circle.size.value = [169, 169]
#circle.position.value = [222, 206]
circle.position.add_keyframe( 0, [256, 256-128])
circle.position.add_keyframe(10, [256, 256])
circle.position.add_keyframe(30, [256+128, 256])

fill = layer.add_shape(objects.Fill())
fill.color.value = [1, 0, 0, 1]
#fill.opacity.value = 100
#fill.opacity.add_keyframe(0, 100)
fill.opacity.add_keyframe(10, 100)
fill.opacity.add_keyframe(30, 0)
fill.opacity.keyframes[-1].start = None

exporters.export_lottie(an, open("/tmp/out.json", "w"))
open("/tmp/out.html", "w").write(exporters.lottie_display_html("/tmp/out.json"))
exporters.export_tgs(an, open("/tmp/out.tgs", "wb"))


import json
latest = None
latest_stat = 0
for entry in os.scandir(os.path.dirname(os.path.abspath(__file__))):
    if entry.name.endswith(".json"):
        stat = entry.stat().st_mtime_ns
        if stat > latest_stat:
            latest_stat = stat
            latest = entry.path
from shutil import copyfile
copyfile(latest, "/tmp/source.json")
open("/tmp/source.html", "w").write(exporters.lottie_display_html("/tmp/source.json"))

