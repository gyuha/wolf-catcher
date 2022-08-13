from abc import ABC, abstractmethod


class SiteBase(ABC): 
    def __init__(self, config):
        self.name = config["name"]
        self.file_extensions = config["file_extensions"]
        self.download_path = config["download_path"]

    @abstractmethod
    def get_chapter_info(self, url):
        pass
    
    @abstractmethod
    def get_img_list(self, url):
        pass
