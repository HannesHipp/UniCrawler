from framework.database import SecureDatabase
from framework.datapoint import Datapoint


class Password(Datapoint):

    def __init__(self) -> None:
        super().__init__(
            SecureDatabase('password')
        )

    def is_valid(self, value):
        if value:
            return True
        else:
            return "Das Passwort ist nicht korrekt."
