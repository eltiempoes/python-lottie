from xml.dom import minidom
from xml.etree import ElementTree

from .base import exporter
from ..parsers.svg.builder import to_svg


def _print_ugly_xml(dom, fp):
    return dom.write(fp, "utf-8", True)


def _print_pretty_xml(dom, fp):
    xmlstr = minidom.parseString(ElementTree.tostring(dom.getroot())).toprettyxml(indent="   ")
    if isinstance(fp, str):
        fp = open(fp, "w")
    fp.write(xmlstr)


@exporter("SVG", ["svg"], [], {"pretty", "frame"})
def export_svg(animation, fp, frame=0, pretty=True):
    _print_xml = _print_pretty_xml if pretty else _print_ugly_xml
    _print_xml(to_svg(animation, frame), fp)
