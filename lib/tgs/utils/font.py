import os
import subprocess
import fontTools.pens.basePen
import fontTools.ttLib
import enum
import math
from xml.etree import ElementTree
from ..nvector import NVector
from ..objects.bezier import Bezier, BezierPoint
from ..objects.shapes import Path, Group, Fill, Stroke
from ..objects.text import TextJustify
from ..objects.base import TgsProp, CustomObject


class BezierPen(fontTools.pens.basePen.BasePen):
    def __init__(self, glyphSet, offset=NVector(0, 0)):
        super().__init__(glyphSet)
        self.beziers = []
        self.current = Bezier()
        self.offset = offset

    def _point(self, pt):
        return self.offset + NVector(pt[0], -pt[1])

    def _moveTo(self, pt):
        self._endPath()

    def _endPath(self):
        if len(self.current.points):
            self.beziers.append(self.current)
        self.current = Bezier()

    def _closePath(self):
        self.current.close()
        self._endPath()

    def _lineTo(self, pt):
        if len(self.current.points) == 0:
            self.current.points.append(self._point(self._getCurrentPoint()))

        self.current.points.append(self._point(pt))

    def _curveToOne(self, pt1, pt2, pt3):
        if len(self.current.points) == 0:
            cp = self._point(self._getCurrentPoint())
            self.current.points.append(
                BezierPoint(
                    cp,
                    None,
                    self._point(pt1) - cp
                )

            )
        else:
            self.current.points[-1].out_tangent = self._point(pt1) - self.current.points[-1].vertex

        dest = self._point(pt3)
        self.current.points.append(
            BezierPoint(
                dest,
                self._point(pt2) - dest,
                None,
            )
        )


class SystemFont:
    def __init__(self, family):
        self.family = family
        self.files = {}
        self.styles = set()
        self._renderers = {}

    def add_file(self, styles, file):
        self.styles |= set(styles)
        self.files[tuple(sorted(styles))] = file

    def filename(self, styles):
        return self.files[self._key(styles)]

    def _key(self, styles):
        if isinstance(styles, str):
            return (styles,)
        return tuple(sorted(styles))

    def __getitem__(self, styles):
        key = self._key(styles)
        if key in self._renderers:
            return self._renderers[key]
        fr = FontRenderer(self.files[key])
        self._renderers[key] = fr
        return fr

    def __repr__(self):
        return "<SystemFont %s>" % self.family


class FontQuery:
    """!
    \see https://www.freedesktop.org/software/fontconfig/fontconfig-user.html#AEN21
         https://manpages.ubuntu.com/manpages/cosmic/man1/fc-pattern.1.html
    """
    def __init__(self, str=""):
        self._query = {}
        if isinstance(str, FontQuery):
            self._query = str._query.copy()
        elif str:
            chunks = str.split(":")
            family = chunks.pop(0)
            self._query = dict(
                chunk.split("=")
                for chunk in chunks
                if chunk
            )
            self.family(family)

    def family(self, name):
        self._query["family"] = name
        return self

    def weight(self, weight):
        self._query["weight"] = weight
        return self

    def css_weight(self, weight):
        """!
            Weight from CSS weight value.

            Weight is different between CSS and fontconfig
            This creates some interpolations to ensure known values are translated properly
            \see https://www.freedesktop.org/software/fontconfig/fontconfig-user.html#AEN178
                 https://developer.mozilla.org/en-US/docs/Web/CSS/font-weight#Common_weight_name_mapping
        """
        if weight < 200:
            v = max(0, weight - 100) / 100 * 40
        elif weight < 500:
            v = -weight**3 / 200000 + weight**2 * 11/2000 - weight * 17/10 + 200
        elif weight < 700:
            v = -weight**2 * 3/1000 + weight * 41/10 - 1200
        else:
            v = (weight - 700) / 200 * 10 + 200
        return self.weight(int(round(v)))

    def style(self, *styles):
        self._query["style"] = " ".join(styles)
        return self

    def charset(self, *hex_ranges):
        self._query["charset"] = " ".join(hex_ranges)
        return self

    def char(self, char):
        return self.charset("%x" % ord(char))

    def custom(self, property, value):
        self._query[property] = value
        return self

    def clone(self):
        return FontQuery(self)

    def __getitem__(self, key):
        return self._query.get(key, "")

    def __contains__(self, item):
        return item in self._query

    def get(self, key, default=None):
        return self._query.get(key, default)

    def __str__(self):
        return self._query.get("family", "") + ":" + ":".join(
            "%s=%s" % (p, v)
            for p, v in self._query.items()
            if p != "family"
        )

    def __repr__(self):
        return "<FontQuery %r>" % str(self)

    def weight_to_css(self):
        x = int(self["weight"])
        if x < 40:
            v = x / 40 * 100 + 100
        elif x < 100:
            v = x**3/300 - x**2 * 11/15 + x*167/3 - 3200/3
        elif x < 200:
            v = (2050 - 10 * math.sqrt(5) * math.sqrt(1205 - 6 * x)) / 3
        else:
            v = (x - 200) * 200 / 10 + 700
        return int(round(v))


class _SystemFontList:
    def __init__(self):
        self.fonts = None

    def _lazy_load(self):
        if self.fonts is None:
            self.load()

    def load(self):
        self.fonts = {}
        self.load_fc_list()

    def cmd(self, *a):
        p = subprocess.Popen(a, stdout=subprocess.PIPE)
        out, err = p.communicate()
        out = out.decode("utf-8").strip()
        return out, p.returncode

    def load_fc_list(self):
        out, returncode = self.cmd("fc-list", r'--format=%{file}\t%{family[0]}\t%{style[0]}\n')
        if returncode == 0:
            for line in out.splitlines():
                file, family, styles = line.split("\t")
                self._get(family).add_file(styles.split(" "), file)

    def best(self, query):
        """!
        Returns the renderer best matching the name
        """
        out, returncode = self.cmd("fc-match", r"--format=%{family}\t%{style}", str(query))
        if returncode == 0:
            fam, style = out.split("\t")
            return self[fam][style]

    def default(self):
        """!
        Returns the default fornt renderer
        """
        return self.best()

    def _get(self, family):
        self._lazy_load()
        if family in self.fonts:
            return self.fonts[family]
        font = SystemFont(family)
        self.fonts[family] = font
        return font

    def __getitem__(self, key):
        self._lazy_load()
        return self.fonts[key]

    def __iter__(self):
        self._lazy_load()
        return iter(self.fonts.values())

    def keys(self):
        self._lazy_load()
        return self.fonts.keys()

    def __contains__(self, item):
        self._lazy_load()
        return item in self.fonts


## Dictionary of system fonts
fonts = _SystemFontList()


def collect_kerning_pairs(font):
    gpos_table = font["GPOS"].table

    unique_kern_lookups = []
    for item in gpos_table.FeatureList.FeatureRecord:
        if item.FeatureTag == "kern":
            feature = item.Feature
            for featLookupItem in feature.LookupListIndex:
                if featLookupItem not in unique_kern_lookups:
                    unique_kern_lookups.append(featLookupItem)

    kerning_pairs = {}
    for kern_lookup_index in sorted(unique_kern_lookups):
        lookup = gpos_table.LookupList.Lookup[kern_lookup_index]
        if lookup.LookupType in {2, 9}:
            for pairPos in lookup.SubTable:
                if pairPos.LookupType == 9:  # extension table
                    if pairPos.ExtensionLookupType == 8:  # contextual
                        continue
                    elif pairPos.ExtensionLookupType == 2:
                        pairPos = pairPos.ExtSubTable

                if pairPos.Format != 1:
                    continue

                firstGlyphsList = pairPos.Coverage.glyphs
                for ps_index, _ in enumerate(pairPos.PairSet):
                    for pairValueRecordItem in pairPos.PairSet[ps_index].PairValueRecord:
                        secondGlyph = pairValueRecordItem.SecondGlyph
                        valueFormat = pairPos.ValueFormat1

                        if valueFormat == 5:  # RTL kerning
                            kernValue = "<%d 0 %d 0>" % (
                                pairValueRecordItem.Value1.XPlacement,
                                pairValueRecordItem.Value1.XAdvance)
                        elif valueFormat == 0:  # RTL pair with value <0 0 0 0>
                            kernValue = "<0 0 0 0>"
                        elif valueFormat == 4:  # LTR kerning
                            kernValue = pairValueRecordItem.Value1.XAdvance
                        else:
                            print(
                                "\tValueFormat1 = %d" % valueFormat,
                                file=sys.stdout)
                            continue  # skip the rest

                        kerning_pairs[(firstGlyphsList[ps_index], secondGlyph)] = kernValue
    return kerning_pairs


class FontRenderer:
    def __init__(self, filename):
        self.filename = filename
        self.font = fontTools.ttLib.TTFont(filename)
        self.glyphset = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap() or {}
        self._kerning = None

    def glyph_beziers(self, name, offset=NVector(0, 0)):
        pen = BezierPen(self.glyphset, offset)
        self.glyphset[name].draw(pen)
        return pen.beziers

    def glyph_shapes(self, name, offset=NVector(0, 0)):
        beziers = self.glyph_beziers(name, offset)
        return [
            Path(bez)
            for bez in beziers
        ]

    def glyph_group(self, name):
        group = Group()
        group.name = name
        group.shapes = self.glyph_shapes(name) + group.shapes
        return group

    def glyph_name(self, ch):
        return self.cmap.get(ord(ch)) or self.font._makeGlyphName(ord(ch))

    def render(self, text, size, pos=None, on_missing=None, use_kerning=True):
        """!
        Renders some text

        @param text         String to render
        @param size         Font size (in pizels)
        @param[in,out] pos  Text position
        @param on_missing   Callable on missing glyphs, called with:
        - Character as string
        - Font size
        - [in, out] Character position
        - Group shape

        @returns a Group shape, augmented with some extra attributes:
        - line_height   Line height

        """
        if use_kerning and self._kerning is None:
            self._kerning = collect_kerning_pairs(self.font)

        scale = size / self.font.tables["head"].unitsPerEm
        line_height = self.font.tables["head"].yMax * scale
        group = Group()
        group.name = text
        if pos is None:
            pos = NVector(0, 0)
        start_x = pos.x
        line = Group()
        group.add_shape(line)
        #group.transform.scale.value = NVector(100, 100) * scale
        for i, ch in enumerate(text):
            if ch == "\n":
                line.next_x = pos.x
                pos.x = start_x
                pos.y += line_height
                line = Group()
                group.add_shape(line)
                continue

            chname = self.glyph_name(ch)
            if chname in self.glyphset:
                glyphdata = self.glyphset[chname]
                next_x = pos.x + glyphdata.width * scale
                pos.x += glyphdata.lsb * scale
                glyph_shapes = self.glyph_shapes(chname, pos / scale)
                glyph_shape_group = line.add_shape(Group()) if len(glyph_shapes) > 1 else line

                for sh in glyph_shapes:
                    sh.shape.value.scale(scale)
                    glyph_shape_group.add_shape(sh)

                (glyph_shape_group if len(glyph_shapes) > 1 else sh).name = ch

                kerning = 0
                if use_kerning and i < len(text) - 1:
                    nextcname = text[i+1]
                    kerning = self.kerning(chname, nextcname)
                pos.x += (glyphdata.width - glyphdata.lsb + kerning) * scale
            elif on_missing:
                on_missing(ch, size, pos, line)

        group.line_height = line_height
        group.next_x = line.next_x = pos.x
        return group

    def kerning(self, c1, c2):
        return self._kerning.get((c1, c2), 0)

    def __repr__(self):
        return "<FontRenderer %r>" % self.filename


class FallbackFontRenderer:
    def __init__(self, query):
        self.query = FontQuery(query)
        self._best = None
        self._bq = None

    @property
    def best(self):
        cq = str(self.query)
        if self._best is None or self._bq != cq:
            self._best = fonts.best(self.query)
            self._bq = cq
        return self._best

    def _on_missing(self, char, size, pos, group):
        font = fonts.best(self.query.clone().char(char))
        child = font.render(char, size, pos)
        if len(child.shapes) == 2:
            group.add_shape(child.shapes[0])
        else:
            group.add_shape(child)

    def render(self, text, size, pos=None, use_kerning=True):
        return self.best.render(text, size, pos, self._on_missing, use_kerning)

    def __repr__(self):
        return "<FallbackFontRenderer %s>" % self.query


class FontStyle:
    def __init__(self, query, size, justify=TextJustify.Left, position=None, use_kerning=True):
        self._renderer = FallbackFontRenderer(query)
        self.size = size
        self.justify = justify
        self.position = position.clone() if position else NVector(0, 0)
        self.use_kerning = use_kerning

    @property
    def query(self):
        return self._renderer.query

    @query.setter
    def query(self, value):
        if str(value) != str(self.query):
            self._renderer = FallbackFontRenderer(value)

    @property
    def renderer(self):
        return self.renderer

    def render(self, text, pos=NVector(0, 0)):
        group = self._renderer.render(text, self.size, self.position+pos, self.use_kerning)
        for subg in group.shapes[:-1]:
            if self.justify == TextJustify.Center:
                subg.transform.position.value.x -= subg.next_x / 2
            elif self.justify == TextJustify.Right:
                subg.transform.position.value.x -= subg.next_x
        return group

    def clone(self):
        return FontStyle(str(self._renderer.query), self.size, self.justify, self.use_kerning)


def _propfac(a):
    return property(lambda s: s._get(a), lambda s, v: s._set(a, v))


class FontShape(CustomObject):
    _props = [
        TgsProp("query_string", "_query", str),
        TgsProp("size", "_size", float),
        TgsProp("justify", "_justify", TextJustify),
        TgsProp("text", "_text", str),
    ]
    wrapped_tgs = Group

    def __init__(self, text="", query="", size=64, justify=TextJustify.Left):
        CustomObject.__init__(self)
        if isinstance(query, FontStyle):
            self.style = query
        else:
            self.style = FontStyle(query, size, justify)
        self.text = text
        self.hidden = None

    def _get(self, a):
        return getattr(self.style, a)

    def _set(self, a, v):
        return setattr(self.style, a, v)

    query = _propfac("query")
    size = _propfac("size")
    justify = _propfac("justify")

    @property
    def query_string(self):
        return str(self.query)

    @query_string.setter
    def query_string(self, v):
        self.query = v

    def _build_wrapped(self):
        g = self.style.render(self.text)
        self.line_height = g.line_height
        return g

    def bounding_box(self, time=0):
        return self.wrapped.bounding_box(time)
