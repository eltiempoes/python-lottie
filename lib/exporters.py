import json
import gzip
import codecs
import sys

from . import tgs


def export_lottie(animation, fp):
    json.dump(animation.to_dict(), fp)


def export_tgs(animation, file):
    with gzip.open(file, "wb") as gzfile:
        export_lottie(animation, codecs.getwriter('utf-8')(gzfile))


def lottie_display_html(rel_lottie_filename):
    return '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <style>
        html, body { width: 100%%; height: 100%%; background-color: #ccc; margin: 0; }
        #bodymovin { width: 100%%; height: 100%%; background-color :#333; }
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
        path: %r,
    };
    var anim = bodymovin.loadAnimation(animData);
</script>
</body>
</html>''' % rel_lottie_filename


def prettyprint(tgs_object, out=sys.stdout, indent="   ", _i=""):
    if isinstance(tgs_object, tgs.TgsObject):
        out.write(tgs_object.__class__.__name__)
        out.write('\n')
        _i += indent
        maxk = max(map(len, tgs_object._props.keys()))
        for k in tgs_object._props.keys():
            out.write(_i)
            out.write(k.ljust(maxk))
            out.write(' : ')
            prettyprint(getattr(tgs_object, k), out, indent, _i)
    elif isinstance(tgs_object, (list, tuple)):
        if not tgs_object or (not isinstance(tgs_object[0], tgs.Tgs) and len(tgs_object) < 16):
            out.write("[")
            out.write(", ".join(map(str, tgs_object)))
            out.write("]\n")
        else:
            out.write("[\n")
            for k in tgs_object:
                out.write(_i + indent)
                prettyprint(k, out, indent, _i + indent)
            out.write(_i)
            out.write(']\n')
    else:
        out.write(str(tgs_object))
        out.write('\n')
