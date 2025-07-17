from PyQt5.QtCore import QObject, pyqtSignal
from gui.database import Database


class Datapoint(QObject):

    value_changed = pyqtSignal()

    def __init__(self, database:Database|None = None) -> None:
        super().__init__()
        value = None
        if database:
            value = self.from_database(database.get())
        self.database = database
        self.value = value

    def _set_value(self, value):
        if value == self.value:
            return
        self.value = value
        self.value_changed.emit()

    def submit_value(self, value):
        response = self.is_valid(value)
        if response is True:
            self._set_value(value)
            return None
        return response
    
    def invalidate(self):
        self._set_value(None)

    def save_value(self):
        if self.database:
            self.database.save(
                self.to_database(self.value))

    def is_valid(self, value):
        return True

    def from_database(self, stored_value):
        return stored_value

    def to_database(self, value):
        return value
