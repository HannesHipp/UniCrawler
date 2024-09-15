import os
import sys
from typing import Self
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QWidget, QStackedWidget


class App(QWidget):

    instance:Self|None = None

    def __init__(self):
        self.qApp = QApplication(sys.argv)
        super().__init__()
        # os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        self.stackedWidget = QStackedWidget()
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.stackedWidget)
        self.setFixedSize(800, 500)
        self.setLayout(mainLayout)
        App.instance = self
        self.frames = []
        self.show()

    def start_with(self, frame):
        frame.show()
        sys.exit(self.qApp.exec_())

    def add_frame(self, frame):
        self.frames.append(frame)
        self.stackedWidget.addWidget(frame)

    def select_frame(self, frame):
        if frame not in self.frames:
            self.add_frame(frame)
        index = self.frames.index(frame) + 1
        self.stackedWidget.setCurrentIndex(index)