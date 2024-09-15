from framework.database import ReadableDatabase
from framework.datapoint import Datapoint


class Courses(Datapoint):

    def __init__(self) -> None:
        super().__init__(
            ReadableDatabase('courses')
        )

    def from_database(self, stored_value: list[tuple]):
        result = {}
        if not stored_value:
            return result
        for tuple in stored_value:
            result[tuple[0]] = tuple[1]
        return result

    def to_database(self, courses):
        result = []
        for course in courses:
            result.append((
                course.get_hash(), 
                course.to_crawl
            ))
        return result


class Course:

    def __init__(self, element) -> None:
        self.element = element
        self.to_crawl = False
        self.is_new = False
        self.was_crawled = False

    @property
    def name(self):
        return self.element.name

    def get_hash(self):
        return self.element.url.split("crs_")[1].split(".html")[0]