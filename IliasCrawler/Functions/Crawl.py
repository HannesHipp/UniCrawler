import time
from Framework.Datapoint import Datapoint
from Framework.Function import Function
from IliasCrawler.Datapoints.Courses import Courses
from IliasCrawler.Datapoints.FilesAndVideos import FilesAndVideos
from IliasCrawler.Functions.Download import filter_url
from IliasCrawler.Session import Session
from IliasCrawler.extractor.extractor import Extractor
from IliasCrawler.extractor.html_node import HtmlNode


class Crawl(Function):

    def __init__(
            self, 
            courses: Courses, 
            files_and_videos: FilesAndVideos, 
            current_course_name: Datapoint,
            percentage_crawled: Datapoint
        ) -> None:
        super().__init__()
        self.courses = courses
        self.files_and_videos = files_and_videos
        self.current_courses_name = current_course_name
        self.percentage_crawled = percentage_crawled

    def execute(self):
        files_and_videos = []
        extractor = Extractor('IliasCrawler\\models\\ilias')
        to_crawl = [course.element for course in self.courses.value if course.to_download]
        crawled = 0
        for course in to_crawl:
            self.current_courses_name.submit_value(course.name)
            files_and_videos += self.crawl_page(course, extractor)
            crawled += 1
            self.percentage_crawled.submit_value(
                int(crawled/len(to_crawl)*100)
            )
        result = []
        existing_files_and_videos = self.files_and_videos.value
        for element in files_and_videos:
            if not element.url in existing_files_and_videos:
                result.append(element)
        self.files_and_videos.submit_value(result)
    
    def crawl_page(self, page:HtmlNode, extractor: Extractor):
        result = []
        page.set_soup(Session.get_content(filter_url(page.url, page.url_format)))
        pages = extractor.crawl_node(page)
        for page in pages:
            if type(page).child_types:
                result.extend(self.crawl_page(page, extractor))
            else:
                result.append(page)
        return result