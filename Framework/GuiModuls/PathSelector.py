from pathlib import Path
from Framework.Datapoint import Datapoint
from PyQt5.QtWidgets import QLabel, QPushButton, QFileDialog
from Framework.GuiModuls.GuiModul import GuiModul


class PathSelector(GuiModul):

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
