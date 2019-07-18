import json
import gzip
import codecs
import sys
from xml.dom import minidom
from xml.etree import ElementTree

from .objects.base import TgsObject, Tgs
from .objects.properties import MultiDimensional, Value, ShapeProperty
from .parsers.svg.builder import to_svg
from .parsers.sif.builder import to_sif


def export_lottie(animation, fp, **kw):
    json.dump(animation.to_dict(), fp, **kw)


def export_tgs(animation, file):
    with gzip.open(file, "wb") as gzfile:
        export_lottie(animation, codecs.getwriter('utf-8')(gzfile))


def lottie_display_html_pre(width=512, height=512):
    return '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <style>
        html, body { width: 100%%; height: 100%%; margin: 0; }
        body { display: flex; }
        #bodymovin { width: %spx; height: %spx; margin: auto;
            background-color: white;
            background-size: 64px 64px;
            background-image:
                linear-gradient(to right, rgba(0, 0, 0, .3) 50%%, transparent 50%%),
                linear-gradient(to bottom, rgba(0, 0, 0, .3) 50%%, transparent 50%%),
                linear-gradient(to bottom, white 50%%, transparent 50%%),
                linear-gradient(to right, transparent 50%%, rgba(0, 0, 0, .5) 50%%);
        }
    </style>
     <script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.5.3/lottie.js"></script>
</head>
<body>

<div id="bodymovin"></div>

<script>
    var animData = {
        container: document.getElementById('bodymovin'),
        renderer: 'svg',
        loop: true,
        autoplay: true,
''' % (width, height)


def lottie_display_html_post():
    return '''
    };
    var anim = bodymovin.loadAnimation(animData);
</script>
</body>
</html>'''


def export_embedded_html(animation, fp):
    if isinstance(fp, str):
        fp = open(fp, "w")
    fp.write(lottie_display_html_pre(animation.width, animation.height))
    fp.write("animationData: ")
    export_lottie(animation, fp, indent=4)
    fp.write(lottie_display_html_post())


def export_linked_html(fp, path):
    if isinstance(fp, str):
        fp = open(fp, "w")
    fp.write(lottie_display_html_pre(animation.width, animation.height))
    fp.write("path: %r" % path)
    fp.write(lottie_display_html_post())


def _prettyprint_scalar(tgs_object, out=sys.stdout):
    if isinstance(tgs_object, float) and tgs_object == round(tgs_object):
        tgs_object = int(tgs_object)
    return str(tgs_object)


def prettyprint(tgs_object, out=sys.stdout, indent="   ", _i=""):
    if isinstance(tgs_object, TgsObject):
        out.write(tgs_object.__class__.__name__)
        out.write('\n')
        _i += indent
        maxk = max(map(lambda x: len(x.name), tgs_object._props))
        for k in tgs_object._props:
            out.write(_i)
            out.write(k.name.ljust(maxk))
            out.write(' : ')
            prettyprint(k.get(tgs_object), out, indent, _i)
    elif isinstance(tgs_object, (list, tuple)):
        if not tgs_object or (not isinstance(tgs_object[0], Tgs) and len(tgs_object) < 16):
            out.write("[")
            out.write(", ".join(map(_prettyprint_scalar, tgs_object)))
            out.write("]\n")
        else:
            out.write("[\n")
            for k in tgs_object:
                out.write(_i + indent)
                prettyprint(k, out, indent, _i + indent)
            out.write(_i)
            out.write(']\n')
    else:
        out.write(_prettyprint_scalar(tgs_object, out))
        out.write('\n')


def _prettyprint_summary_printable(obj):
    if isinstance(obj, TgsObject):
        return not isinstance(obj, (MultiDimensional, Value, ShapeProperty))
    return obj and isinstance(obj, (list, tuple)) and isinstance(obj[0], TgsObject)


def prettyprint_summary(tgs_object, out=sys.stdout, indent="   ", _i=""):
    if isinstance(tgs_object, TgsObject):
        out.write(tgs_object.__class__.__name__)
        name = getattr(tgs_object, "name", None)
        if name:
            out.write(" %r" % name)
        out.write('\n')
        _i += indent
        for k in tgs_object._props:
            val = k.get(tgs_object)
            if _prettyprint_summary_printable(val):
                out.write(_i)
                out.write(k.name)
                out.write(' : ')
                prettyprint_summary(val, out, indent, _i)
    elif _prettyprint_summary_printable(tgs_object):
            out.write("[\n")
            for k in tgs_object:
                out.write(_i + indent)
                prettyprint_summary(k, out, indent, _i + indent)
            out.write(_i)
            out.write(']\n')


def multiexport(animation, basename, lottie_json=True, lottie_html=True, tgs=True, embedded_html=True):
    if lottie_json:
        with open(basename+".json", "w") as lottieout:
            export_lottie(animation, lottieout, sort_keys=True, indent=4)

    if lottie_html:
        if embedded_html:
            export_embedded_html(animation, basename+".html")
        else:
            export_linked_html(basename+".html", basename+".json")

    if tgs:
        with open(basename+".tgs", "wb") as tgsout:
            export_tgs(animation, tgsout)


def _print_ugly_xml(dom, fp):
    return dom.write(fp, "utf-8", True)


def _print_pretty_xml(dom, fp):
    xmlstr = minidom.parseString(ElementTree.tostring(dom.getroot())).toprettyxml(indent="   ")
    if isinstance(fp, str):
        fp = open(fp, "w")
    fp.write(xmlstr)


def export_svg(animation, fp, time=0, pretty=True):
    _print_xml = _print_pretty_xml if pretty else _print_ugly_xml
    _print_xml(to_svg(animation, time), fp)


def export_sif(animation, fp, pretty=True):
    dom = to_sif(animation)
    if isinstance(fp, str):
        fp = open(fp, "w")
    dom.writexml(fp, "", "  " if pretty else "", "\n" if pretty else "")
