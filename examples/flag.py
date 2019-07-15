import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.utils import animation as anutils
from tgs import NVector

an = objects.Animation(60)

layer = objects.ShapeLayer()
an.add_layer(layer)
g = layer.add_shape(objects.Group())

displacer = anutils.SineDisplacer(300, 50, 0, 60, 10, 1, 45)

for i in range(0, 512+1, 16):
    b = g.add_shape(objects.Ellipse())
    b.size.value = NVector(16, 16)
    b.position.value = NVector(i, 100)
    displacer.animate_point(b.position)


bez = g.add_shape(objects.Shape())
bez.vertices.value.add_smooth_point(NVector(256, 200), NVector(50, 0))
bez.vertices.value.add_smooth_point(NVector(156, 300), NVector(0, -50))
bez.vertices.value.add_smooth_point(NVector(256, 400), NVector(-50, 0))
bez.vertices.value.add_smooth_point(NVector(356, 300), NVector(0, 50))
bez.vertices.value.close()
bez.vertices.value.split_self_chunks(8)
displacer.animate_bezier(bez.vertices)

g.add_shape(objects.Fill(NVector(1, 1, 0)))


g = layer.add_shape(objects.Group())
bez = g.add_shape(objects.Shape())
g.add_shape(objects.Stroke(NVector(1, 0, 0), 5))
g.add_shape(objects.Fill(NVector(0, 0, 1)))
for i in range(9):
    bez.vertices.value.add_point(NVector(i*64, 160), NVector(-20, 0), NVector(20, 0))

for i in range(9):
    bez.vertices.value.add_point(NVector(512-i*64, 420), NVector(20, 0), NVector(-20, 0))
bez.vertices.value.close()
displacer.animate_bezier(bez.vertices)


exporters.multiexport(an, "/tmp/flag")


