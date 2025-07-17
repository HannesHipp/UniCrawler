from gui.app import App

from crawler.datapoints.username import Username
from crawler.datapoints.password import Password
from crawler.datapoints.courses import Courses
from crawler.datapoints.files import Files
from crawler.datapoints.path import Path
from crawler.datapoints.autostart import Autostart

from crawler.frames.crawling_frame import CrawlingFrame
from crawler.frames.downloading_frame import DownloadingFrame
from crawler.frames.login_frame import LoginFrame
from crawler.frames.login_validation_frame import LoginValidationFrame
from crawler.frames.path_selection_frame import PathSelectionFrame
from crawler.frames.get_courses_frame import GetCoursesFrame
from crawler.frames.course_selection_frame import CourseSelectionFrame
from crawler.frames.autostart_frame import AutostartFrame
from crawler.frames.end_frame import EndFrame

app = App()

username = Username()
password = Password()
path = Path()
courses = Courses()
autostart = Autostart()
autostart.submit_value(True)
files = Files()


login_frame = LoginFrame(username, password)
login_validation_frame = LoginValidationFrame(username, password)
path_frame = PathSelectionFrame(path)
get_courses_frame = GetCoursesFrame(username, password, courses, autostart)
course_selection_frame = CourseSelectionFrame(courses)
autostart_frame = AutostartFrame()
crawling_frame = CrawlingFrame(courses, files)
downloading_frame = DownloadingFrame(path, files)
success_frame = EndFrame()


login_frame.add_next_frames(login_validation_frame)
login_validation_frame.add_next_frames(login_frame, path_frame)
path_frame.add_next_frames(get_courses_frame)
get_courses_frame.add_next_frames(course_selection_frame, autostart_frame)
course_selection_frame.add_next_frames(crawling_frame)
autostart_frame.add_next_frames(course_selection_frame, crawling_frame)
crawling_frame.add_next_frames(downloading_frame)
downloading_frame.add_next_frames(success_frame)

if username.value and password.value and path.value:
    app.start_with(get_courses_frame)
else:
    app.start_with(login_frame)

# TO-DO
    # Auflösung Laptop Michi
    # Verkehrstechnik nicht vollständig
    # Kurse Ausklappmenü
    # tree-importance einbeziehen und redundante Ordner löschen
    # Shorten Pathlength