from crawler.extraction.html_node import HtmlNode
from framework.frame import Frame
from crawler.datapoints.courses import Course, Courses


class CourseSelectionFrame(Frame):

    def __init__(self, courses: Courses):
        super().__init__(
            path="crawler\\resources\\course_selection_view.ui",
            datapoints=[courses],
            next_frame_button_names=['button_select_choice']
        )
        self.courses = courses
        self.add_module(
            CustomTreeView(courses, self.tree_view)
        )

    def add_next_frames(self, crawlingFrame):
        self.crawlingFrame = crawlingFrame

    def decide_next_frame(self, pressedButton):
        return self.crawlingFrame
    

from PyQt5.QtWidgets import QTreeView
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor, QFont

from framework.gui_module import GuiModule
import re


class CustomTreeView(GuiModule):

    def __init__(self, courses: Courses, tree_view: QTreeView) -> None:
        self.model = QStandardItemModel()
        super().__init__(
            datapoint=courses,
            changed_signal=self.model.dataChanged
        )
        self.model.itemChanged.connect(self._update_checkboxes)
        self.tree_view = tree_view
        self.tree_view.setModel(self.model)
        self.tree_view.setHeaderHidden(True) 

    def get_value(self):
        result = []
        for semester_index in range(self.model.rowCount()):
            semester_item = self.model.item(semester_index)
            for course_index in range(semester_item.rowCount()):
                course_item = semester_item.child(course_index)
                course = course_item.data()
                if course_item.checkState() == Qt.Checked:
                    course.to_crawl = True
                else:
                    course.to_crawl = False
                result.append(course)
        return result

    def set_value(self, courses: list[Course]):
        # set value only once
        if self.model.rowCount() > 0: 
            return
        semester_nodes_to_items = {}
        bold_font = QFont()
        bold_font.setBold(True)
        bold_font.setPointSize(10)
        for course in courses:
            semester_node = course.semester_node
            if semester_node not in semester_nodes_to_items:
                semester_item = QStandardItem(semester_node.name)
                semester_item.setCheckable(True)
                semester_item.setEditable(False)
                semester_item.setFont(bold_font)
                semester_nodes_to_items[semester_node] = semester_item
        
        semester_nodes_to_items = sort_semester_nodes_to_items(semester_nodes_to_items)

        for course in sorted(courses, key=lambda course: course.name):
            semester_item = semester_nodes_to_items[course.semester_node]
            course_item = QStandardItem(course.name)
            course_item.setData(course)
            course_item.setCheckable(True)
            course_item.setEditable(False)
            course_item.setCheckState(Qt.Unchecked)
            if course.to_crawl:
                course_item.setCheckState(Qt.Checked)
            if course.is_new:
                course_item.setBackground(QBrush(QColor(113, 217, 140)))
                semester_item.insertRow(0, course_item)
            else:
                semester_item.appendRow(course_item)

        for semester_item in semester_nodes_to_items.values():
            semester_item.setCheckState(get_parent_checkbox_state(semester_item))
            self.model.appendRow(semester_item)
            semester_index = self.model.indexFromItem(semester_item) 
            self.tree_view.expand(semester_index)


    def _update_checkboxes(self, changed_item):
        if self.model.blockSignals(True): 
            return 

        if not changed_item.parent(): 
            # changed item is a semester_item
            for row in range(changed_item.rowCount()):
                child = changed_item.child(row)
                child.setCheckState(changed_item.checkState())
        else: 
            # changed item is a course_item
            parent = changed_item.parent()
            parent.setCheckState(get_parent_checkbox_state(parent))

        self.model.blockSignals(False) 

        self.update()

def get_parent_checkbox_state(parent):
    all_checked = all(parent.child(i).checkState() == Qt.Checked 
                      for i in range(parent.rowCount()))
    return Qt.Checked if all_checked else Qt.Unchecked

def sort_semester_nodes_to_items(semester_nodes_to_items: dict[HtmlNode,QStandardItem]):

    def extract_sort_key(semester_node):
        name = semester_node.name
        # Extract season
        season = "Sommer" if "Sommer" in name else "Winter"
        # Extract the 4-digit year
        year_match = re.search(r'(\d{4})', name)
        year = int(year_match.group(1)) if year_match else 0
        # Return tuple for sorting: (year, 0 for Sommer, 1 for Winter)
        return (year, 0 if season == "Sommer" else 1)
    
    sorted_semester_nodes = sorted(semester_nodes_to_items.keys(), key=extract_sort_key, reverse=True)
    return {semester_node: semester_nodes_to_items[semester_node] for semester_node in sorted_semester_nodes}