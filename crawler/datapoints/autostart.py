from framework.database import ReadableDatabase
from framework.datapoint import Datapoint


class Autostart(Datapoint):

    def __init__(self) -> None:
        super().__init__(
            ReadableDatabase('autostart')
        )

    def is_valid(self, value):
        return True
