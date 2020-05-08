import threading
from functools import reduce
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt

from ..exporters.base import exporters
from ..importers.base import importers
from ..parsers.baseporter import IoProgressReporter, ExtraOption


class GuiProgressReporter(IoProgressReporter):
    def __init__(self):
        self.dialogs = {}
        self.threads = {}
        self.lock = threading.Lock()
        self.id = 0

    @classmethod
    def set_global(cls):
        IoProgressReporter.instance = cls()

    def gen_id(self, parent):
        self.id += 1
        with self.lock:
            dialog = QtWidgets.QProgressDialog(parent)
            dialog.setCancelButton(None)
            dialog.setWindowModality(Qt.ApplicationModal)
            self.dialogs[self.id] = dialog
        return self.id

    def get_thread_dialog(self):
        with self.lock:
            id = threading.current_thread().ident
            return self.dialogs[self.threads[id]]

    def setup(self, title, id):
        with self.lock:
            tid = threading.current_thread().ident
            self.threads[tid] = id
            dialog = self.dialogs[id]

        dialog.setWindowTitle(title)
        dialog.hide()

    def report_progress(self, title, value, total):
        dialog = self.get_thread_dialog()
        dialog.show()
        dialog.setValue(value)
        dialog.setMaximum(total)
        dialog.setLabelText(title)

    def report_message(self, message):
        dialog = self.get_thread_dialog()
        dialog.show()
        dialog.setRange(0, 0)
        dialog.setLabelText(message)

    def cleanup(self):
        with self.lock:
            id = threading.current_thread().ident
            dialog = self.dialogs.pop(self.threads.pop(id))
            dialog.hide()
            dialog.deleteLater()


class GuiBasePorter:
    def __init__(self, porter):
        self.porter = porter
        self.file_filter = "%s (%s)" % (porter.name, " ".join("*.%s" % e for e in porter.extensions))
        self._dialog = None
        self.widgets = {}

    def _build_dialog(self):
        self._dialog = QtWidgets.QDialog()
        self._dialog.setWindowTitle("Export to %s" % self.porter.name)
        layout = QtWidgets.QFormLayout()
        self._dialog.setLayout(layout)

        for go in self.porter.generic_options:
            self._generic_option(layout, go)

        for option in self.porter.extra_options:
            self._add_option(layout, option)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self._dialog.accept)
        button_box.rejected.connect(self._dialog.reject)
        layout.addRow(button_box)

    def _add_option(self, layout, option: ExtraOption):
        if option.dest in self.widgets:
            return
        label = QtWidgets.QLabel(option.name.replace("_", " ").title())

        default = option.kwargs.get("default", None)
        option_type = option.kwargs.get("type", str)

        if option.kwargs.get("action") == "store_true":
            widget = QtWidgets.QCheckBox()
            widget.setChecked(False)
            getter = widget.isChecked
        elif option.kwargs.get("action") == "store_false":
            widget = QtWidgets.QCheckBox()
            labtext = label.text()
            if labtext.startswith("No "):
                label.setText(labtext[3:])
            widget.setChecked(True)
            getter = widget.isChecked
        elif "choices" in option.kwargs:
            widget = QtWidgets.QComboBox()
            for choice in option.kwargs["choices"]:
                widget.addItem(str(choice))
            if default:
                widget.setCurrentText(str(default))
            getter = lambda: option_type(widget.currentText())
        elif option_type is int:
            widget = QtWidgets.QSpinBox()
            widget.setMinimum(-1000)
            widget.setMaximum(1000)
            if default is not None:
                widget.setValue(int(default))
            getter = widget.value
        else:
            widget = QtWidgets.QLineEdit()
            if default is not None:
                widget.setText(str(default))
            getter = widget.text

        help = option.kwargs.get("help", "")
        widget.setWhatsThis(help)
        widget.setToolTip(help)

        widget.setObjectName(option.dest)
        self.widgets[option.dest] = getter
        layout.addRow(label, widget)

    @property
    def needs_dialog(self):
        return self.porter.generic_options or self.porter.extra_options

    @property
    def dialog(self):
        if not self._dialog:
            self._build_dialog()
        return self._dialog

    def get_options(self):
        return {
            name: getter()
            for name, getter in self.widgets.items()
        }

    def prompt_options(self, parent):
        if self.needs_dialog:
            self.dialog.setParent(parent)
            self.dialog.setWindowFlags(Qt.Dialog)
            if self.dialog.exec_() != QtWidgets.QDialog.DialogCode.Accepted:
                return None

        return self.get_options()

    def _generic_option(self, layout, go):
        pass


class GuiExporter(GuiBasePorter):
    def _generic_option(self, layout, go):
        if go == "pretty":
            self._add_option(layout, ExtraOption("pretty", action="store_true", help="Pretty print"))
        if go == "frame":
            self._add_option(layout, ExtraOption("frame", type=int, help="Frame to extract"))

    @property
    def exporter(self):
        return self.porter


class GuiImporter(GuiBasePorter):
    @property
    def importer(self):
        return self.porter


class ExportThread(QtCore.QThread):
    def __init__(self, parent, exporter, animation, file_name, options):
        super().__init__()
        self.id = IoProgressReporter.instance.gen_id(parent)
        self.animation = animation
        self.exporter = exporter
        self.file_name = file_name
        self.options = options

    def run(self):
        IoProgressReporter.instance.setup("Export to %s" % self.exporter.name, self.id)
        try:
            self.exporter.process(self.animation, self.file_name, **self.options)
        except Exception:
            IoProgressReporter.instance.report_message("Error on export")
        IoProgressReporter.instance.cleanup()


gui_exporters = list(map(GuiExporter, exporters))
gui_importers = list(map(GuiImporter, importers))


def get_open_filename(parent, title, dirname):
    extensions = reduce(lambda a, b: a | b, (set(gi.importer.extensions) for gi in gui_importers))
    all_files = "All Supported Files (%s)" % " ".join("*.%s" % ex for ex in extensions)
    filters = all_files + ";;" + ";;".join(ge.file_filter for ge in gui_importers)
    file_name, filter = QtWidgets.QFileDialog.getOpenFileName(
        parent, title, dirname, filters
    )
    if file_name:
        if filter == all_files:
            importer = gui_importer_from_filename(file_name)
            if importer:
                return file_name, importer
        else:
            for importer in gui_importers:
                if importer.file_filter == filter:
                    return file_name, importer

    return None, None


def get_save_filename(parent, title, dirname):
    extensions = reduce(lambda a, b: a | b, (set(gi.exporter.extensions) for gi in gui_exporters))
    all_files = "All Supported Files (%s)" % " ".join("*.%s" % ex for ex in extensions)
    filters = all_files + ";;" + ";;".join(ge.file_filter for ge in gui_exporters)
    file_name, filter = QtWidgets.QFileDialog.getSaveFileName(
        parent, title, dirname, filters
    )

    if file_name:
        if filter == all_files:
            exporter = gui_exporter_from_filename(file_name)
            if exporter:
                return file_name, exporter
        else:
            for exporter in gui_exporters:
                if exporter.file_filter == filter:
                    return file_name, exporter

    return None, None


def start_export(parent, exporter, animation, file_name, options):
    thread = ExportThread(parent, exporter, animation, file_name, options)
    thread.start()
    return thread


def gui_importer_from_filename(filename):
    importer = importers.get_from_filename(filename)
    for gip in gui_importers:
        if gip.importer is importer:
            return gip
    return None


def gui_exporter_from_filename(filename):
    exporter = exporters.get_from_filename(filename)
    for gip in gui_exporters:
        if gip.exporter is exporter:
            return gip
    return None
