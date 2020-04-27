from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtWidgets import *


class TimelineWidget(QWidget):
    frame_changed = Signal(int)

    def __init__(self):
        super().__init__()
        layout_slider = QHBoxLayout()
        layout_slider.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout_slider)
        self.button_play = QPushButton()
        self.button_play.setCheckable(True)
        self.button_play.toggled.connect(self.play_toggle)
        layout_slider.addWidget(self.button_play)
        self.slider = QSlider(Qt.Horizontal)
        layout_slider.addWidget(self.slider)
        self.slider_spin = QSpinBox()
        layout_slider.addWidget(self.slider_spin)
        self.slider.valueChanged.connect(self.slider_spin.setValue)
        self.slider_spin.valueChanged.connect(self.slider.setValue)
        self.slider.valueChanged.connect(self.frame_changed)

        self.framerate = 60
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._next_frame)
        self.stop()

        self._min = 0
        self._max = 99

    def set_min_max(self, min, max):
        self._min = min
        self._max = max
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.slider_spin.setMinimum(min)
        self.slider_spin.setMaximum(max)

    @Slot(int)
    def set_frame(self, frame):
        self.slider.setValue(frame)

    @property
    def frame(self):
        return self.slider.value()

    def _next_frame(self):
        nf = self.frame + 1
        if nf > self._max:
            nf = self._min
        self.slider.setValue(nf)

    @Slot()
    def stop(self):
        self.timer.stop()
        self.button_play.setIcon(QIcon.fromTheme("media-playback-start"))
        self.button_play.setText("Play")
        self.button_play.setChecked(False)

    @Slot()
    def play(self):
        if not self.isEnabled():
            self.stop()
            return

        self.button_play.setIcon(QIcon.fromTheme("media-playback-stop"))
        self.button_play.setText("Stop")

        self.timer.start(1000/self.fps)

    @Slot(bool)
    def play_toggle(self, play):
        if play:
            self.play()
        else:
            self.stop()
