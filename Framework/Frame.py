from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

from framework.gui_module import GuiModule
from framework.app import App
import crawler.resources.resources


class Frame(QWidget):

    display = pyqtSignal(object)

    def __init__(self, path, next_frame_button_names=[]):
        super().__init__()
        loadUi(path, self)
        self.index = None
        for button_name in next_frame_button_names:
            button = getattr(self, button_name)
            button.pressed.connect(self.finalize)
        self.gui_modules = []
        self.display.connect(App.instance.selectFrame)

    def add_module(self, gui_module: GuiModule):
        self.gui_modules.append(gui_module)

    def show(self):
        for gui_module in self.gui_modules:
            gui_module.update()
        self.display.emit(self)

    def finalize(self):
        errors = self.get_module_errors()
        if errors:
            self.show_errors(errors)
        else:
            self.save_datapoints()
            next_frame = self.get_next_frame(self.sender())
            next_frame.show()

    def get_next_frame(self, sender):
        button_name = None
        for attribute, value in self.__dict__.items():
            if value is sender:
                button_name = str(attribute)
                break
        return self.decide_next_frame(button_name)

    def get_module_errors(self):
        errors = []
        for gui_module in self.gui_modules:
            if gui_module.error is not None:
                errors.append(gui_module.error)
        return errors

    def show_errors(self, errors):
        print(errors)

    def save_datapoints(self):
        for gui_module in self.gui_modules:
            gui_module.save_datapoint()

    def decide_next_frame(self):
        raise Exception(
            f"decideNextFrame method not implemented in {self.__class__.__name__}"
        )
