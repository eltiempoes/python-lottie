from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtWidgets import *


class SearchWidget(QWidget):
    frame_changed = Signal(int)

    def __init__(self, target):
        super().__init__()
        self.target = target

        layout_slider = QHBoxLayout()
        layout_slider.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout_slider)

        self.line_find = QLineEdit()
        self.line_find.setPlaceholderText("Find")
        self.line_find.returnPressed.connect(self.find_next)
        layout_slider.addWidget(self.line_find)

        self.line_replace = QLineEdit()
        self.line_replace.setPlaceholderText("Replace")
        self.line_replace.returnPressed.connect(self.replace)
        layout_slider.addWidget(self.line_replace)

        self.button_next = QPushButton()
        self.button_next.setIcon(QIcon.fromTheme("go-down-search"))
        self.button_next.clicked.connect(self.find_next)
        self.button_next.setToolTip("Next")
        layout_slider.addWidget(self.button_next)

        self.button_prev = QPushButton()
        self.button_prev.setIcon(QIcon.fromTheme("go-up-search"))
        self.button_prev.clicked.connect(self.find_prev)
        self.button_next.setToolTip("Previous")
        layout_slider.addWidget(self.button_prev)

        self.button_repl = QPushButton()
        self.button_repl.setText("Replace")
        self.button_repl.clicked.connect(self.replace)
        layout_slider.addWidget(self.button_repl)

        self.button_case = QPushButton()
        self.button_case.setCheckable(True)
        self.button_case.setIcon(QIcon.fromTheme("format-text-superscript"))
        self.button_case.setToolTip("Case Sensitive")
        layout_slider.addWidget(self.button_case)

        self.combo_mode = QComboBox()
        self.combo_mode.addItem("Text")
        self.combo_mode.addItem("RegExp")
        layout_slider.addWidget(self.combo_mode)

        self.button_selection = QPushButton()
        self.button_selection.setCheckable(True)
        self.button_selection.setIcon(QIcon.fromTheme("edit-select-all"))
        self.button_selection.setToolTip("Only in selection")
        layout_slider.addWidget(self.button_selection)

        self.set_replace_enabled(False)

    def start_search(self, replace):
        if self.target.hasSelectedText():
            st = self.target.selectedText()
            if "\n" in st:
                self.button_selection.setChecked(True)
            else:
                self.button_selection.setChecked(False)
                self.line_find.setText(st)
        self.line_find.selectAll()
        self.line_find.setFocus(True)
        self.set_replace_enabled(replace)

    def set_replace_enabled(self, show):
        #self.button_selection.setChecked(show != self.button_selection.isVisible())
        #self.button_selection.setVisible(show)
        self.line_replace.setVisible(show)
        self.button_repl.setVisible(show)

    def find(self, forward):
        func = self.target.findFirst if not self.button_selection.isChecked() else self.target.findFirstInSelection
        func(
            self.line_find.text(),
            self.combo_mode.currentIndex() != 0,
            self.button_case.isChecked(),
            False,
            True,
            forward,
            True
        )

    def find_next(self):
        return self.find(True)

    def find_prev(self):
        return self.find(False)

    def replace(self):
        self.target.replace(self.line_replace.text())
        self.find_next()
