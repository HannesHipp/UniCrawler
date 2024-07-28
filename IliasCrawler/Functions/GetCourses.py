from Framework.Function import Function
from IliasCrawler.Datapoints.Courses import Courses, Course
from IliasCrawler.Datapoints.Username import Username
from IliasCrawler.Datapoints.Password import Password
from IliasCrawler.Session import Session
from IliasCrawler.extractor.extractor import Extractor


class GetCourses(Function):

    def __init__(self, username: Username, password: Password, courses: Courses) -> None:
        super().__init__()
        self.username = username
        self.password = password
        self.courses = courses

    def execute(self):
        COURSES_URL = 'https://ilias3.uni-stuttgart.de/ilias.php?baseClass=ildashboardgui&cmd=show&view=1'
        Session.set_session(self.username.value, self.password.value)
        extractor = Extractor('IliasCrawler\\models\\ilias')
        root = extractor.root_type(None)
        root.name = 'Ilias'
        root.set_soup(Session.get_content(COURSES_URL))
        course_elements = extractor.crawl_node(root)

        old_courses = self.courses.value
        current_courses = []
        for course_element in course_elements:
            current_course = Course(course_element)
            if (hash:=current_course.get_hash()) in old_courses:
                current_course.to_download = old_courses[hash]
            else:
                current_course.is_new = True
            current_courses.append(current_course)
        self.courses.submit_value(current_courses)