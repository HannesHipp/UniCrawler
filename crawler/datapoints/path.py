import pathlib
from gui.database import ReadableDatabase
from gui.datapoint import Datapoint


class Path(Datapoint):

    def __init__(self) -> None:
        super().__init__(
            ReadableDatabase('path')
        )

    def is_valid(self, value):
        if value:
            return True
        else:
            return "Es muss ein Pfad ausgewählt werden."
        
    def from_database(self, stored_value):
        if not stored_value:
            return None
        return pathlib.Path(stored_value)

    def to_database(self, path):
        return str(path)
