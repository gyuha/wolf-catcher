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
    def __init__(self, id: str, site_config):
        super(DownloadItem, self).__init__()

        self.ui = Ui_DownloadItem()
        self.ui.setupUi(self)

        self.id = id

        self.site_config = site_config
        if site_config == None:
            return

        self.name = site_config["name"]
        self.url = site_config["url"] + site_config["url_format"]["list"]["filter"]
        self.url = self.url.format(self.id)

        self.__init_site()

    @property
    def key(self):
        return self.name + self.id

    def __init_site(self):
        self.siteLoader = SiteLoader(self, self.site_config)
        self.siteLoader.signals.on_site_loaded.connect(self.__on_site_loaded)
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

    @Slot(GET_TYPE, GET_STATE)
    def __on_get_state(self, type: GET_TYPE, state: GET_STATE):
        if state == GET_STATE.ERROR:
            notification.notify(
                title="안내",
                message="챕터의 내용을 받지 못 했습니다.",
                app_name="Wolf",
                timeout=3,  # seconds
            )
        elif state != GET_STATE.LOADING:
            return
        elif state == GET_STATE.DONE:
            pass
