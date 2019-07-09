import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.utils.linediff import difflines


an = objects.Animation()

layer = objects.ShapeLayer()
an.out_point = layer.out_point = 60
an.layers.append(layer)


heart = objects.Bezier()
heart.add_point([50, 20], [50, -20], [-50, -20])
heart.add_smooth_point([0, 50], [-5, -10])
heart.add_smooth_point([50, 100], [-10, 0])
heart.add_smooth_point([100, 50], [-5, 10])
heart.closed = True
antiheart = (
    objects.Bezier()
    .add_smooth_point([50, 0], [10, 0])
    .add_smooth_point([0, 50], [0, -20])
    .add_point([50, 80], [-50, 20], [50, 20])
    .add_smooth_point([100, 50], [0, 20])
    .close()
)

g1 = layer.add_shape(objects.Group())
shape = g1.add_shape(objects.Shape())
#shape.vertices.value = heart
shape.vertices.add_keyframe(0, heart)
shape.vertices.add_keyframe(30, antiheart)
shape.vertices.add_keyframe(59, heart)


fill = g1.add_shape(objects.Fill([1, 0, 0, 1]))



layer.index = 1

exporters.export_lottie(an, open("/tmp/out.json", "w"), indent=4)
open("/tmp/out.html", "w").write(exporters.lottie_display_html("/tmp/out.json"))
exporters.export_tgs(an, open("/tmp/out.tgs", "wb"))

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

