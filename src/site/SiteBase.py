from abc import abstractmethod


class SiteBase: 
    def __init__(self, config):
        self.name = config["name"]
        self.file_extensions = config["file_extensions"]
        self.download_path = config["download_path"]
    
    @abstractmethod
    def chapter_list(self, url):
        pass