from framework.app import App

from crawler.datapoints.username import Username
from crawler.datapoints.password import Password
from crawler.datapoints.courses import Courses
from crawler.datapoints.files_and_videos import FilesAndVideos
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
files_and_videos = FilesAndVideos()


login_frame = LoginFrame(username, password)
login_validation_frame = LoginValidationFrame(username, password)
path_frame = PathSelectionFrame(path)
get_courses_frame = GetCoursesFrame(username, password, courses, autostart)
course_selection_frame = CourseSelectionFrame(courses)
autostart_frame = AutostartFrame()
crawling_frame = CrawlingFrame(courses, files_and_videos)
downloading_frame = DownloadingFrame(path, files_and_videos)
success_frame = EndFrame()


login_frame.addNextFrames(login_validation_frame)
login_validation_frame.addNextFrames(login_frame, path_frame)
path_frame.addNextFrames(get_courses_frame)
get_courses_frame.addNextFrames(course_selection_frame, autostart_frame)
course_selection_frame.addNextFrames(crawling_frame)
autostart_frame.addNextFrames(course_selection_frame, crawling_frame)
crawling_frame.add_next_frames(downloading_frame)
downloading_frame.add_next_frames(success_frame)

if username.value and password.value and path.value:
    app.startWith(get_courses_frame)
else:
    app.startWith(login_frame)

# TO-DO
    # Herruntergeladene Items werden nicht gespeichert
    # Auflösung Laptop Michi
    # Verkehrstechnik nicht vollständig
    # Kurse Ausklappmenü
    # 