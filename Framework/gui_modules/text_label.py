from PyQt5.QtWidgets import QLabel
from framework.datapoint import Datapoint
from framework.gui_module import GuiModule


class TextLabel(GuiModule):

    def __init__(self, datapoint: Datapoint, qtLabel: QLabel, func) -> None:
        super().__init__(
            datapoint=datapoint
        )
        self.qtLabel = qtLabel
        self.func = func

    def set_value(self, value):
        self.qtLabel.setText(str(self.func(value)))
