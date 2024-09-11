from PyQt5.QtWidgets import QProgressBar, QLabel
from framework.datapoint import Datapoint
from framework.gui_module import GuiModule


class ProgressBar(GuiModule):

    def __init__(self, percentage: Datapoint, qtProgressBar: QProgressBar, qtPercentageLabel: QLabel) -> None:
        super().__init__(
            datapoint=percentage
        )
        self.qtProgressbar = qtProgressBar
        self.qtPercentageLabel = qtPercentageLabel

    def set_value(self, value):
        if not value:
            value = 0
        self.qtPercentageLabel.setText(str(value))
        self.qtProgressbar.setValue(value)
