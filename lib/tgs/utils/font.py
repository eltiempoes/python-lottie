import subprocess
import fontTools.pens.basePen
import fontTools.ttLib
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


class _SystemFontList:
    def __init__(self):
        self.fonts = None

    def _lazy_load(self):
        if self.fonts is None:
            self.load()

    def load(self):
        self.fonts = {}
        self.load_fc_list()

    def load_fc_list(self):
        p = subprocess.Popen(["fc-list", r'--format=%{file}\t%{family[0]}\t%{style[0]}\n'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        out = out.decode("utf-8").strip()
        if p.returncode == 0:
            for line in out.splitlines():
                file, family, styles = line.split("\t")
                self._get(family).add_file(styles.split(" "), file)

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

    def render(self, size, text, on_missing=None):
        """!
        Renders some text

        @param size         Font size (in pizels)
        @param text         String to render
        @param on_missing   Callable on missing glyphs, called with:
        - Character as string
        - Font size
        - [in, out] Character position
        - Group shape

        @returns a Group shape, augmented with some extra attributes:
        - next_pos      Offset for the next glyph
        - line_height   Line height

        """
        scale = size / self.font.tables["head"].unitsPerEm
        line_height = self.font.tables["head"].yMax
        group = Group()
        group.name = text
        group.transform.scale.value = NVector(100, 100) * scale
        pos = NVector(0, 0)
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
                on_missing(ch, size, pos, group)

        group.next_pos = pos * scale
        group.line_height = line_height * scale
        return group

    def __repr__(self):
        return "<FontRenderer %r>" % self.filename
