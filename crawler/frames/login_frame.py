from framework.frame import Frame
from framework.gui_modules.text_field import TextField


class LoginFrame(Frame):

    def __init__(self, username, password):
        super().__init__(
            path="crawler\\resources\\login_view.ui",
            datapoints=[username, password],
            next_frame_button_names=['button_login']
        )
        self.username = username
        self.password = password
        self.add_module(TextField(username, self.textfield_username))
        self.add_module(TextField(password, self.textfield_password))

    def add_next_frames(self, loginValidationFrame):
        self.loginValidationFrame = loginValidationFrame

    def decide_next_frame(self, pressedButton):
        return self.loginValidationFrame
