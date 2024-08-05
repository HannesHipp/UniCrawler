from framework.gui_modules.path_selector import PathSelector
from framework.frame import Frame


class PathSelectionFrame(Frame):

    def __init__(self, path):
        super().__init__(
            path="crawler\\resources\\path_selection_view.ui",
            next_frame_button_names=['button_continue']
        )
        self.path = path
        self.add_module(
            PathSelector(path, self.lineedit_path, self.button_select_path)
        )

    def addNextFrames(self, getCoursesFrame):
        self.getCoursesFrame = getCoursesFrame

    def decide_next_frame(self, pressedButton):
        return self.getCoursesFrame
