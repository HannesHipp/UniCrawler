from typing import Self
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal

from framework.datapoint import Datapoint
from framework.gui_module import GuiModule
from framework.app import App
import crawler.resources.resources


class Frame(QWidget):

    display = pyqtSignal(object)

    def __init__(self, path, datapoints:list[Datapoint] = [], next_frame_button_names:list[str] = []):
        super().__init__()
        loadUi(path, self)
        self.datapoints = datapoints
        for button_name in next_frame_button_names:
            button = getattr(self, button_name)
            button.pressed.connect(self.finalize)
        self.gui_modules = []
        self.display.connect(App.instance.select_frame)

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
            return
        self.save_datapoints()
        pressed_btn_name = self.get_attr_name(self.sender())
        next_frame = self.decide_next_frame(pressed_btn_name)
        next_frame.show()

    def get_attr_name(self, attr_value) -> str:
        for attr_name, value in self.__dict__.items():
            if value is attr_value:
                return attr_name
        raise Exception(f"Object {attr_value} not found in {self.__class__.__name__}")

    def get_module_errors(self):
        errors = []
        for gui_module in self.gui_modules:
            if gui_module.error is not None:
                errors.append(gui_module.error)
        return errors

    def show_errors(self, errors):
        print(errors)

    def save_datapoints(self):
        for datapoint in self.datapoints:
            datapoint.save_value()	

    def decide_next_frame(self, pressed_button_name) -> Self:
        raise Exception(
            f"decide_next_frame method not implemented in {self.__class__.__name__}"
        )
