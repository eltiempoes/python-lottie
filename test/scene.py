import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import tgs, exporters


an = tgs.Animation()

layer = tgs.ShapeLayer()
an.out_point = layer.out_point = 59
an.layers.append(layer)

circle = layer.add_shape(tgs.Ellipse())
circle.size.value = [153, 100]
#circle.position.value = [222, 206]
circle.position = tgs.MultiDimensionalKeyframed()
circle.position.keyframes = [
    tgs.OffsetKeyframe(0, [222, 0], [222, 206]),
    tgs.OffsetKeyframe(10, [222, 206], [422, 206]),
    tgs.OffsetKeyframe(30, [422, 206]),
]

fill = layer.add_shape(tgs.Fill())
fill.color.value = [1, 0, 0]

exporters.export_lottie(an, open("/tmp/out.json", "w"))
open("/tmp/out.html", "w").write(exporters.lottie_display_html("/tmp/out.json"))
exporters.export_tgs(an, open("/tmp/out.tgs", "wb"))
