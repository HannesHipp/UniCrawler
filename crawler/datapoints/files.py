from crawler.extraction.html_node import HtmlNode
from crawler.models.ilias.ilias import File as IliasFile
from gui.database import ReadableDatabase
from gui.datapoint import Datapoint

class File:

    def __init__(self, 
                 html_node = None, 
                 hash = None, 
                 is_saved = False
                 ) -> None:
        self.html_node:HtmlNode = html_node
        self.hash = hash
        self.is_saved = is_saved
    
    @property
    def name(self):
        return self.html_node.name
        
    def get_hash(self):
        if self.hash:
            return self.hash
        return self.html_node.get_hash()


class Files(Datapoint):

    def __init__(self) -> None:
        super().__init__(
            ReadableDatabase('files')
        )

    def from_database(self, stored_value):
        result = []
        if not stored_value:
            return result
        for hash in stored_value:
            result.append(File(hash=hash, is_saved=True))
        return result

    def to_database(self, files:list[File]):
        result = []
        for file in files:
            if file.is_saved:
                result.append(file.get_hash())
        return result