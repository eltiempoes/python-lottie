import os
import pkgutil
import importlib


class Exporter:
    def __init__(self, name, extensions, callback, extra_options=[], generic_options=set(), slug=None):
        self.name = name
        self.extensions = extensions
        self.callback = callback
        self.extra_options = extra_options
        self.generic_options = generic_options
        self.slug = slug if slug is not None else extensions[0]

    def export(self, animation, filename, options):
        self.callback(animation, filename, **options)

    def __repr__(self):
        return "<Exporter %s>" % self.slug

    def argparse_options(self, ns):
        o_options = {}
        for opt in self.extra_options:
            o_options[opt.name] = getattr(ns, opt.nsvar(self.slug))
        for opt in self.generic_options:
            o_options[opt] = getattr(ns, opt)
        return o_options


class ExtraOption:
    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs

    def add_argument(self, slug, parser):
        opt = "--%s-%s" % (slug, self.name.replace("_", "-"))
        parser.add_argument(opt, metavar=self.name, **self.kwargs)

    def nsvar(self, slug):
        return "%s_%s" % (slug, self.name)


_exporters = {}


def exporter(name, extensions, extra_options=[], generic_options=set(), slug=None):
    def decorator(callback):
        exporter = Exporter(name, extensions, callback, extra_options, generic_options, slug)
        _exporters[exporter.slug] = exporter
        return callback
    return decorator


def _add_options(parser, ie, object):
    if not object.extra_options:
        return

    suf = " %sing options" % ie
    group = parser.add_argument_group(object.name + suf)
    for op in object.extra_options:
        op.add_argument(object.slug, group)


class _ExporterLoader:
    def __init__(self):
        self._exporters = None

    def load_modules(self):
        for _, modname, _ in pkgutil.iter_modules([os.path.dirname(__file__)]):
            if modname == "base":
                continue

            #full_modname = "tgs.exporters." + modname
            full_modname = "." + modname
            try:
                importlib.import_module(full_modname, "tgs.exporters")
            except ImportError:
                pass

    @property
    def exporters(self):
        if self._exporters is None:
            self.load_modules()
            self._exporters = _exporters
        return self._exporters

    def __iter__(self):
        return iter(self.exporters.values())

    def get(self, slug):
        return self.exporters.get(slug, None)

    def __getitem__(self, key):
        return self.get(key)

    def get_from_filename(self, filename):
        return self.get_from_extension(os.path.splitext(filename)[1][1:])

    def get_from_extension(self, ext):
        for p in self.exporters.values():
            if ext in p.extensions:
                return p
        return None

    def set_options(self, parser):
        group = parser.add_argument_group("Generic output options")
        group.add_argument(
            "--pretty", "-p",
            action="store_true",
            help="Pretty print (for formats that support it)",
        )
        group.add_argument(
            "--frame",
            type=int,
            default=0,
            help="Frame to extract (for single-image formats)",
        )

        for exporter in self.exporters.values():
            _add_options(parser, "export", exporter)

        return group

    def keys(self):
        return self.exporters.keys()


exporters = _ExporterLoader()
