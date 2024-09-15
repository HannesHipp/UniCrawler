from PyQt5.QtCore import QObject, pyqtSignal
from framework.database import Database


class Datapoint(QObject):

    value_changed = pyqtSignal()

    def __init__(self, database: Database = None) -> None:
        super().__init__()
        self.value = None
        self.database = database
        if database:
            self.value = self.from_database(database.get())

    def _set_value(self, value):
        self.value = value
        self.value_changed.emit()

    def submit_value(self, value):
        if value == self.value:
            return
        validation_result = self.is_valid(value)
        if validation_result is True:
            self._set_value(value)
        else:
            raise ValidationError(validation_result)

    def reset_value(self):
        self._set_value(None)
    
    def is_valid(self, value):
        return True
    
    def save_value(self):
        if self.database:
            self.database.save(self.to_database(self.value))
    
    def from_database(self, value):
        raise Exception(
            f"from_database() method not implemented for {self.__class__.__name__}"
        )

    def to_database(self, value):
        raise Exception(
            f"to_database() method not implemented for {self.__class__.__name__}"
        )

class ValidationError(Exception):
    pass