from framework.datapoint import Datapoint
from framework.gui_modules.progress_bar import ProgressBar
from framework.gui_modules.text_label import TextLabel
from framework.output_frame import OutputFrame

from crawler.datapoints.files import Files
from crawler.datapoints.path import Path
from crawler.functions.download import Download


class DownloadingFrame(OutputFrame):

    def __init__(self, path: Path, files: Files):
        current_file = Datapoint()
        percentage_downloaded = Datapoint()
        function = Download(path, files, current_file, percentage_downloaded)
        super().__init__(
            path="crawler\\resources\\downloading_view.ui",
            datapoints=[path, files],
            function=function
        )
        self.path = path
        self.files = files
        self.add_module(
            ProgressBar(percentage_downloaded, self.progress_bar, self.label_percentage)
        )
        self.add_module(
            TextLabel(current_file, self.label_current_file_name, lambda x: x)
        )

    def add_next_frames(self, success_frame):
        self.success_frame = success_frame

    def decide_next_frame(self, pressedButton):
        return self.success_frame
