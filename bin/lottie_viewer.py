#!/usr/bin/env python3

import os
import sys
import signal
from io import StringIO

from PySide2 import QtCore, QtWidgets, QtGui, QtSvg

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.importers.core import import_tgs
from lottie.exporters.svg import export_svg


class LottieViewerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.animation = None
        self._frame_cache = {}

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
        self.layout_slider.addWidget(QtWidgets.QLabel("frame"))
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

    def _update_frame(self):
        if not self.animation:
            return

        frame = self.slider_spin.value()
        if frame in self._frame_cache:
            rendered = self._frame_cache[frame]
        else:
            file = StringIO()
            export_svg(self.animation, file, frame)
            rendered = file.getvalue().encode("utf-8")
            self._frame_cache[frame] = rendered

        self.display.load(rendered)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtWidgets.QApplication([])

    window = LottieViewerWindow()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())


