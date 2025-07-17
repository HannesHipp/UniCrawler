from crawler.extraction.html_node import HtmlNode
from gui.database import ReadableDatabase
from gui.datapoint import Datapoint

class Course:

    def __init__(self, 
                 html_node = None, 
                 hash = None, 
                 to_crawl = False, 
                 is_new = False
                 ) -> None:
        self.html_node:HtmlNode = html_node
        self.hash = hash
        self.to_crawl = to_crawl
        self.is_new = is_new

    @property
    def name(self):
        return self.html_node.name
    
    @property
    def semester_node(self):
        return self.html_node.parent

    def get_hash(self):
        if self.hash:
            return self.hash
        return self.html_node.get_hash()


class Courses(Datapoint):

    def __init__(self) -> None:
        super().__init__(
            ReadableDatabase('courses')
        )

    def from_database(self, stored_value: list[tuple]):
        result = []
        if not stored_value:
            return result
        for tuple in stored_value:
            result.append(
                Course(
                    hash=tuple[0], 
                    to_crawl=tuple[1],
                    is_new=False
                )
            )
        return result

    def to_database(self, courses:list[Course]):
        result = []
        for course in courses:
            result.append((
                course.get_hash(), 
                course.to_crawl
            ))
        return result