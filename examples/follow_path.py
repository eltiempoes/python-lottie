import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.utils.animation import follow_path
from tgs import NVector

an = objects.Animation(180)

layer = objects.ShapeLayer()
an.add_layer(layer)

group = layer.add_shape(objects.Group())
ball = group.add_shape(objects.Ellipse())
ball.size.value = NVector(10, 10)
group.add_shape(objects.Fill(NVector(0, 1, 0)))

group = layer.add_shape(objects.Group())
bez = group.add_shape(objects.Shape())
bez.vertices.value.add_point(NVector(256, 128), NVector(0, 0), NVector(64, 64))
bez.vertices.value.add_point(NVector(256, 256), NVector(-64, -64), NVector(-64, 64))
bez.vertices.value.add_point(NVector(256, 256+120), NVector(0, 0), NVector(0, 0))
group.add_shape(objects.Stroke(NVector(1, 0, 0), 10))

follow_path(ball.position, bez.vertices.value, 0, 90, 30)
follow_path(ball.position, bez.vertices.value, 90, 180, 30, True)


exporters.multiexport(an, "/tmp/follow_path")
