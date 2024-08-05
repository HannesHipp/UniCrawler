from framework.gui_modules.obj_selection_list import ObjSelectionList
from framework.frame import Frame

from crawler.datapoints.courses import Courses


class CourseSelectionFrame(Frame):

    def __init__(self, courses: Courses):
        super().__init__(
            path="crawler\\resources\\course_selection_view.ui",
            next_frame_button_names=['button_select_choice']
        )
        self.courses = courses
        self.add_module(
            ObjSelectionList(
                courses, 
                self.listView,
                'name', 
                "to_download", 
                "is_new"
            )
        )

    def addNextFrames(self, crawlingFrame):
        self.crawlingFrame = crawlingFrame

    def decide_next_frame(self, pressedButton):
        return self.crawlingFrame
