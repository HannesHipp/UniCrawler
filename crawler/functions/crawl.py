from gui.datapoint import Datapoint
from gui.function import Function

from crawler.extraction.html_node import HtmlNode
from crawler.functions.download import filter_url
from crawler.session import Session
from crawler.extraction.extractor import Extractor
from crawler.datapoints.courses import Courses
from crawler.datapoints.files import File, Files


class Crawl(Function):

    def __init__(
            self, 
            courses: Courses, 
            files: Files, 
            current_course_name: Datapoint,
            percentage_crawled: Datapoint
        ) -> None:
        super().__init__()
        self.courses = courses
        self.files = files
        self.current_courses_name = current_course_name
        self.percentage_crawled = percentage_crawled

    def execute(self):
        crawled_file_nodes = []
        extractor = Extractor('crawler\\models\\ilias')
        courses_to_crawl = [course for course in self.courses.value if course.to_crawl]
        for index, course in enumerate(courses_to_crawl):
            self.current_courses_name.submit_value(course.name)
            crawled_file_nodes += self.crawl_page(course.html_node, extractor)
            self.percentage_crawled.submit_value(
                int((index+1)/len(courses_to_crawl)*100)
            )
        all_files = self.add_new_files(crawled_file_nodes)
        self.files.submit_value(all_files)
    
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
    
    def add_new_files(self, crawled_file_nodes: list[HtmlNode]):
        new_files = []
        existing_files:list[File] = self.files.value
        for file_node in crawled_file_nodes:
            is_new = True
            for existing_file in existing_files:
                if file_node.get_hash() == existing_file.get_hash():
                    is_new = False
                    break
            if is_new:
                new_files.append(File(html_node=file_node, is_saved=False))
        return existing_files + new_files