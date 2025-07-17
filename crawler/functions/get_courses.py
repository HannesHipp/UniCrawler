import re
from crawler.extraction.html_node import HtmlNode
from crawler.functions.download import filter_url
from gui.function import Function

from crawler.datapoints.courses import Courses, Course
from crawler.datapoints.username import Username
from crawler.datapoints.password import Password
from crawler.extraction.extractor import Extractor
from crawler.session import Session


class GetCourses(Function):

    def __init__(self, username: Username, password: Password, courses: Courses) -> None:
        super().__init__()
        self.username = username
        self.password = password
        self.courses = courses

    def execute(self):
        COURSES_URL = 'https://ilias3.uni-stuttgart.de/ilias.php?baseClass=ildashboardgui&cmd=show&view=1'
        Session.set_session(self.username.value, self.password.value)
        extractor = Extractor('crawler\\models\\ilias')
        root = extractor.root_type(None)
        root.name = 'Ilias'
        root.set_soup(Session.get_content(COURSES_URL))
        course_elements:list[HtmlNode] = extract_course_items(root, extractor)

        saved_courses:list[Course] = self.courses.value
        all_courses = []
        for course_element in course_elements:
            is_new = True
            for saved_course in saved_courses:
                if saved_course.get_hash() == course_element.get_hash():
                    saved_course.html_node = course_element
                    all_courses.append(saved_course)
                    is_new = False
                    break
            if is_new:
                new_course = Course(
                    html_node=course_element,
                    to_crawl=False, 
                    is_new=True
                )
                all_courses.append(new_course)
        
        unify_semesters(all_courses)

        self.courses.submit_value(all_courses)

def extract_course_items(root:HtmlNode, extractor:Extractor):
    course_pages = extractor.crawl_node(root)
    courses = []
    for course_page in course_pages:
        course_page.set_soup(
            Session.get_content(
                filter_url(course_page.url, course_page.url_format)
            ))
        courses.extend(extractor.crawl_node(course_page))
    # remove course pages from tree
    for course in courses:
        course.parent.parent = root
    return courses

def unify_semesters(courses: list[Course]):
    root = courses[0].html_node.parent.parent
    semesters = {} 
    other_semester = HtmlNode(root)
    other_semester.name = 'Andere'
    for course in courses:
        course_element = course.html_node
        semester_name = extract_season_and_year(course_element.parent.name)
        if semester_name is None:
            course_element.parent = other_semester
            continue
        if semester_name not in semesters:
            new_semester = HtmlNode(root)
            new_semester.name = semester_name
            semesters[semester_name] = new_semester
        course_element.parent = semesters[semester_name]

def extract_season_and_year(name):
    year_match = re.search(r'\d{4}/\d{2}|\d{4}', name)
    if year_match:
        year = year_match.group()
        if 'Winter' in name:
            return f'Winter {year}'
        elif 'Sommer' in name:
            return f'Sommer {year}'
    return None