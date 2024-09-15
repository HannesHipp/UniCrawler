from framework.datapoint import Datapoint


class Course:

    @staticmethod
    def get_hash(url):
        return url.split("crs_")[1].split(".html")[0]

    def __init__(self, hash, to_download, is_new) -> None:
        self.hash = hash
        self.to_download = to_download
        self.is_new = is_new
        self.element = None
        self.was_crawled = False

    @property
    def name(self):
        return self.element.name


class Courses(Datapoint):

    def tuple_list_to_value(self, tuple_list: list[tuple]):
        result = []
        for tuple in tuple_list:
            result.append(Course(tuple[0], tuple[1], False))
        return result

    def value_to_tuple_list(self, courses: list[Course]):
        result = []
        for course in courses:
            result.append((course.hash, course.to_download))
        return result


