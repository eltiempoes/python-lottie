
from .base import exporter
from ..parsers.sif.builder import to_sif


@exporter("Synfig", ["sif"], [], {"pretty"})
def export_sif(animation, fp, pretty=True):
    dom = to_sif(animation)
    if isinstance(fp, str):
        fp = open(fp, "w")
    dom.writexml(fp, "", "  " if pretty else "", "\n" if pretty else "")
