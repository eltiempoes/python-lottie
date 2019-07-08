import json
import gzip
import codecs


def export_lottie(animation, fp):
    json.dump(animation.to_dict(), fp)


def export_tgs(animation, file):
    with gzip.open(file, "wb") as gzfile:
        export_lottie(animation, codecs.getwriter('utf-8')(gzfile))


def lottie_display_html(rel_lottie_filename):
    return '''
<!DOCTYPE html>
<html style="width: 100%;height: 100%">
<head>
     <script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.5.3/lottie.js"></script>
</head>
<body style="background-color:#ccc; margin: 0px;height: 100%; font-family: sans-serif;font-size: 10px">

<div style="width:100%;height:100%;background-color:#333;" id="bodymovin"></div>

<script>
    var animData = {
        container: document.getElementById('bodymovin'),
        renderer: 'svg',
        loop: true,
        autoplay: true,
        path:%r
    };
    var anim = bodymovin.loadAnimation(animData);
</script>
</body>
</html>''' % rel_lottie_filename

