#!/usr/bin/env python3

import io
import os
import sys
import json
import signal
import argparse
import tempfile

from PyQt5 import QtSvg
from PyQt5.Qsci import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie import gui, objects
from lottie import __version__
from lottie.exporters.svg import export_svg
from lottie.exporters.core import export_tgs
from lottie.exporters.tgs_validator import TgsValidator


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
        ks = QKeySequence
        for action in [
            ("&Open...",    "document-open",    ks.Open,    self.dialog_open_file),
            ("&Save",       "document-save",    ks.Save,    self.save_code, "action_save"),
            ("Save &As...", "document-save-as", ks.SaveAs,  self.dialog_save_as),
            ("&Refresh",    "document-revert",  ks.Refresh, self.reload_document),
            ("A&uto Refresh", "view-refresh",   None,       None, "action_auto_refresh"),
            ("&Validate TGS", "document-edit-verify", None, self.tgs_check),
            ("&Quit",       "application-exit", ks.Quit,    self.close),
        ]:
            self._make_action(file_menu, file_toolbar, *action)

        self.action_auto_refresh.setCheckable(True)
        self.action_auto_refresh.setChecked(True)
        self.action_save.setEnabled(False)

        self.view_menu = menu.addMenu("&View")

        self.tree_widget = QTreeWidget()
        self.tree_widget.setColumnCount(2)
        self.tree_widget.setHeaderLabels(["Property", "Value"])
        self.tree_widget.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.dock_tree = self._dock("Properties", self.tree_widget, Qt.LeftDockWidgetArea, Qt.RightDockWidgetArea)

        layout_display = QHBoxLayout()
        self.layout.addLayout(layout_display)
        self.display = QtSvg.QSvgWidget()
        layout_display.addWidget(self.display)
        self.display.setFixedSize(512, 512)
        self.display.setAutoFillBackground(True)
        palette = self.display.palette()
        palette.setBrush(
            self.display.backgroundRole(),
            QBrush(QColor(255, 255, 255))
            #QBrush(QColor(128, 128, 128), Qt.Dense7Pattern)
        )
        self.display.setPalette(palette)

        self.widget_time = gui.timeline_widget.TimelineWidget()
        self.widget_time.frame_changed.connect(self._update_frame)
        self.widget_time.setEnabled(False)
        self._dock("Timeline", self.widget_time, Qt.BottomDockWidgetArea, Qt.TopDockWidgetArea)

        self._init_json_editor()
        code_menu = menu.addMenu("&Code")
        code_toolbar = self.addToolBar("Code")
        toggle_action = self.dock_json.toggleViewAction()
        toggle_action.setIcon(QIcon.fromTheme("document-edit"))
        code_toolbar.addAction(toggle_action)

        apply_key = QKeySequence("Ctrl+B", QKeySequence.PortableText)
        for action in [
            ("&Apply",  "system-run",   apply_key,  self.apply_json),
            ("&Code",   "code-context", None,       self.toggle_code, "action_code_mode"),
        ]:
            self._make_action(code_menu, code_toolbar, *action)

        self.action_code_mode.setCheckable(True)
        self.action_code_mode.setEnabled(False)
        self.code_mode = None

        self._old_load = objects.Animation.load
        objects.Animation.load = self._new_load

        self.label_cahed = QLabel()
        self.statusBar().addPermanentWidget(self.label_cahed)

        self.fs_watcher = QFileSystemWatcher()
        self.fs_watcher.fileChanged.connect(self.maybe_reload)

        self.filename = ""

    def _init_json_editor(self):
        self.edit_json = QsciScintilla()
        self.edit_json.setUtf8(True)
        self.edit_json.setIndentationGuides(True)
        self.edit_json.setIndentationsUseTabs(False)
        self.edit_json.setTabWidth(4)
        self.edit_json.setTabIndents(True)
        self.edit_json.setAutoIndent(True)
        self.edit_json.setMarginType(0, QsciScintilla.NumberMargin)
        self.edit_json.setMarginWidth(0, "0000")
        self.edit_json.setFolding(QsciScintilla.BoxedTreeFoldStyle)

        self.code_font = QFont("monospace", 10)
        self.code_font.setStyleHint(QFont.Monospace)
        self.edit_json.setFont(self.code_font)

        self.lexer_svg = QsciLexerXML()
        self.lexer_svg.setDefaultFont(self.code_font)

        self.lexer_py = QsciLexerPython()
        self.lexer_py.setDefaultFont(self.code_font)
        self.lexer_py.setFont(self.code_font)

        self.lexer_json = QsciLexerJSON()
        self.lexer_json.setDefaultFont(self.code_font)

        self.edit_json.setLexer(self.lexer_json)

        self.dock_json = self._dock("Json", self.edit_json, Qt.RightDockWidgetArea, Qt.LeftDockWidgetArea)
        self.dock_json.hide()

    def _init_code_editor(self):
        self.lexer_svg = QsciLexerXML()
        self.lexer_svg

    def _new_load(self, json_dict):
        self._json_dump = json.dumps(json_dict, indent=" "*4)
        if not self.action_code_mode.isChecked():
            self.edit_json.setText(self._json_dump)
        return self._old_load(json_dict)

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        w = ev.size().width()
        docks = []

        if self.dock_tree.isVisible():
            docks.append(self.dock_tree)

        if self.dock_json.isVisible():
            docks.append(self.dock_json)

        if docks:
            self.resizeDocks(docks, [w] * len(docks), Qt.Horizontal)

    def _dock(self, name, widget, start_area, other_areas):
        dock = QDockWidget(name, self)
        dock.setAllowedAreas(start_area | other_areas)
        self.addDockWidget(start_area, dock)
        dock.setWidget(widget)
        self.view_menu.addAction(dock.toggleViewAction())
        return dock

    def _make_action(self, menu, toolbar, name, theme, key_sequence, trigger, attname=None):
        action = QAction(QIcon.fromTheme(theme), name, self)
        if key_sequence:
            action.setShortcut(key_sequence)
        if trigger:
            action.triggered.connect(trigger)

        if attname:
            setattr(self, attname, action)

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
        self._clear()
        self.setWindowTitle("Lottie Viewer")
        if self.filename:
            self.fs_watcher.removePath(self.filename)

        self.importer = None
        self.importer_options = None
        self.filename = ""
        self.edit_json.setText("")
        self.clear_code_mode()

    def clear_code_mode(self):
        self.code_mode = None
        self.action_save.setEnabled(False)
        self.action_code_mode.setEnabled(False)
        self.action_code_mode.setChecked(False)
        self.edit_json.setLexer(self.lexer_json)

    def _clear(self):
        self.widget_time.stop()
        self.animation = None
        self.widget_time.setEnabled(False)
        self.widget_time.stop()
        self._frame_cache = {}
        self.tree_widget.clear()

    def open_file(self, file_name, importer, options=None):
        if options is None:
            options = importer.prompt_options(self)
            if options is None:
                return

        self.close_file()
        animation = importer.importer.process(file_name, **options)
        self._open_animation(animation)
        self.setWindowTitle("Lottie Viewer - %s" % os.path.basename(file_name))
        self.dirname = os.path.dirname(file_name)
        self.importer = importer
        self.importer_options = options
        self.filename = file_name
        self.fs_watcher.addPath(self.filename)

        ext = os.path.splitext(file_name)[1][1:]
        if ext in ["svg", "py"]:
            self.code_mode = ext
            self.action_code_mode.setEnabled(True)
            with open(file_name) as f:
                self._code_dump = f.read()
        elif ext == "json":
            self.action_save.setEnabled(True)

    def _open_animation(self, animation):
        self.widget_time.set_min_max(animation.in_point, animation.out_point)
        self.widget_time.set_frame(animation.in_point)
        self.widget_time.fps = animation.frame_rate
        self.animation = animation
        self.display.setFixedSize(self.animation.width, self.animation.height)
        gui.tree_view.lottie_to_tree(self.tree_widget, animation)
        self._update_frame()
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

        file = io.StringIO()
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

    def tgs_check(self):
        if not self.animation:
            return

        validator = TgsValidator()
        validator(self.animation)
        bio = io.BytesIO()
        export_tgs(self.animation, bio, False, False)
        validator.check_size(len(bio.getvalue()), "exported")
        if validator.errors:
            QMessageBox.warning(
                self,
                "TGS Validation Issues",
                "\n".join(map(str, validator.errors))+"\n",
                QMessageBox.Ok
            )
        else:
            QMessageBox.information(
                self,
                "TGS Validation Issues",
                "No issues found",
                QMessageBox.Ok
            )

    def apply_json(self):
        if self.code_mode and self.action_code_mode.isChecked():
            with tempfile.NamedTemporaryFile("w") as file:
                file.write(self.edit_json.text())
                file.flush()
                animation = self.importer.importer.process(file.name, **self.importer_options)
        else:
            animation = objects.Animation.load(json.loads(self.edit_json.text()))

        self._clear()
        self._open_animation(animation)

    def toggle_code(self):
        self.action_save.setEnabled(False)
        if not self.animation or not self.code_mode:
            return

        if self.action_code_mode.isChecked():
            self.action_auto_refresh.setChecked(False)
            self.action_save.setEnabled(True)
            if not self.dock_json.isVisible():
                self.dock_json.show()
            self.edit_json.setLexer(getattr(self, "lexer_" + self.code_mode))
            self.edit_json.setText(self._code_dump)
        else:
            self.edit_json.setLexer(self.lexer_json)
            self.edit_json.setText(self._json_dump)

    def save_code(self):
        with open(self.filename, "w") as outfile:
            outfile.write(self.edit_json.text())


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
