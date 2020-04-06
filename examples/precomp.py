#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs.utils import script
from tgs import objects
from tgs import NVector, Color


an = objects.Animation(80)

precomp = objects.Precomp("myid", an)
an.assets.append(precomp)

# Define stuff in the precomposition (a circle moving left to right)
layer = objects.ShapeLayer()
precomp.add_layer(layer)

circle = layer.add_shape(objects.Ellipse())
circle.size.value = NVector(100, 100)
circle.position.add_keyframe(0, NVector(-50, 50))
circle.position.add_keyframe(60, NVector(512+50, 50))

fill = layer.add_shape(objects.Fill())
fill.color.add_keyframe(0, Color(1, 1, 0))
fill.color.add_keyframe(60, Color(1, 0, 0))


# plays the precomp as it is
pcl0 = an.add_layer(objects.PreCompLayer("myid"))

# plays the precomp, offset in time by 20 frames and in space by 100 pixels
pcl1 = an.add_layer(objects.PreCompLayer("myid"))
pcl1.start_time = 20
pcl1.transform.position.value = NVector(0, 100)

# playes the composition, but starts it with negative time, so it's farther ahead
pcl2 = an.add_layer(objects.PreCompLayer("myid"))
pcl2.start_time = -20
pcl2.transform.position.value = NVector(0, 200)

# another instance on the same position as the one before
# but with a different time offset, to make the animation loop
pcl3 = an.add_layer(objects.PreCompLayer("myid"))
pcl3.start_time = 60
pcl3.transform.position.value = NVector(0, 200)

script.script_main(an)

