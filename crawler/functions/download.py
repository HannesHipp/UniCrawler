import os
from gui.datapoint import Datapoint
from gui.function import Function

from crawler.datapoints.files import Files
from crawler.datapoints.path import Path
from crawler.session import Session




class Download(Function):

    def __init__(
            self, 
            path: Path,
            files: Files, 
            current_file: Datapoint,
            percentage_downloaded: Datapoint
        ) -> None:
        super().__init__()
        self.path = path
        self.files = files
        self.current_file = current_file
        self.percentage_downloaded = percentage_downloaded

    def execute(self):
        # shorten tree 

        # preprocess file paths
        # self.shorten_long_paths(self.files.value)
        # download files
        files_to_download = [file for file in self.files.value if not file.is_saved]
        for index, file in enumerate(files_to_download):
            self.current_file.submit_value(file.name)
            self.download(file.html_node)
            file.is_saved = True
            self.percentage_downloaded.submit_value(int((index+1)/len(files_to_download)*100))
        
    def download(self, item):
        path = self.get_path(item) 
        if not os.path.isdir(path.parent):
            os.makedirs(path.parent)
        with open(str(path) + '.pdf', 'wb') as file:
            file.write(Session.get_file_content(filter_url(item.url, item.url_format))) 

    def get_path(self, element):
        if element.parent is None:
            return self.path.value / filter_name(element.name)
        else:
            return self.get_path(element.parent) / filter_name(element.name)

    def shorten_long_paths(self, data):
        windows_path_length_limit = 240
        for item in data:
            while len(str(self.get_path(item)) + '.pdf') > windows_path_length_limit:  # Convert to string for length check
                item.parent = item.parent.parent

def filter_name(name):
    for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '...']:
        name = " ".join(name.split(char))
    return " ".join(name.split())

def filter_url(url, url_format:dict):
    if 'http' in url:
        return url
    for key in url_format.keys():
        if key in url:
            if url[:2] == "./":
                url = url[2:]
            url = url_format[key] + url
            break
    return url