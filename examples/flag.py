import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.utils import animation as anutils

an = objects.Animation(60)

layer = objects.ShapeLayer()
an.add_layer(layer)
g = layer.add_shape(objects.Group())

for i in range(0, 512+1, 16):
    b = g.add_shape(objects.Ellipse())
    b.size.value = [16, 16]
    b.position.value = [i, 100]
    anutils.sine_displace(b.position, 300, 50, 0, 60, 10, 1, 45)


bez = g.add_shape(objects.Shape())
bez.vertices.value.add_smooth_point([256, 200], [50, 0])
bez.vertices.value.add_smooth_point([156, 300], [0, -50])
bez.vertices.value.add_smooth_point([256, 400], [-50, 0])
bez.vertices.value.add_smooth_point([356, 300], [0, 50])
bez.vertices.value.close()
bez.vertices.value.split_self_chunks(8)
anutils.sine_displace_bezier(bez.vertices, 300, 50, 0, 60, 10, 1, 45)

g.add_shape(objects.Fill([1, 1, 0]))


g = layer.add_shape(objects.Group())
bez = g.add_shape(objects.Shape())
g.add_shape(objects.Stroke([1, 0, 0], 5))
g.add_shape(objects.Fill([0, 0, 1]))
for i in range(9):
    bez.vertices.value.add_point([i*64, 160], [-20, 0], [20, 0])

for i in range(9):
    bez.vertices.value.add_point([512-i*64, 420], [20, 0], [-20, 0])
bez.vertices.value.close()
anutils.sine_displace_bezier(bez.vertices, 300, 50, 0, 60, 10, 1, 45)


exporters.multiexport(an, "/tmp/flag")


