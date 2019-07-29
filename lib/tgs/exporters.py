import io
import sys
import json
import gzip
import codecs
from xml.dom import minidom
from xml.etree import ElementTree

from .objects.base import TgsObject, Tgs
from .objects.properties import MultiDimensional, Value, ShapeProperty
from .parsers.svg.builder import to_svg
from .parsers.sif.builder import to_sif


def export_lottie(animation, fp, **kw):
    if isinstance(fp, str):
        fp = open(fp, "w")
    json.dump(animation.to_dict(), fp, **kw)


def export_tgs(animation, file):
    with gzip.open(file, "wb") as gzfile:
        export_lottie(animation, codecs.getwriter('utf-8')(gzfile))


class HtmlOutput:
    def __init__(self, animation, file):
        self.animation = animation
        self.file = file

    def style(self):
        self.file.write("""
    <style>
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
    """ % (self.animation.width, self.animation.height))

    def body_pre(self):
        self.file.write("""
<div id="bodymovin"></div>

<script>
    var animData = {
        container: document.getElementById('bodymovin'),
        renderer: 'svg',
        loop: true,
        autoplay: true,
        """)

    def body_embedded(self):
        self.file.write("animationData: ")
        export_lottie(self.animation, self.file, indent=4)

    def body_post(self):
        self.file.write("""
    };
    var anim = bodymovin.loadAnimation(animData);
</script>""")

    def html_begin(self):
        self.file.write("""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <style>
        html, body { width: 100%; height: 100%; margin: 0; }
        body { display: flex; }
    </style>""")
        self.style()
        self.file.write("</head><body>")

    def html_end(self):
        self.file.write("</body></html>")


def export_embedded_html(animation, fp):
    if isinstance(fp, str):
        fp = open(fp, "w")
    out = HtmlOutput(animation, fp)
    out.html_begin()
    out.body_pre()
    out.body_embedded()
    out.body_post()
    out.html_end()


def export_linked_html(animation, fp, path):
    if isinstance(fp, str):
        fp = open(fp, "w")
    out = HtmlOutput(animation, fp)
    out.html_begin()
    out.body_pre()
    fp.write("path: %r" % path)
    out.body_post()
    out.html_end()


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


def _print_ugly_xml(dom, fp):
    return dom.write(fp, "utf-8", True)


def _print_pretty_xml(dom, fp):
    xmlstr = minidom.parseString(ElementTree.tostring(dom.getroot())).toprettyxml(indent="   ")
    if isinstance(fp, str):
        fp = open(fp, "w")
    fp.write(xmlstr)


def export_svg(animation, fp, frame=0, pretty=True):
    _print_xml = _print_pretty_xml if pretty else _print_ugly_xml
    _print_xml(to_svg(animation, frame), fp)


def export_sif(animation, fp, pretty=True):
    dom = to_sif(animation)
    if isinstance(fp, str):
        fp = open(fp, "w")
    dom.writexml(fp, "", "  " if pretty else "", "\n" if pretty else "")


try:
    import cairosvg
    has_cairo = True

    def _export_cairo(func, animation, fp, frame, dpi):
        intermediate = io.StringIO()
        export_svg(animation, intermediate, frame)
        intermediate.seek(0)
        func(file_obj=intermediate, write_to=fp, dpi=dpi)

    def export_png(animation, fp, frame=0, dpi=96):
        _export_cairo(cairosvg.svg2png, animation, fp, frame, dpi)

    def export_pdf(animation, fp, frame=0, dpi=96):
        _export_cairo(cairosvg.svg2pdf, animation, fp, frame, dpi)

    def export_ps(animation, fp, frame=0, dpi=96):
        _export_cairo(cairosvg.svg2ps, animation, fp, frame, dpi)

    try:
        from PIL import Image
        has_gif = True

        def _png_gif_prepare(image):
            alpha = image.split()[3]
            image = image.convert('P', palette=Image.ADAPTIVE, colors=255)
            mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
            image.paste(255, mask)
            return image

        def export_gif(animation, fp, dpi=96, skip_frames=5):
            """
            Gif export

            Note that it's a bit slow.
            """
            start = animation.in_point
            end = animation.out_point
            frames = []
            for i in range(start, end+1, skip_frames):
                file = io.BytesIO()
                export_png(animation, file, i, dpi)
                file.seek(0)
                frames.append(_png_gif_prepare(Image.open(file)))

            duration = 1000 / animation.frame_rate
            frames[0].save(
                fp,
                format='GIF',
                append_images=frames[1:],
                save_all=True,
                duration=duration,
                loop=0,
                transparency=255,
                disposal=2,
            )

    except ImportError:
        has_gif = False

except ImportError:
    has_cairo = False
    has_gif = False
