import importlib
import time
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, QThread, Signal, Slot
from src.site.browser.BrowserGet import BrowserGet, GET_STATE, GET_TYPE
from src.site.SiteLoader import SiteLoader
from ui.Ui_DownloadItem import Ui_DownloadItem
from src.site.SiteBase import SiteBase
from util.Config import Config
from plyer import notification


class DownloadItem(QWidget):
    def __init__(self, url: str):
        super(DownloadItem, self).__init__()

        self.config = Config()
        self.ui = Ui_DownloadItem()
        self.ui.setupUi(self)

        self.url = url

        self.__init_site(url)

    def __init_site(self, url):
        config = self.config.get_site_config(url)
        if config == None:
            return
        self.siteLoader = SiteLoader(self, config)
        self.siteLoader.signals.on_site_loaded.connect(self.__on_site_loaded)
        self.siteLoader.is_loading = True
        self.siteLoader.start()

    def __on_site_loaded(self):
        self.site = self.siteLoader.site_class
        self.browser = self.site.browser
        self.browserGet = BrowserGet(self, self.browser)
        self.browserGet.signals.get_state.connect(self.__on_get_state)
        self.__get_url_capter_info()

    def __get_url_capter_info(self):
        self.browserGet.condition(GET_TYPE.CHAPTER_INFO, self.url)
        self.browserGet.start()
        # print('📢[DownloadItem.py:17]: ', self.url)
        # self.site.get_chapter_info(self.url)

    @Slot(GET_TYPE, GET_STATE)
    def __on_get_state(self, type: GET_TYPE, state: GET_STATE):
        print('📢[DownloadItem.py:48]: ', state)
        print('📢[DownloadItem.py:48]: ', type)
        if state != GET_STATE.ERROR:
            notification.notify(
                title="안내",
                message="챕터의 내용을 받지 못 했습니다.",
                app_name="Wolf",
                timeout=3,  # seconds
            )
        elif state != GET_STATE.LOADING:
            return;
        elif state == GET_STATE.DONE:
            pass
