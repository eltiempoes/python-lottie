from io import StringIO
from difflib import SequenceMatcher
from ..exporters import prettyprint


def difflines_str(a, b, width=60):
    lines_a = a.splitlines()
    lines_b = b.splitlines()
    ia = 0
    ib = 0

    for ja, jb, size in SequenceMatcher(None, lines_a, lines_b, False).get_matching_blocks():
        sideprinter(lines_a[ia:ja], lines_b[ib:jb], width, "\x1b[31m>", "=", "<\x1b[m")
        ia = ja+size
        ib = jb+size
        sideprinter(lines_a[ja:ia], lines_b[jb:ib], width, "\x1b[m ", "|", " \x1b[m")


def sideprinter(left, right, width=40, prefix="", infix=" | ", suffix=""):
    if len(left) > len(right):
        right += [""] * (len(left) - len(right))
    else:
        left += [""] * (len(right) - len(left))
    for l, r in zip(left, right):
        print("".join([prefix, l[:width].ljust(width), infix, r[:width].ljust(width), suffix]))


def difflines(a, b, width=60):
    ioa = StringIO()
    prettyprint(a, ioa)
    iob = StringIO()
    prettyprint(b, iob)
    difflines_str(ioa.getvalue(), iob.getvalue())
