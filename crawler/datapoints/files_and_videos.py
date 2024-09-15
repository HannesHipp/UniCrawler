from framework.database import ReadableDatabase
from framework.datapoint import Datapoint


class FilesAndVideos(Datapoint):

    def __init__(self) -> None:
        super().__init__(
            ReadableDatabase('files_and_videos')
        )

    def from_database(self, stored_value):
        result = []
        if not stored_value:
            return result
        for tuple in stored_value:
            result.append(tuple[0])
        return result

    def to_database(self, files_and_videos):
        result = []
        for element in files_and_videos:
            result.append((element.url,))
        return result