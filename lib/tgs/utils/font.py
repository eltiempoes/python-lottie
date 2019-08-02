import os
import subprocess
import fontTools.pens.basePen
import fontTools.ttLib
from xml.etree import ElementTree
from .nvector import NVector
from ..objects.bezier import Bezier, BezierPoint
from ..objects.shapes import Path, Group


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
    \see https://www.freedesktop.org/software/fontconfig/fontconfig-user.html#AEN21 https://manpages.ubuntu.com/manpages/cosmic/man1/fc-pattern.1.html
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
            )
            self.family(family)

    def family(self, name):
        self._query["family"] = name
        return self

    def weight(self, weight):
        self._query["weight"] = weight
        return self

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

    def __str__(self):
        return self._query.get("family", "") + ":" + ":".join(
            "%s=%s" % (p, v)
            for p, v in self._query.items()
            if p != "family"
        )

    def __repr__(self):
        return "<FontQuery %r>" % str(self)


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


class FontRenderer:
    def __init__(self, filename):
        self.filename = filename
        self.font = fontTools.ttLib.TTFont(filename)
        self.glyphset = self.font.getGlyphSet()

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

    def render(self, text, size, pos=None, on_missing=None):
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
        scale = size / self.font.tables["head"].unitsPerEm
        line_height = self.font.tables["head"].yMax
        group = Group()
        group.name = text
        group.transform.scale.value = NVector(100, 100) * scale
        pos /= scale
        for ch in text:
            if ch == "\n":
                pos.x = 0
                pos.y += line_height
                continue

            chname = self.font._makeGlyphName(ord(ch))
            if chname in self.glyphset:
                for sh in self.glyph_shapes(chname, pos):
                    group.add_shape(sh)
                pos.x += self.glyphset[chname].width
            elif on_missing:
                on_missing(ch, self.font.tables["head"].unitsPerEm, pos, group)

        pos *= scale
        group.line_height = line_height * scale
        return group

    def __repr__(self):
        return "<FontRenderer %r>" % self.filename


class FallbackFontRenderer:
    def __init__(self, query):
        self.query = FontQuery(query)
        self.best = fonts.best(self.query)

    def _on_missing(self, char, size, pos, group):
        font = fonts.best(self.query.clone().char(char))
        group.add_shape(font.render(char, size, pos))

    def render(self, size, text):
        return self.best.render(size, text, NVector(0, 0), self._on_missing)

    def __repr__(self):
        return "<FallbackFontRenderer %s>" % self.query
