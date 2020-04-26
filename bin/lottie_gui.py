#!/usr/bin/env python3

import os
import sys
import signal
import argparse
from io import StringIO

from PySide2 import QtCore, QtWidgets, QtGui, QtSvg

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie import gui
from lottie import __version__
from lottie.exporters.svg import export_svg
from lottie.importers.base import importers

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

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_toolbar = self.addToolBar("File")
        ks = QtGui.QKeySequence
        for action in [
            ("&Open...",    "document-open",    ks.Open,    self.dialog_open_file),
            ("Save &As...", "document-save-as", ks.SaveAs,  self.dialog_save_as),
            ("&Refresh",    "view-refresh",     ks.Refresh, self.reload_document),
            ("&Quit",       "application-exit", ks.Quit,    self.close),
        ]:
            self._make_action(file_menu, file_toolbar, *action)

        self.view_menu = menu.addMenu("&View")

        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setColumnCount(1)
        self.tree_widget.setHeaderLabels(["Name"])
        self._dock("Tree", self.tree_widget, QtCore.Qt.LeftDockWidgetArea, QtCore.Qt.RightDockWidgetArea)

        layout_display = QtWidgets.QHBoxLayout()
        self.layout.addLayout(layout_display)
        self.display = QtSvg.QSvgWidget()
        layout_display.addWidget(self.display)
        self.display.setFixedSize(512, 512)
        self.display.setAutoFillBackground(True)
        palette = self.display.palette()
        palette.setBrush(
            self.display.backgroundRole(),
            QtGui.QBrush(QtGui.QColor(255, 255, 255))
            #QtGui.QBrush(QtGui.QColor(128, 128, 128), QtCore.Qt.Dense7Pattern)
        )
        self.display.setPalette(palette)

        self.widget_time = gui.timeline_widget.TimelineWidget()
        self.widget_time.frame_changed.connect(self._update_frame)
        self.widget_time.setEnabled(False)
        self._dock("Timeline", self.widget_time, QtCore.Qt.BottomDockWidgetArea, QtCore.Qt.TopDockWidgetArea)

        self.label_cahed = QtWidgets.QLabel()
        self.statusBar().addPermanentWidget(self.label_cahed)

    def _dock(self, name, widget, start_area, other_areas):
        dock = QtWidgets.QDockWidget(name, self)
        dock.setAllowedAreas(start_area | other_areas)
        self.addDockWidget(start_area, dock)
        dock.setWidget(widget)
        self.view_menu.addAction(dock.toggleViewAction())
        return dock

    def _make_action(self, menu, toolbar, name, theme, key_sequence, trigger):
        action = QtWidgets.QAction(QtGui.QIcon.fromTheme(theme), name, self)
        action.setShortcut(key_sequence)
        action.triggered.connect(trigger)
        menu.addAction(action)
        toolbar.addAction(action)

    def dialog_open_file(self):
        file_name, importer = gui.import_export.get_open_filename(
            self, "Open Animation", self.dirname
        )

        if file_name:
            self.open_file(file_name, importer)

    def dialog_save_as(self):
        file_name, exporter = gui.import_export.get_save_filename(
            self, "Open Animation", self.dirname
        )

        if not file_name:
            return

        options = exporter.prompt_options(self)
        if options is None:
            return

        if not os.path.splitext(file_name)[1]:
            file_name += "." + exporter.exporter.extensions[0]

        thread = gui.import_export.start_export(self, exporter.exporter, self.animation, file_name, options)
        self._fu_gc.append(thread)

    def open_file(self, file_name, importer, options=None):
        if options is None:
            options = importer.prompt_options(self)
            if options is None:
                return

        self.widget_time.stop()
        self.animation = None
        self.widget_time.setEnabled(False)
        self.widget_time.stop()
        self._frame_cache = {}
        animation = importer.importer.process(file_name, **options)
        self.widget_time.set_min_max(animation.in_point, animation.out_point)
        self.widget_time.set_frame(animation.in_point)
        self.widget_time.fps = animation.frame_rate
        self.animation = animation
        self.display.setFixedSize(self.animation.width, self.animation.height)
        self.tree_widget.clear()
        gui.tree_view.lottie_to_tree(self.tree_widget, animation)
        self._update_frame()
        self.setWindowTitle("Lottie Viewer - %s" % os.path.basename(file_name))
        self.dirname = os.path.dirname(file_name)
        self.importer = importer
        self.importer_options = options
        self.filename = file_name

        self.widget_time.setEnabled(True)

    def reload_document(self):
        if self.animation:
            self.open_file(self.filename, self.importer, self.importer_options)

    def _update_frame(self):
        if not self.animation:
            return

        rendered = self._render_frame(self.widget_time.frame)
        self.display.load(rendered)

    def _render_frame(self, frame):
        if frame in self._frame_cache:
            return self._frame_cache[frame]

        file = StringIO()
        export_svg(self.animation, file, frame)
        rendered = file.getvalue().encode("utf-8")
        self._frame_cache[frame] = rendered
        self.label_cahed.setText("%d%% Frames Rendered" % (
            len(self._frame_cache) / ((self.animation.out_point+1) - self.animation.in_point) * 100
        ))
        return rendered


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

    gui.import_export.GuiProgressReporter.set_global()

    window = LottieViewerWindow()
    window.resize(800, 600)
    window.show()
    if ns.file:
        importer = importers.get_from_filename(ns.file)
        for gip in gui.import_export.gui_importers:
            if gip.importer is importer:
                break
        window.open_file(ns.file, gip)

    sys.exit(app.exec_())


