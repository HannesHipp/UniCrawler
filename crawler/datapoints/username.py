from gui.database import ReadableDatabase
from gui.datapoint import Datapoint


class Username(Datapoint):

    def __init__(self) -> None:
        super().__init__(
            ReadableDatabase('username')
        )

    def is_valid(self, value):
        if value:
            return True
        else:
            return "Der Benutzername ist nicht korrekt."
