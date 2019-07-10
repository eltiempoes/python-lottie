import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects
from tgs.utils.linediff import difflines
from tgs.parsers.svg import parse_svg_file


an = parse_svg_file(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "examples",
    "blep.svg"
))

#an = parse_svg_file("/tmp/foo.svg")

layer = an.find("durg")
layer.transform.anchor_point.value = [256, 256]
layer.transform.position.value = [256, 256]
layer.transform.rotation.add_keyframe(0, 0)
layer.transform.rotation.add_keyframe(30, 180)
layer.transform.rotation.add_keyframe(60, 360)


exporters.multiexport(an, "/tmp/out")

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

