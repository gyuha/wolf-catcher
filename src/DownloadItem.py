import importlib
from PySide6.QtWidgets import QWidget
from src.site.browser.BrowserGet import BrowserGet, GET_STATE, GET_TYPE
from src.site.Site import Site
from ui.Ui_DownloadItem import Ui_DownloadItem
from src.site.SiteBase import SiteBase
from util.Config import Config


class DownloadItem(QWidget):
    def __init__(self, url: str):
        print("📢[DownloadItem.py:10]: ", url)
        super(DownloadItem, self).__init__()

        self.config = Config()
        self.ui = Ui_DownloadItem()
        self.ui.setupUi(self)

        self.url = url
        self.site = self.load_site_class(self.url)
        # print("📢[DownloadItem.py:16]: ", self.site)
        self.browserGet = BrowserGet(self, self.site.browser)

        # 리스트 받기
        self.dowload_capter_list()

    def load_site_class(self, url) -> SiteBase:
        config = self.config.get_site_config(url)

        if config is None:
            raise Exception("Could not find config")

        class_module = getattr(
            importlib.import_module("src.site." + config["class_name"]),
            config["class_name"],
        )

        if class_module is None:
            return None
        module = class_module(config)
        return module

    def dowload_capter_list(self):
        self.browserGet.condition(GET_TYPE.CHAPTER_INFO, self.url)
        self.browserGet.start()
        # print('📢[DownloadItem.py:17]: ', self.url)
        # self.site.get_chapter_info(self.url)
