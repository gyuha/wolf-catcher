from enum import Enum
import os
import pathlib
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

from util.Downloader import DOWNLOAD_STATE, DOWNLOAD_TYPE, Downloader
from src.util.DatabaseManager import DatabaseManager
from util.message import toast


class DOWNLOAD_ITEM_STATE(Enum):
    READY = 0
    DOING = 1
    DONE = 2
    ERROR = 3


class DownloadItemSignals(QObject):
    remove_item = Signal(str)
    download_state = Signal(str, DOWNLOAD_ITEM_STATE)


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
        self.url = site_config["url"] + site_config["url_format"]["title"]["filter"]
        self.url = self.url.format(self.id)
        self.info = TitleInfo()

        self.__init_text()
        self.__init_downloader()
        self.__init_connect()
        self.state = DOWNLOAD_ITEM_STATE.READY
        self.db = DatabaseManager()
        # self.__init_site()

    def __init_connect(self):
        self.ui.delete_button.clicked.connect(self.__on_click_delete_button)
        self.ui.folder_open_button.clicked.connect(self.__on_click_open_folder)

    def __init_text(self):
        self.ui.title_label.setText("----")
        self.ui.id_label.setText(self.id)
        self.ui.status_label.setText("대기")

    @property
    def key(self):
        return self.name + self.id

    def start(self):
        self.state = DOWNLOAD_ITEM_STATE.DOING
        self.site_loader = SiteLoader(self, self.site_config)
        self.site_loader.signals.on_site_loaded.connect(self.__on_site_loaded)
        self.site_loader.start()
        self.ui.status_label.setText("정보 조회 중")

    def __init_downloader(self):
        self.downloader = Downloader(self, self.site_config["url"])
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
        self.browserGet.id = self.id
        self.browserGet.signals.get_state.connect(self.__on_get_state)
        self.__get_url_title_info()

    def __get_url_title_info(self):
        """
        타이틀 읽기 -> 챕터 목록
        """
        self.browserGet.condition(
            GET_TYPE.TITLE_INFO,
            self.url,
            self.site_config["url_format"]["title"]["visible_condition"]["type"],
            self.site_config["url_format"]["title"]["visible_condition"]["text"],
        )
        self.browserGet.start()
        self.ui.status_label.setText(f"[{self.site.current_chapter+1}/{self.site.total_chapter}] 조회 중")

    def __get_chapter_info(self):
        """
        챕터 내용 읽기 -> 이미지 목록
        """
        subject, url = self.site.get_current_chapter()
        if subject is None:
            self.__set_done()
            return
        self.browserGet.condition(
            GET_TYPE.CHAPTER_INFO,
            url,
            self.site_config["url_format"]["chapter"]["visible_condition"]["type"],
            self.site_config["url_format"]["chapter"]["visible_condition"]["text"],
        )
        self.browserGet.start()

    @Slot(str, GET_TYPE, GET_STATE)
    def __on_get_state(self, id: str, type: GET_TYPE, state: GET_STATE):
        if self.id != id:
            return
        if state == GET_STATE.ERROR:
            notification.notify(
                title="안내",
                message="챕터의 내용을 받지 못 했습니다.",
                app_name="Wolf",
                timeout=3,  # seconds
            )
            self.state = DOWNLOAD_ITEM_STATE.ERROR
            self.signals.download_state.emit(self.key, self.state)
        elif state == GET_STATE.LOADING:
            return
        elif state == GET_STATE.DONE:
            self.__on_get_done(type)

    def __on_get_done(self, type: GET_TYPE):
        if type == GET_TYPE.TITLE_INFO:
            self.site.get_chapter_info_parser(self.browser)
            self.__get_chapter_info()
            # self.ui.progress_bar.setValue(self.site.progress)
            self.__set_status_text()
            return
        elif type == GET_TYPE.CHAPTER_INFO:
            self.site.get_img_list(self.browser)
            self.__download_chapter_images()
            self.__set_status_text()
            pass

    def __set_status_text(self):
        subject = self.site.get_current_chapter()[0]
        current = self.site.current_chapter+1
        if current > self.site.total_chapter:
            current = self.site.total_chapter
        self.ui.status_label.setText(f"[{current}/{self.site.total_chapter}] {subject}")

    def __on_click_delete_button(self):
        if self.state == DOWNLOAD_ITEM_STATE.DOING:
            toast(self, "지울 수 없습니다.")
            return
        self.signals.remove_item.emit(self.key)
    
    def __on_click_open_folder(self):
        path = os.path.realpath(self.site.path)
        if os.path.exists(path):
            os.startfile(path)

    def download_thumbnail(self, url: str, file_path: str):
        if os.path.exists(file_path):
            self.__thumbnail()
            return

        self.downloader.id = self.id
        self.downloader.add_image_files(DOWNLOAD_TYPE.THUMBNAIL, [[url, file_path]])
        self.downloader.start()

    def __download_chapter_images(self):
        self.downloader.id = self.id
        chapter_title, _ = self.site.get_current_chapter()
        chapter_images = self.site.chapter_images

        file_path = os.path.join(
            self.site.path, self.site.strip_title_for_path(chapter_title)
        )
        pathlib.Path(file_path).mkdir(parents=True, exist_ok=True)

        image_list = []
        image_num = 0
        self.title_path = os.path.join(
            self.site.path, self.site.strip_title_for_path(chapter_title)
        )
        for image in chapter_images:
            image_num += 1
            file_path = os.path.join(self.title_path, f"{image_num:03d}.jpg")
            image_list.append([image, file_path])
        self.downloader.set_title_path(self.title_path)
        self.downloader.add_image_files(DOWNLOAD_TYPE.IMAGES, image_list)
        self.downloader.start()

    def update_info(self, info, update = True):
        self.info = info
        try:
            self.ui.title_label.setText(f'{info["title"]}')
            self.ui.tag_label.setText(f'{"/".join(info["tags"])}')
            if update:
                self.db.updated_product(
                    self.id,
                    info["title"],
                    info["author"],
                    "",
                    "/".join(info["tags"])
                )
        except Exception as e:
            print('📢[DownloadItem.py:209]: ', e)
            

    @Slot(str, DOWNLOAD_TYPE, DOWNLOAD_STATE, int, int)
    def __on_download_state(self, id, type, state, count, total):
        """
        다운로드 완료 후 처리
        """
        if str(self.id) != str(id):
            return

        if type == DOWNLOAD_TYPE.THUMBNAIL:
            self.__thumbnail()
            return

        if type == DOWNLOAD_TYPE.IMAGES:
            if state == DOWNLOAD_STATE.COMPRESS:
                self.ui.status_label.setText(f"[{self.site.current_chapter+1}/{self.site.total_chapter}] 압축중")
                return

            self.ui.progress_bar.setValue(int(float(count) / float(total) * 100))

            if state == DOWNLOAD_STATE.DONE:
                self.__on_download_done()
            return

    def __on_download_done(self):
        self.site.set_next_chapter()
        if self.site.progress > 100:
            self.__set_done()
            return
        self.__get_chapter_info()

    def __set_done(self):
        """
        완료 처리
        """
        self.ui.status_label.setText("완료")
        self.ui.progress_bar.setValue(100)

        self.state = DOWNLOAD_ITEM_STATE.DONE
        self.signals.download_state.emit(self.key, self.state)

    def __thumbnail(self):
        if not os.path.exists(self.site.thumbnail_path):
            return
        pixmap = QtGui.QPixmap(self.site.thumbnail_path)
        pixmap = pixmap.scaled(QSize(60, 60))
        self.ui.image_label.setPixmap(pixmap)
