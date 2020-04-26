#!/usr/bin/env python3

import os
import sys
import signal
import argparse
from io import StringIO

from PySide2 import QtGui, QtSvg
from PySide2.QtWidgets import *
from PySide2.QtCore import *

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie import gui
from lottie import __version__
from lottie.exporters.svg import export_svg


class LottieViewerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.animation = None
        self.dirname = ""
        self._frame_cache = {}
        self._fu_gc = []
        self.setWindowTitle("Lottie Viewer")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_toolbar = self.addToolBar("File")
        ks = QtGui.QKeySequence
        file_actions = [
            self._make_action(file_menu, file_toolbar, *action)
            for action in [
                ("&Open...",    "document-open",    ks.Open,    self.dialog_open_file),
                ("Save &As...", "document-save-as", ks.SaveAs,  self.dialog_save_as),
                ("&Refresh",    "document-revert",  ks.Refresh, self.reload_document),
                ("A&uto Refresh", "view-refresh",   None,       None),
                ("&Quit",       "application-exit", ks.Quit,    self.close),
            ]
        ]
        self.action_auto_refresh = file_actions[3]
        self.action_auto_refresh.setCheckable(True)
        self.action_auto_refresh.setChecked(True)

        self.view_menu = menu.addMenu("&View")

        self.tree_widget = QTreeWidget()
        self.tree_widget.setColumnCount(2)
        self.tree_widget.setHeaderLabels(["Property", "Value"])
        self.tree_widget.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.dock_tree = self._dock("Tree", self.tree_widget, Qt.LeftDockWidgetArea, Qt.RightDockWidgetArea)

        layout_display = QHBoxLayout()
        self.layout.addLayout(layout_display)
        self.display = QtSvg.QSvgWidget()
        layout_display.addWidget(self.display)
        self.display.setFixedSize(512, 512)
        self.display.setAutoFillBackground(True)
        palette = self.display.palette()
        palette.setBrush(
            self.display.backgroundRole(),
            QtGui.QBrush(QtGui.QColor(255, 255, 255))
            #QtGui.QBrush(QtGui.QColor(128, 128, 128), Qt.Dense7Pattern)
        )
        self.display.setPalette(palette)

        self.widget_time = gui.timeline_widget.TimelineWidget()
        self.widget_time.frame_changed.connect(self._update_frame)
        self.widget_time.setEnabled(False)
        self._dock("Timeline", self.widget_time, Qt.BottomDockWidgetArea, Qt.TopDockWidgetArea)

        self.label_cahed = QLabel()
        self.statusBar().addPermanentWidget(self.label_cahed)

        self.fs_watcher = QFileSystemWatcher()
        self.fs_watcher.fileChanged.connect(self.maybe_reload)

        self.filename = ""

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        w = ev.size().width()
        self.resizeDocks([self.dock_tree], [w], Qt.Horizontal)

    def _dock(self, name, widget, start_area, other_areas):
        dock = QDockWidget(name, self)
        dock.setAllowedAreas(start_area | other_areas)
        self.addDockWidget(start_area, dock)
        dock.setWidget(widget)
        self.view_menu.addAction(dock.toggleViewAction())
        return dock

    def _make_action(self, menu, toolbar, name, theme, key_sequence, trigger):
        action = QAction(QtGui.QIcon.fromTheme(theme), name, self)
        if key_sequence:
            action.setShortcut(key_sequence)
        if trigger:
            action.triggered.connect(trigger)
        menu.addAction(action)
        toolbar.addAction(action)
        return action

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

    def close_file(self):
        self.widget_time.stop()
        self.animation = None
        self.widget_time.setEnabled(False)
        self.widget_time.stop()
        self._frame_cache = {}
        self.tree_widget.clear()
        self.setWindowTitle("Lottie Viewer")
        if self.filename:
            self.fs_watcher.removePath(self.filename)
        self.importer = None
        self.importer_options = None
        self.filename = ""

    def open_file(self, file_name, importer, options=None):
        if options is None:
            options = importer.prompt_options(self)
            if options is None:
                return

        self.close_file()
        animation = importer.importer.process(file_name, **options)
        self.fs_watcher
        self.widget_time.set_min_max(animation.in_point, animation.out_point)
        self.widget_time.set_frame(animation.in_point)
        self.widget_time.fps = animation.frame_rate
        self.animation = animation
        self.display.setFixedSize(self.animation.width, self.animation.height)
        gui.tree_view.lottie_to_tree(self.tree_widget, animation)
        self._update_frame()
        self.setWindowTitle("Lottie Viewer - %s" % os.path.basename(file_name))
        self.dirname = os.path.dirname(file_name)
        self.importer = importer
        self.importer_options = options
        self.filename = file_name
        self.fs_watcher.addPath(self.filename)
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

    def maybe_reload(self, filename):
        if filename == self.filename and self.action_auto_refresh.isChecked():
            self.open_file(self.filename, self.importer, self.importer_options)


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

    app = QApplication([])

    gui.import_export.GuiProgressReporter.set_global()

    window = LottieViewerWindow()
    window.resize(1024, 800)
    window.show()
    if ns.file:
        importer = gui.import_export.gui_importer_from_filename(ns.file)
        window.open_file(ns.file, importer)

    sys.exit(app.exec_())
