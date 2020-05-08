import io
import sys
import parser
import inspect
import traceback
import contextlib

from PyQt5.QtWidgets import *


class Console(QWidget):
    def __init__(self, *a):
        super().__init__(*a)
        self.context_global = {}
        self.context_local = {}

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.lines = QPlainTextEdit()
        self.lines.setReadOnly(True)
        layout.addWidget(self.lines)

        self.input = QLineEdit()
        self.input.returnPressed.connect(self.on_input)
        layout.addWidget(self.input)

    def set_font(self, font):
        self.lines.setFont(font)
        self.input.setFont(font)

    def define(self, name, value):
        self.context_global[name] = value

    def on_input(self):
        self.eval(self.input.text())
        self.input.clear()

    def eval(self, line):
        self.lines.appendPlainText(">>> " + line)

        try:
            try:
                expression = True
                code = compile(line, "<console>", "eval")
            except SyntaxError:
                expression = False
                code = compile(line, "<console>", "single")

            sterrout = io.StringIO()
            with contextlib.redirect_stderr(sterrout):
                with contextlib.redirect_stdout(sterrout):
                    if expression:
                        value = eval(code, self.context_global, self.context_local)
                    else:
                        value = None
                        exec(code, self.context_global, self.context_local)

            stdstreams = sterrout.getvalue()
            if stdstreams:
                if stdstreams.endswith("\n"):
                    stdstreams = stdstreams[:-1]
                self.lines.appendPlainText(stdstreams)
            if value is not None:
                self.lines.appendPlainText(repr(value))
        except Exception:
            etype, value, tb = sys.exc_info()
            # Find how many frames to print to hide the current frame and above
            parent = inspect.currentframe().f_back
            i = 0
            for frame, ln in traceback.walk_tb(tb):
                i += 1
                if frame.f_back == parent:
                    i = 0

            file = io.StringIO()
            traceback.print_exception(etype, value, tb, limit=-i, file=file)
            self.lines.appendPlainText(file.getvalue())

        self.lines.verticalScrollBar().setValue(self.lines.verticalScrollBar().maximum())
