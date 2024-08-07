import os
from framework.datapoint import Datapoint
from framework.function import Function

from crawler.datapoints.files_and_videos import FilesAndVideos
from crawler.datapoints.path import Path
from crawler.session import Session




class Download(Function):

    def __init__(
            self, 
            path: Path,
            files_and_videos: FilesAndVideos, 
            current_file: Datapoint,
            percentage_downloaded: Datapoint
        ) -> None:
        super().__init__()
        self.path = path
        self.files_and_videos = files_and_videos
        self.current_file = current_file
        self.percentage_downloaded = percentage_downloaded

    def execute(self):
        # shorten tree 

        # preprocess file paths
        self.shorten_long_paths(self.files_and_videos.value)
        # download files
        total_downloads = len(self.files_and_videos.value)
        downloaded = 0
        for item in self.files_and_videos.value:
            self.current_file.submit_value(item.name)
            self.download(item)
            downloaded += 1
            self.percentage_downloaded.submit_value(int(downloaded/total_downloads*100))
        

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

    def download(self, item):
        path = self.get_path(item) 
        if not os.path.isdir(path.parent):
            os.makedirs(path.parent)
        with open(str(path) + '.pdf', 'wb') as file:
            file.write(Session.get_file_content(filter_url(item.url, item.url_format))) 

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