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

group = layer.add_shape(objects.Group())

circle = group.add_shape(objects.Ellipse())
circle.size.value = [100, 100]
circle.position.value = [200, 100]
#circle.position.add_keyframe( 0, [256, 256-128])
#circle.position.add_keyframe(10, [256, 256])
#circle.position.add_keyframe(30, [256+128, 256])

group.add_shape(objects.Fill([1, 0, 0]))
group.add_shape(objects.Stroke([0, 0, 0], 2))


group = layer.add_shape(objects.Group())

round = group.add_shape(objects.Star())
round.inner_radius.value = 10
round.outer_radius.value = 50
round.position.value = [300, 100]


rect = group.add_shape(objects.Rect())
rect.size.value = [100, 100]
rect.position.value = [100, 200]


#group.transform.position.value = [200, 200]
shape = group.add_shape(objects.Shape())
heart = objects.Bezier()
heart.add_point([50, 20], [50, -20], [-50, -20])
heart.add_smooth_point([0, 50], [-5, -10])
heart.add_smooth_point([50, 100], [-10, 0])
heart.add_smooth_point([100, 50], [-5, 10])
heart.closed = True
circbez = (
    objects.Bezier()
    .add_smooth_point([50, 0], [20, 0])
    .add_smooth_point([0, 50], [0, -20])
    .add_smooth_point([50, 100], [-20, 0])
    .add_smooth_point([100, 50], [0, 20])
    .close()
)

shape.vertices.add_keyframe(0, heart)
shape.vertices.add_keyframe(30, circbez)
shape.vertices.add_keyframe(59, heart)
#shape.vertices.value = heart


fill = group.add_shape(objects.Fill())
fill.color.value = [1, 1, 0]
#fill.color.add_keyframe(0, [1, 0, 0])
#fill.color.add_keyframe(10, [1, 1, 0])
#fill.color.add_keyframe(30, [1, 1, 1])
fill.opacity.value = 100
#fill.opacity.add_keyframe(10, 100)
#fill.opacity.add_keyframe(30, 0)

stroke = group.add_shape(objects.Stroke([0, 0, 0], 5))
#grad = group.add_shape(objects.GradientStroke())
#grad.end_point.value = [200, 0]
##grad.colors.set_colors([[1, 0, 0], [1, 1, 0]])
#grad.colors.add_keyframe(0, [[1, 0, 0], [1, 1, 0]])
#grad.colors.add_keyframe(10, [[1, 1, 0], [0, 1, 0]])
#grad.colors.add_keyframe(30, [[1, 0, 1], [0, 0, 1]])
#grad.colors.add_keyframe(59, [[1, 0, 0], [1, 1, 0]])
#grad.colors.count = 2
#grad.stroke_width.value = 10



exporters.export_lottie(an, open("/tmp/out.json", "w"), indent=4)
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

