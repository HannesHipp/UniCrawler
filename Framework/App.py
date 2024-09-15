import os
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QWidget, QStackedWidget
from PyQt5.QtWidgets import QApplication

class App(QWidget):

    instance = None

    def __init__(self):
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        self.q_app = QApplication(sys.argv)
        super().__init__()
        self.stacked_widget = QStackedWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.stacked_widget)
        self.setFixedSize(800, 500)
        self.setLayout(main_layout)
        App.instance = self
        self.frames = []
        self.current_frame = None
        self.q_app.aboutToQuit.connect(self.on_exit)
        self.show()

    def start_with(self, frame):
        frame.show()
        try:
            sys.exit(self.q_app.exec_())
        except Exception as e:
            print(e)
            self.current_frame.save_datapoints()
            sys.exit(1)

    def add_frame(self, frame):
        self.frames.append(frame)
        self.stacked_widget.addWidget(frame)

    def select_frame(self, frame):
        if not frame in self.frames:
            self.add_frame(frame)
        index = self.frames.index(frame)
        self.stacked_widget.setCurrentIndex(index)
        self.current_frame = frame

    def on_exit(self):
        self.current_frame.save_datapoints()