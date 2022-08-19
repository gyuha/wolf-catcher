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

class DownloadItemSignals(QObject):
    remove_item = Signal(str)

class DownloadItem(QWidget):
    signals = DownloadItemSignals()

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

        self.__init_connect()
        self.__init_site()
    
    def __init_connect(self):
        self.ui.delete_button.setEnabled(False)
        self.ui.delete_button.clicked.connect(self.__on_click_delete_button)

    @property
    def key(self):
        return self.name + self.id

    def __init_site(self):
        self.site_loader = SiteLoader(self, self.site_config)
        self.site_loader.signals.on_site_loaded.connect(self.__on_site_loaded)
        self.site_loader.start()

    def __on_site_loaded(self):
        self.site = self.site_loader.site_class
        self.browser = self.site.browser
        self.browserGet = BrowserGet(self, self.browser)
        self.browserGet.signals.get_state.connect(self.__on_get_state)
        self.__get_url_capter_info()

    def __get_url_capter_info(self):
        self.browserGet.condition(
            GET_TYPE.CHAPTER_INFO, 
            self.url,
            self.site_config["url_format"]["list"]["visible_condition"]["type"],
            self.site_config["url_format"]["list"]["visible_condition"]["text"],
            )
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
            print('📢[DownloadItem.py:73]: ', GET_STATE.DONE)
        elif state == GET_STATE.LOADING:
            return
        elif state == GET_STATE.DONE:
            print('📢[DownloadItem.py:73]: ', GET_STATE.DONE)
            self.ui.delete_button.setEnabled(True)
    
    def __on_click_delete_button(self):
        self.signals.remove_item.emit(self.key)
