from framework.output_frame import OutputFrame

from crawler.datapoints.password import Password
from crawler.datapoints.username import Username
from crawler.functions.validate_login import ValidateLogin


class LoginValidationFrame(OutputFrame):

    def __init__(self, username: Username, password: Password):
        super().__init__(
            path="crawler\\resources\\login_validation_view.ui",
            function=ValidateLogin(username, password)
        )
        self.username = username
        self.password = password

    def add_next_frames(self, loginFrame, pathFrame):
        self.loginFrame = loginFrame
        self.pathFrame = pathFrame

    def decide_next_frame(self, pressedButton):
        if self.function.error:
            return self.loginFrame
        return self.pathFrame
