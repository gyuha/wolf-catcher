from enum import Enum
import os
import pathlib
import re
from PySide6.QtWidgets import QWidget
from PySide6 import QtGui, QtCore
from PySide6.QtCore import QObject, QThread, Signal, Slot, QSize, Qt
from src.site.Wfwf import Wfwf
from src.site.TitleInfo import TitleInfo
from src.site.SiteLoader import SiteLoader
from ui.Ui_DownloadItem import Ui_DownloadItem
from src.site.SiteBase import SiteBase
from util.Compressor import COMPRESS_STATE, Compressor
from util.Config import Config
from src.site.browser.RequestGet import RequestGet, REQUEST_GET_STATE, REQUEST_GET_TYPE

from util.Downloader import DOWNLOAD_STATE, DOWNLOAD_TYPE, Downloader
from src.util.DatabaseManager import DatabaseManager
from util.ImageCompress import ImageCompress
from util.Upscaler import Upscaler
from util.message import toast


class DOWNLOAD_ITEM_STATE(Enum):
    READY = 1
    DOING = 2
    DONE = 3
    ERROR = 4


class DownloadItemSignals(QObject):
    remove_item = Signal(str)
    download_state = Signal(str, DOWNLOAD_ITEM_STATE)


class DownloadItem(QWidget):
    signals = DownloadItemSignals()

    def __init__(self, id: str, site_config):
        super(DownloadItem, self).__init__()

        self.ui = Ui_DownloadItem()
        self.ui.setupUi(self)
        # self.browserDriver = browserDriver

        self.id = id

        self.site_config = site_config
        self.config = Config()
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
        self.ui.state_label.setText("READY")

        self.compressor = Compressor(self)
        self.compressor.signals.compress_state.connect(self.__on_compress_state)

        self.upscaler = Upscaler()
        self.upscaler.signals.upscale_state.connect(self.__on_upscale_state)

        self.image_compress = ImageCompress(self)
        self.image_compress.signals.image_compress_state.connect(self.__on_image_compress_state)

        self.db = DatabaseManager()
        self.title_path = ""
        # self.__init_site()

        self.retry_count = 0

    def __init_connect(self):
        self.ui.delete_button.clicked.connect(self.__on_click_delete_button)
        self.ui.folder_open_button.clicked.connect(self.__on_click_open_folder)
        self.ui.open_link_button.clicked.connect(self.__on_click_open_link)

    def __init_text(self):
        self.ui.title_label.setWordWrap(True)
        self.ui.title_label.setText("----")
        self.ui.id_label.setText(self.id)
        self.ui.status_label.setText("대기")

    @property
    def key(self):
        return self.name + self.id

    def start(self):
        self.state = DOWNLOAD_ITEM_STATE.DOING
        self.ui.state_label.setText("DOING")
        self.site_loader = SiteLoader(self)
        self.site_loader.signals.on_site_loaded.connect(self.__on_site_loaded)
        self.site_loader.start()
        self.ui.status_label.setText("웹 초기화 중")

    def __init_downloader(self):
        self.downloader = Downloader(self, self.site_config["url"])
        self.downloader.id = self.id
        self.downloader.signals.download_state.connect(self.__on_download_state)

    @Slot(str)
    def __on_site_loaded(self, key):
        """
        사이트의 내용이 완료
        """
        if key != self.key:
            return
        self.site = self.site_loader.site_class
        self.site.id = self.id
        self.site.parent = self

        self.requestGet = RequestGet(self)
        self.requestGet.id = self.id
        self.requestGet.signals.get_state.connect(self.__on_get_state)
        self.__get_url_title_info()

    def __get_url_title_info(self):
        """
        타이틀 읽기 -> 챕터 목록
        """
        self.requestGet.condition(
            REQUEST_GET_TYPE.TITLE_INFO,
            self.url,
            self.site_config["url_format"]["title"]["condition"],
        )
        self.requestGet.start()
        self.__set_current_state_label("조회 중")
    

    def __set_current_state_label(self, msg: str):
        """
        상태 라벨 출력하기
        """
        current = self.site.current_chapter + 1
        if current > self.site.total_chapter:
            current = self.site.total_chapter
        self.ui.status_label.setText(f"[{current}/{self.site.total_chapter}] {msg}")


    def __get_chapter_info(self):
        """
        챕터 내용 읽기 -> 이미지 목록
        """
        subject, url = self.site.get_current_chapter()
        if subject is None:
            self.__set_done()
            return
        self.requestGet.condition(
            REQUEST_GET_TYPE.CHAPTER_INFO,
            self.site_config["url"] + url,
            self.site_config["url_format"]["chapter"]["condition"],
        )
        self.requestGet.start()

    @Slot(str, REQUEST_GET_TYPE, REQUEST_GET_STATE)
    def __on_get_state(self, id: str, type: REQUEST_GET_TYPE, state: REQUEST_GET_STATE):
        if self.id != id:
            return
        if state == REQUEST_GET_STATE.ERROR:
            if type == REQUEST_GET_TYPE.CHAPTER_INFO:
                self.ui.status_label.setText("챕터의 내용을 받지 못 했습니다.")
                self.state = DOWNLOAD_ITEM_STATE.ERROR
                self.signals.download_state.emit(self.key, self.state)

                # 다음 챕터
                self.__on_get_done(type)
            else:
                self.__set_current_state_label("이미지 목록을 읽기 실패")

                self.__on_download_done()
        elif state == REQUEST_GET_STATE.LOADING:
            self.__set_current_state_label("조회중")
            return
        elif state == REQUEST_GET_STATE.DONE:
            self.__on_get_done(type)

    def __on_get_done(self, type: REQUEST_GET_TYPE):
        if type == REQUEST_GET_TYPE.TITLE_INFO:
            self.site.get_chapter_info_parser(self.requestGet.content)
            self.__get_chapter_info()
            # self.ui.progress_bar.setValue(self.site.progress)
            self.__set_status_text()
        elif type == REQUEST_GET_TYPE.CHAPTER_INFO:
            self.site.get_img_list(self.requestGet.content)
            self.__download_chapter_images()
            self.__set_status_text()

    def __set_status_text(self):
        subject = self.site.get_current_chapter()[0]
        current = self.site.current_chapter + 1
        if current > self.site.total_chapter:
            current = self.site.total_chapter
        if subject == None:
            subject = "완료"
        self.ui.status_label.setText(f"[{current}/{self.site.total_chapter}] {subject}")

    def __on_click_delete_button(self):
        if self.state == DOWNLOAD_ITEM_STATE.DOING:
            toast(self, "다운로드 중에는 지울 수 없습니다.")
            return
        self.signals.remove_item.emit(self.key)

    def __on_click_open_folder(self):
        path = os.path.realpath(self.title_path)
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
        chapter_path = os.path.join(
            self.site.path, self.site.strip_title_for_path(chapter_title)
        )
        for image in chapter_images:
            image_num += 1
            file_path = os.path.join(chapter_path, f"{image_num:03d}.jpg")
            image_list.append([image, file_path])
        self.chapter_path = chapter_path
        self.downloader.set_chapter_path(chapter_path)
        self.downloader.add_image_files(DOWNLOAD_TYPE.IMAGES, image_list)
        self.downloader.start()

    def update_info(self, info, update=True):
        self.info = info
        try:
            self.ui.title_label.setText(f'{info["title"]}')
            self.ui.tag_label.setText(f'{"/".join(info["tags"])}')
            if update:
                self.db.updated_product(
                    self.id, info["title"], info["author"], "", "/".join(info["tags"])
                )
            self.__thumbnail()
        except Exception as e:
            print("📢[DownloadItem.py:240]: ", e)

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

        if int(count) == 0 or int(total) == 0:
            self.ui.progress_bar.setValue(0)
        else:
            self.ui.progress_bar.setValue(int(float(count) / float(total) * 100))

        if state == DOWNLOAD_STATE.DONE:
            self.__on_download_done()
        return

    def __on_download_done(self):
        # 파일 다운로드 완료
        if self.config.setting["use_upscale"] == False:
            self.compressor.set_chapter_path(self.id, self.chapter_path)
            self.compressor.start()
            return
        # 업스케일링 경우
        self.upscaler.start(self.id, self.chapter_path)

    @Slot(str, bool, int, int)
    def __on_upscale_state(self, id: str, complete: bool, current: int, total: int):
        if str(self.id) != id:
            return
        if complete == False:
            self.ui.status_label.setText(f"[{self.site.current_chapter + 1}/{self.site.total_chapter}] 업스케일링중 ({current}/{total})")
        else:
            self.image_compress.set_chapter_path(self.id, self.chapter_path)
            self.image_compress.start()

    @Slot(str, COMPRESS_STATE)
    def __on_compress_state(self, id: str, state: COMPRESS_STATE):
        if str(self.id) != str(id):
            return
        # 압축 상태
        if state == COMPRESS_STATE.DONE or state == COMPRESS_STATE.ERROR:
            self.__set_next()
    

    @Slot(str, bool, int, int)
    def __on_image_compress_state(self, id: str, complete: bool, current: int, total: int):
        if self.id != id:
            return
        if complete == False:
            self.ui.status_label.setText(f"[{self.site.current_chapter + 1}/{self.site.total_chapter}] 이미지 최적화 중 ({current}/{total})")
        else:
            self.compressor.set_chapter_path(self.id, self.chapter_path)
            self.compressor.start()


    def __set_next(self):
        # 다음 챕터 처리
        self.site.set_next_chapter()
        if self.site.progress > 100:
            self.__set_done()
            return
        self.__get_chapter_info()

    def __set_done(self):
        """
        완료 처리
        """
        # self.ui.status_label.setText("완료")
        self.__set_status_text()
        self.ui.progress_bar.setValue(100)
        # self.site.browserDriver.driver_close()
        self.state = DOWNLOAD_ITEM_STATE.DONE
        self.ui.state_label.setText("DONE")
        self.signals.download_state.emit(self.key, self.state)

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

    def __thumbnail(self):
        self.title_path = os.path.join(
            self.site_config["download_path"],
            self.strip_title_for_path(self.info["title"]),
        )
        thumbnail_path = os.path.join(
            self.title_path,
            "thumbnail.jpg",
        )
        if not os.path.exists(thumbnail_path):
            return
        pixmap = QtGui.QPixmap(thumbnail_path)
        pixmap = pixmap.scaled(QSize(80, 80))
        self.ui.image_label.setPixmap(pixmap)

    def __on_click_open_link(self):
        link_url = self.site_config["url"]
        link_url += self.site_config["url_format"]["title"]["filter"].format(self.id)
        url = QtCore.QUrl(link_url)
        QtGui.QDesktopServices.openUrl(url)
