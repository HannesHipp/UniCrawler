from framework.function import Function

from crawler.datapoints.username import Username
from crawler.datapoints.password import Password
from crawler.session import Session


class ValidateLogin(Function):

    def __init__(self, username: Username, password: Password) -> None:
        super().__init__()
        self.username = username
        self.password = password

    def execute(self):
        if Session.set_session(self.username.value, self.password.value):
            return True
        else:
            self.username.reset_value()
            self.password.reset_value()
            raise Exception('Der Benutzername oder das Passwort ist falsch.')
