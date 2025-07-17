from gui.gui_modules.text_label import TextLabel
from gui.output_frame import OutputFrame
from gui.function import Function
from gui.datapoint import Datapoint
from time import sleep


class AutostartFrame(OutputFrame):

    def __init__(self):
        autostartTimer = Datapoint()
        super().__init__(
            path="crawler\\resources\\autostart_view.ui",
            function=AutostartCountdown(autostartTimer),
            cancel_button_name='button_cancel'
        )
        self.add_module(
            TextLabel(autostartTimer,  self.label_timer, lambda x: x)
        )

    def add_next_frames(self, courseSelectionFrame, crawlingFrame):
        self.courseSelectionFrame = courseSelectionFrame
        self.crawlingFrame = crawlingFrame

    def decide_next_frame(self, pressed_button):
        if self.function.canceled:
            return self.courseSelectionFrame
        return self.crawlingFrame


class AutostartCountdown(Function):

    def __init__(self, timer: Datapoint) -> None:
        super().__init__()
        self.timer = timer

    def execute(self):
        time = 10
        while time != 0 and not self.canceled:
            self.timer.submit_value(time)
            sleep(1.0)
            time = time - 1