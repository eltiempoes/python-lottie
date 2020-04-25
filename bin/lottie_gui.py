#!/usr/bin/env python3

import os
import sys
import signal
import argparse
import threading
from io import StringIO

from PySide2 import QtCore, QtWidgets, QtGui, QtSvg

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.exporters.svg import export_svg
from lottie.exporters.base import exporters
from lottie.importers.base import importers
from lottie.parsers.baseporter import IoProgressReporter, ExtraOption
from lottie import __version__


class GuiProgressReporter(IoProgressReporter):
    def __init__(self):
        self.dialogs = {}
        self.threads = {}
        self.lock = threading.Lock()
        self.id = 0

    def gen_id(self, parent):
        self.id += 1
        with self.lock:
            dialog = QtWidgets.QProgressDialog(parent)
            dialog.setCancelButton(None)
            dialog.setWindowModality(QtGui.Qt.ApplicationModal)
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
            self.dialogs.pop(self.threads.pop(id)).hide()


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
            widget.setChecked(True)
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
    def __init__(self, id, exporter, animation, file_name, options):
        super().__init__()
        self.id = id
        self.animation = animation
        self.exporter = exporter
        self.file_name = file_name
        self.options = options

    def run(self):
        IoProgressReporter.instance.setup("Export to %s" % self.exporter.name, self.id)
        self.exporter.process(self.animation, self.file_name, **self.options)
        IoProgressReporter.instance.cleanup()


class LottieViewerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.animation = None
        self.dirname = ""
        self._frame_cache = {}
        self._fu_gc = []
        self.setWindowTitle("Lottie Viewer")

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(self.layout)

        self.display = QtSvg.QSvgWidget()
        self.display.setFixedSize(512, 512)
        layout_display = QtWidgets.QHBoxLayout()
        layout_display.addWidget(self.display)
        self.layout.addLayout(layout_display)
        self.display.setAutoFillBackground(True)
        palette = self.display.palette()
        palette.setBrush(
            self.display.backgroundRole(),
            QtGui.QBrush(QtGui.QColor(255, 255, 255))
            #QtGui.QBrush(QtGui.QColor(128, 128, 128), QtCore.Qt.Dense7Pattern)
        )
        self.display.setPalette(palette)

        self.layout_slider = QtWidgets.QHBoxLayout()
        self.button_play = QtWidgets.QPushButton()
        self.button_play.setCheckable(True)
        self.button_play.toggled.connect(self.play_toggle)
        self.layout_slider.addWidget(self.button_play)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.layout_slider.addWidget(self.slider)
        self.slider_spin = QtWidgets.QSpinBox()
        self.layout_slider.addWidget(self.slider_spin)
        self.layout.addLayout(self.layout_slider)
        self.slider.valueChanged.connect(self.slider_spin.setValue)
        self.slider_spin.valueChanged.connect(self.slider.setValue)
        self.slider_spin.valueChanged.connect(self._update_frame)

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        self._make_action(file_menu, "&Open...", "document-open", QtGui.QKeySequence.Open, self.dialog_open_file)
        self._make_action(file_menu, "Save &As..", "document-save-as", QtGui.QKeySequence.SaveAs, self.dialog_save_as)
        self._make_action(file_menu, "&Quit", "application-exit", QtGui.QKeySequence.Quit, self.close)

        self.label_cahed = QtWidgets.QLabel()
        self.statusBar().addPermanentWidget(self.label_cahed)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._next_frame)
        self.stop()

    def _make_action(self, menu, name, theme, key_sequence, trigger):
        action = QtWidgets.QAction(QtGui.QIcon.fromTheme(theme), name, self)
        action.setShortcut(key_sequence)
        action.triggered.connect(trigger)
        menu.addAction(action)

    def dialog_open_file(self):
        filters = ";;".join(ge.file_filter for ge in gui_importers)
        file_name, filter = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Animation", self.dirname, filters
        )
        for importer in gui_importers:
            if importer.file_filter == filter:
                break
        else:
            return

        if file_name:
            self.open_file(file_name, importer)

    def dialog_save_as(self):
        filters = ";;".join(ge.file_filter for ge in gui_exporters)
        file_name, filter = QtWidgets.QFileDialog.getSaveFileName(self, "Save Animation", self.dirname, filters)

        if not file_name:
            return

        for exporter in gui_exporters:
            if exporter.file_filter == filter:
                break
        else:
            return

        if exporter.needs_dialog:
            exporter.dialog.setParent(self)
            exporter.dialog.setWindowFlags(QtGui.Qt.Dialog)
            if exporter.dialog.exec_() != QtWidgets.QDialog.DialogCode.Accepted:
                return

        options = exporter.get_options()
        if not os.path.splitext(file_name)[1]:
            file_name += "." + exporter.exporter.extensions[0]

        thread = ExportThread(
            IoProgressReporter.instance.gen_id(self), exporter.exporter,
            self.animation, file_name, options
        )
        thread.start()
        self._fu_gc.append(thread)

    def open_file(self, file_name, importer):
        if importer.needs_dialog:
            importer.dialog.setParent(self)
            importer.dialog.setWindowFlags(QtGui.Qt.Dialog)
            if importer.dialog.exec_() != QtWidgets.QDialog.DialogCode.Accepted:
                return

        self.stop()
        self.animation = None
        self._frame_cache = {}
        animation = importer.importer.process(file_name, **importer.get_options())
        self.slider.setMinimum(animation.in_point)
        self.slider.setMaximum(animation.out_point)
        self.slider_spin.setMinimum(animation.in_point)
        self.slider_spin.setMaximum(animation.out_point)
        self.slider.setValue(animation.in_point)
        self.animation = animation
        self.display.setFixedSize(self.animation.width, self.animation.height)
        self._update_frame()
        self.setWindowTitle("Lottie Viewer - %s" % os.path.basename(file_name))
        self.dirname = os.path.dirname(file_name)

    def _update_frame(self):
        if not self.animation:
            return

        rendered = self._render_frame(self.slider_spin.value())
        self.display.load(rendered)

    def _render_frame(self, frame):
        if frame in self._frame_cache:
            return self._frame_cache[frame]

        file = StringIO()
        export_svg(self.animation, file, frame)
        rendered = file.getvalue().encode("utf-8")
        self._frame_cache[frame] = rendered
        self.label_cahed.setText("%d%% Frames Rendered" % (
            len(self._frame_cache) / (self.animation.out_point - self.animation.in_point) * 100
        ))
        return rendered

    def stop(self):
        self.timer.stop()
        self.button_play.setIcon(QtGui.QIcon.fromTheme("media-playback-start"))
        self.button_play.setText("Play")
        self.button_play.setChecked(False)

    def play(self):
        if not self.animation:
            self.stop()
            return

        self.button_play.setIcon(QtGui.QIcon.fromTheme("media-playback-stop"))
        self.button_play.setText("Stop")

        self.timer.start(1000/self.animation.frame_rate)

    def _next_frame(self):
        nf = self.slider.value() + 1
        if nf > self.animation.out_point:
            nf = self.animation.in_point
        self.slider.setValue(nf)

    def play_toggle(self, play):
        if play:
            self.play()
        else:
            self.stop()


gui_exporters = list(map(GuiExporter, exporters))
gui_importers = list(map(GuiImporter, importers))

parser = argparse.ArgumentParser(description="GUI viewer for lottie Animations")
parser.add_argument(
    "file",
    help="File to open",
    default=None,
    nargs="?"
)
parser.add_argument("--version", "-v", action="version", version="%(prog)s - python-lottie " + __version__)

if __name__ == "__main__":
    ns = parser.parse_args()

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QtWidgets.QApplication([])

    IoProgressReporter.instance = GuiProgressReporter()

    window = LottieViewerWindow()
    window.resize(800, 600)
    window.show()
    if ns.file:
        importer = importers.get_from_filename(ns.file)
        for gip in gui_importers:
            if gip.importer is importer:
                break
        window.open_file(ns.file, gip)

    sys.exit(app.exec_())


