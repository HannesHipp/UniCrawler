from gui.frame import Frame


class EndFrame(Frame):

    def __init__(self):
        super().__init__(
            path="crawler\\resources\\ending_view.ui",
        )

    def decide_next_frame(self, pressedButton):
        return None