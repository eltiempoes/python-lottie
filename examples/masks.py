
import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.parsers.svg import parse_svg_file
from tgs import Point, Color


an = parse_svg_file(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "blep.svg"
))


maskshape = objects.Star()
maskshape.inner_radius.value = 100
maskshape.outer_radius.value = 200
maskshape.rotation.value = 180
maskshape.position.value = Point(256, 256)
#maskshape.size.value = Point(256, 256)
maskbez = maskshape.to_bezier()

mask = objects.Mask()
an.layers[0].masks = [mask]
mask.shape.value = maskbez.shape.value

g = an.layers[0].add_shape(objects.Group())
r = g.add_shape(objects.Rect())
r.position.value = Point(256, 256)
r.size.value = Point(512, 512)
g.add_shape(objects.Fill(Color(1, 1, 1)))


exporters.multiexport(an, "/tmp/masks")
