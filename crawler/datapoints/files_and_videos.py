from framework.datapoint import Datapoint


class FilesAndVideos(Datapoint):

    def __init__(self) -> None:
        super().__init__()

    def tuple_list_to_value(self, tupleList):
        result = []
        for tuple in tupleList:
            result.append(tuple[0])
        return result

    def value_to_tuple_list(self, files_and_videos):
        result = []
        for element in files_and_videos:
            result.append((element.url,))
        return result