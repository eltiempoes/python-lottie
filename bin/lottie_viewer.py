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
from lottie.importers.core import import_tgs
from lottie.exporters.svg import export_svg
from lottie import __version__


class LottieViewerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.animation = None
        self._frame_cache = {}
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
        self._make_action(file_menu, "&Open", "document-open", QtGui.QKeySequence.Open, self.dialog_open_file)
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
        file_name, filter = QtWidgets.QFileDialog.getOpenFileName(self, "Open Animation", "", "Lottie (*.json *.tgs)")
        if file_name:
            self.open_file(file_name)

    def open_file(self, file_name):
        self.stop()
        self.animation = None
        self._frame_cache = {}
        animation = import_tgs(file_name)
        self.slider.setMinimum(animation.in_point)
        self.slider.setMaximum(animation.out_point)
        self.slider_spin.setMinimum(animation.in_point)
        self.slider_spin.setMaximum(animation.out_point)
        self.slider.setValue(animation.in_point)
        self.animation = animation
        self.display.setFixedSize(self.animation.width, self.animation.height)
        self._update_frame()
        self.setWindowTitle("Lottie Viewer - %s" % os.path.basename(file_name))

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

    window = LottieViewerWindow()
    window.resize(800, 600)
    if ns.file:
        window.open_file(ns.file)
    window.show()

    sys.exit(app.exec_())


