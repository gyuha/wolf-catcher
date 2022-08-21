import os
import PySide6
import importlib
import time
from PySide6.QtWidgets import QWidget
from PySide6 import QtGui
from PySide6.QtCore import QObject, QThread, Signal, Slot, QSize, Qt
from src.site.TitleInfo import TitleInfo
from src.site.browser.BrowserGet import BrowserGet, GET_STATE, GET_TYPE
from src.site.SiteLoader import SiteLoader
from ui.Ui_DownloadItem import Ui_DownloadItem
from src.site.SiteBase import SiteBase
from util.Config import Config
from plyer import notification

from util.Downloader import DOWNLOAD_TYPE, Downloader


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
        self.info = TitleInfo()

        self.__init_text()
        self.__init_downloader()
        self.__init_connect()
        self.__init_site()

    def __init_connect(self):
        self.ui.delete_button.setEnabled(False)
        self.ui.delete_button.clicked.connect(self.__on_click_delete_button)
    
    def __init_text(self):
        self.ui.title_label.setText(self.id)

    @property
    def key(self):
        return self.name + self.id

    def __init_site(self):
        self.site_loader = SiteLoader(self, self.site_config)
        self.site_loader.signals.on_site_loaded.connect(self.__on_site_loaded)
        self.site_loader.start()
    
    def __init_downloader(self):
        self.downloader = Downloader(self.site_config["url"])
        self.downloader.id = self.id
        self.downloader.signals.download_state.connect(self.__on_download_state)

    def __on_site_loaded(self):
        """
        사이트의 내용이 완료
        """
        self.site = self.site_loader.site_class
        self.site.id = self.id
        self.site.parent = self

        self.browser = self.site.browser
        self.browserGet = BrowserGet(self, self.browser)
        self.browserGet.signals.get_state.connect(self.__on_get_state)
        self.__get_url_capter_info()

    def __get_url_capter_info(self):
        """
        챕터 내용 읽기
        """
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
            print("📢[DownloadItem.py:73]: ", GET_STATE.DONE)
        elif state == GET_STATE.LOADING:
            return
        elif state == GET_STATE.DONE:
            self.__on_get_done(type)
            # print('📢[DownloadItem.py:73]: ', GET_STATE.DONE)
            # self.ui.delete_button.setEnabled(True)

    def __on_get_done(self, type: GET_TYPE):
        if type == GET_TYPE.CHAPTER_INFO:
            self.site.get_chapter_info_parser(self.browser)
            pass
        elif type == GET_TYPE.IMAGE_LIST:
            pass

    def __on_click_delete_button(self):
        self.signals.remove_item.emit(self.key)

    def download_thumbnail(self, url: str, file_path: str):
        if os.path.exists(file_path):
            self.__thumbnail()
            return

        self.downloader.id = self.id
        self.downloader.add_image_files(DOWNLOAD_TYPE.THUMBNAIL, [[url, file_path]])
        self.downloader.download_run()
        # downloader.add_files(DOWNLOAD_TYPE.THUMBNAIL)
        # print('📢[DownloadItem.py:99]: ', file_path)
        # print('📢[DownloadItem.py:99]: ', url)
    
    def update_info(self, info: TitleInfo):
        self.info = info
        self.ui.title_label.setText(f'{self.id} : {info["title"]}')
    
    @Slot(str, DOWNLOAD_TYPE, int, int)
    def __on_download_state(self, id, type, count, total):
        """
        다운로드 완료 후 처리
        """
        print('📢[DownloadItem.py:137]: ', self.id)
        print('📢[DownloadItem.py:138]: ', id)
        if str(self.id) != str(id):
            return;
        
        if type == DOWNLOAD_TYPE.THUMBNAIL:
            self.__thumbnail()
            return

    def __thumbnail(self):
        print('📢[DownloadItem.py:145]: ', self.site.thumbnail_path)
        pixmap  = QtGui.QPixmap(self.site.thumbnail_path)
        pixmap = pixmap.scaled(QSize(60, 60))
        self.ui.image_label.setPixmap(pixmap)