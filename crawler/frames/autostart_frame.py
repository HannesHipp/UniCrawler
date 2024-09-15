from framework.gui_modules.text_label import TextLabel
from framework.output_frame import OutputFrame
from framework.function import Function
from framework.datapoint import Datapoint
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

    def addNextFrames(self, courseSelectionFrame, crawlingFrame):
        self.courseSelectionFrame = courseSelectionFrame
        self.crawlingFrame = crawlingFrame

    def decide_next_frame(self, pressedButton):
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