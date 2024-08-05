from pathlib import Path
from PyQt5.QtWidgets import QLabel, QPushButton, QFileDialog
from framework.datapoint import Datapoint
from framework.gui_modules.gui_module import GuiModule


class PathSelector(GuiModule):

    def __init__(self, datapoint: Datapoint, line_edit: QLabel, button: QPushButton) -> None:
        super().__init__(
            datapoint=datapoint,
            changed_signal=button.clicked
        )
        self.line_edit = line_edit

    def get_value(self):
        value = QFileDialog.getExistingDirectory(None, "Ordner auswählen")
        value = Path(value)
        self.set_value(value)
        return value

    def set_value(self, value):
        self.line_edit.setText(str(value))
