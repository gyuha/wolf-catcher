from abc import ABC, abstractmethod
import os
import pathlib
import re
from src.site.TitleInfo import TitleInfo
from util.Config import Config
from selenium import webdriver
from selenium.webdriver.common.by import By


class SiteBase(ABC):
    def __init__(self, config: Config):

        self.config = config
        self.id = ""
        self.name = config["name"]
        self.url = config["url"]
        self.file_extensions = config["file_extensions"]
        self.download_path = config["download_path"]
        self.url_format = config["url_format"]

        self.title_info = TitleInfo()

        self.path = "" # 다운로드 경로
        self.parent = None

    @property
    def site_name(self):
        return self.name
    
    @property
    def thumbnail_path(self):
        return os.path.join(self.path, "thumbnail.jpg")

    @abstractmethod
    async def get_chapter_info_parser(self, driver: webdriver):
        pass

    @abstractmethod
    def get_img_list(self, url):
        pass

    def strip_title_for_path(self, title: str) -> str:
        """
        윈도우에서 사용이 가능한 파일 명으로 변경
        """
        title = re.sub(r"NEW\t+", "", title)

        title = title.replace("\n", "")
        title = re.sub(r"\t.*$", "", title)
        title = (
            title.replace(":", "")
            .replace("?", "")
            .replace("/", "")
            .replace("!", "")
            .replace("\\", "")
        )
        title = title.replace("「", " ").replace("」", "").replace(".", "")
        title = title.replace("<", "").replace(">", "")

        title = title.strip()
        return title

    def download_path_init(self, base_path: str, title: str) -> str:
        path = os.path.join(base_path, self.strip_title_for_path(title))
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        self.path = path
        return path

    def download_thumbnail(self, url, file_path):
        self.parent.download_thumbnail(url, file_path)
