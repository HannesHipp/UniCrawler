from PyQt5.QtWidgets import QLineEdit
from framework.datapoint import Datapoint
from framework.gui_modules.gui_module import GuiModule


class TextField(GuiModule):

    def __init__(self, datapoint: Datapoint, qtTextEdit: QLineEdit) -> None:
        super().__init__(
            datapoint=datapoint, 
            changed_signal=qtTextEdit.textChanged
        )
        self.qtTextEdit = qtTextEdit

    def get_value(self):
        return self.qtTextEdit.text()

    def set_value(self, value):
        self.qtTextEdit.setText(value)
