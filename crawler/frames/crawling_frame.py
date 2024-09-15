from framework.datapoint import Datapoint
from framework.gui_modules.progress_bar import ProgressBar
from framework.gui_modules.text_label import TextLabel
from framework.output_frame import OutputFrame

from crawler.datapoints.courses import Courses
from crawler.datapoints.files import Files
from crawler.functions.crawl import Crawl


class CrawlingFrame(OutputFrame):

    def __init__(self, courses: Courses, files: Files):
        current_course_name = Datapoint()
        percentage_crawled = Datapoint()
        function = Crawl(courses, files, current_course_name, percentage_crawled)
        super().__init__(
            path="crawler\\resources\\crawling_view.ui",
            datapoints=[courses, files],
            function=function
        )
        self.courses = courses
        self.files = files
        self.add_module(
            ProgressBar(percentage_crawled, self.progress_bar, self.label_percentage)
        )
        self.add_module(
            TextLabel(current_course_name, self.label_current_course_name, lambda x: x)
        )

    def add_next_frames(self, downloading_frame):
        self.downloading_frame = downloading_frame

    def decide_next_frame(self, pressedButton):
        return self.downloading_frame
