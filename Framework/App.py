import os
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QWidget, QStackedWidget
from PyQt5.QtWidgets import QApplication

class App(QWidget):

    instance = None

    def __init__(self):
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        self.qApp = QApplication(sys.argv)
        super().__init__()
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

    def selectFrame(self, frame):
        if not frame in self.frames:
            self.add_frame(frame)
        index = self.frames.index(frame)
        self.stackedWidget.setCurrentIndex(index)
