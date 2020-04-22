#!/usr/bin/env python3
import sys
import os
import math
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.utils import script
from lottie import objects
from lottie.utils import animation as anutils
from lottie import Point, Color
from lottie.utils import ik


an = objects.Animation(180)

layer = objects.ShapeLayer()
an.add_layer(layer)

g = layer.add_shape(objects.Group())
b1 = g.add_shape(objects.Ellipse())
b1.size.value = Point(20, 20)
g.add_shape(objects.Fill(Color(1, 1, 0)))

g = layer.add_shape(objects.Group())
b2 = g.add_shape(objects.Ellipse())
b2.size.value = Point(20, 20)
g.add_shape(objects.Fill(Color(0, 1, 0)))


for i in range(an.out_point):
    t = i / (an.out_point-1)
    p1 = Point(math.cos(t*math.pi*2)/2+1, math.sin(t*math.pi*2)/2+1) * 256
    b1.position.add_keyframe(i, p1)

    p2 = Point(math.sin(2*t*math.pi*2)/2+1, -math.cos(t*math.pi*2)/2+1) * 256
    b2.position.add_keyframe(i, p2)


def chain_bezier(chain):
    b = objects.Bezier()
    for seg in chain.joints:
        b.add_point(seg)
    return b


g = layer.add_shape(objects.Group())
s = g.add_shape(objects.Path())
g.add_shape(objects.Stroke(Color(1, 0, 0), 5))

chain = ik.Chain(Point(0, 0))
chain.add_joint(Point(50, 0))
chain.add_joint(Point(150, 0))
chain.add_joint(Point(350, 0))
chain.add_joint(Point(400, 0))
#chain.add_joint(Point(500, 0))


octmaster = ik.Chain(Point(512, 512), True)
octmaster.add_joint(Point(450, 450))
octmaster.add_joint(Point(400, 400))
octmaster.add_joint(Point(450, 450))
octmaster.add_joint(Point(512, 512))

oct = ik.Octopus(octmaster)
ch1 = oct.add_chain("ch1")
ch1.add_joint(Point(412, 512))
ch1.add_joint(Point(312, 512))
ch2 = oct.add_chain("ch2")
ch2.add_joint(Point(512, 412))
ch2.add_joint(Point(512, 312))


g = layer.add_shape(objects.Group())
octshapes = {
    n: g.add_shape(objects.Path())
    for n in oct.chains.keys()
}
g.add_shape(objects.Stroke(Color(0, 0, 1), 5))


for i in range(an.out_point):
    t = i / (an.out_point-1)
    p1 = Point(math.cos(t*math.pi*2)/2+1, math.sin(t*math.pi*2)/2+1) * 256
    p2 = Point(math.sin(2*t*math.pi*2)/2+1, -math.cos(t*math.pi*2)/2+1) * 256
    chain.reach(p1)
    s.shape.add_keyframe(i, chain_bezier(chain))

    oct.reach({"ch1": p1, "ch2": p2})
    for name, ochain in oct.chains.items():
        octshapes[name].shape.add_keyframe(i, chain_bezier(ochain))

script.script_main(an)
