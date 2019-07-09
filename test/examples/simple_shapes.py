import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "lib"
))
from tgs import exporters
from tgs import objects


an = objects.Animation()

layer = objects.ShapeLayer()
an.out_point = layer.out_point = 59
an.layers.append(layer)

circle = layer.add_shape(objects.Ellipse())
circle.size.value = [100, 100]
circle.position.value = [200, 100]

star = layer.add_shape(objects.Star())
star.inner_radius.value = 10
star.outer_radius.value = 50
star.position.value = [300, 100]

rect = layer.add_shape(objects.Rect())
rect.size.value = [100, 100]
rect.position.value = [100, 100]


fill = layer.add_shape(objects.Fill([1, 1, 0]))
stroke = layer.add_shape(objects.Stroke([0, 0, 0], 5))



exporters.export_lottie(an, open("/tmp/out.json", "w"), indent=4)
open("/tmp/out.html", "w").write(exporters.lottie_display_html("/tmp/out.json"))
exporters.export_tgs(an, open("/tmp/out.tgs", "wb"))
