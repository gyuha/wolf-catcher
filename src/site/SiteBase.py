from abc import ABC, abstractmethod
import os
import pathlib
import re
from src.util.file_name import strip_file_path
from util.Config import Config
from util.SeleniumWorker import SeleniumWorker
from selenium.webdriver.common.by import By
from src.site.browser.BrowserDriver import BrowserDriver


class SiteBase(ABC):
    def __init__(self, config: Config):
        self.browerDriver = BrowserDriver()

        self.name = config["name"]
        self.url = config["url"]
        self.file_extensions = config["file_extensions"]
        self.download_path = config["download_path"]
        self.url_format = config["url_format"]

    @property
    def site_name(self):
        return self.name

    @abstractmethod
    async def get_chapter_info(self, url):
        pass

    @abstractmethod
    def get_img_list(self, url):
        pass

    def strip_title_for_path(self, title: str) -> str:
        """
        윈도우에서 사용이 가능한 파일 명으로 변경
        """
        path = re.sub(r"NEW\t+", "", path)

        path = path.replace("\n", "")
        path = re.sub(r"\t.*$", "", path)
        path = (
            path.replace(":", "")
            .replace("?", "")
            .replace("/", "")
            .replace("!", "")
            .replace("\\", "")
        )
        path = path.replace("「", " ").replace("」", "").replace(".", "")
        path = path.replace("<", "").replace(">", "")

        path = path.strip()
        return path

    def dowload_path(self, base_path: str, title: str) -> str:
        path = os.path.join(base_path, self.strip_file_path(title))
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        return path

    def __find_type(self, type: str) -> By:
        if type == "xpath":
            return By.XPATH

        return By
