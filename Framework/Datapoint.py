from PyQt5.QtCore import QObject, pyqtSignal
from framework.database import Database


class Datapoint(QObject):

    value_changed = pyqtSignal()
    invalidate = pyqtSignal()

    def __init__(self, database:Database|None = None) -> None:
        super().__init__()
        value = None
        if database:
            value = self.from_database(database.get())
        self.database = database
        self.value = value
        self.invalidate.connect(self._invalidate)

    def _set_value(self, value):
        self.value = value
        self.value_changed.emit()

    def submit_value(self, value):
        error = self.has_error(value)
        if not error:
            self._set_value(value)
        return error
    
    def _invalidate(self):
        self._set_value(None)

    def save_to_db(self):
        if self.database:
            self.database.save(
                self.to_database(self.value))

    def has_error(self, value):
        response = self.is_valid(value)
        if response is True:
            return None
        return response
    
    def is_valid(self, value):
        return True

    def from_database(self, stored_value):
        return stored_value

    def to_database(self, value):
        return value
