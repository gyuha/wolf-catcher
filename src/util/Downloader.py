from enum import Enum
import os
import shutil
import threading
import time
import zipfile
import requests
from PySide6.QtCore import QObject, QThread, Signal, Slot
from requests import Response
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from PySide6.QtCore import QObject, Signal
from multiprocessing import cpu_count


class DOWNLOAD_TYPE(Enum):
    THUMBNAIL = 1
    IMAGES = 2


class DOWNLOAD_STATE(Enum):
    READY = 0
    DOING = 1
    COMPRESS = 2
    DONE = 3


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36"
}


class DownloaderSignal(QObject):
    download_state = Signal(
        str, DOWNLOAD_TYPE, DOWNLOAD_STATE, int, int
    )  # id, type, current, total
    download_error = Signal(str)


class Downloader(QThread):
    signals = DownloaderSignal()

    def __init__(self, parent, referer: str = ""):
        QThread.__init__(self, parent)
        self._parent = parent
        self.files = []
        self.downloading = False
        self.send_count = 0
        self.total_count = 0
        self.current_index = 0
        self.pool_count = 0
        self.referer = referer
        self.id = None
        self.title_path = None

    def set_title_path(self, title_path):
        self.title_path = title_path

    def run(self):
        cpus = cpu_count()
        self.current_index = 0
        self.send_count = 0
        while self.send_count < self.total_count:
            if self.current_index < self.total_count and self.pool_count < cpus:
                self.create_download_thread(self.files[self.current_index])
                self.current_index += 1
            time.sleep(0.01)

        if self.type == DOWNLOAD_TYPE.THUMBNAIL:
            self.signals.download_state.emit(
                self.id,
                self.type,
                DOWNLOAD_STATE.COMPRESS,
                self.send_count,
                self.total_count,
            )
            return

        # 이미지이면 폴더 압축하기
        self.signals.download_state.emit(
            self.id,
            self.type,
            DOWNLOAD_STATE.COMPRESS,
            self.send_count,
            self.total_count,
        )
        self.create_compress_thread()

    def create_compress_thread(self):
        compress_thread = threading.Thread(
            target=self.__zip_folder, args=(self.title_path, self.title_path + ".cbz")
        )
        compress_thread.start()

    def create_download_thread(self, data):
        self.pool_count += 1
        download_thread = threading.Thread(
            target=self.__download_url_to_file, args=(data[0], data[1])
        )
        download_thread.start()

    def add_image_files(self, type: DOWNLOAD_TYPE, image_list: list) -> None:
        self.type = type
        self.files = image_list
        self.total_count = len(self.files)

    # @retry(exceptions=Exception, tries=5, delay=0)
    def __download_url_to_file(self, url, path) -> None:
        # print('📢[Downloader.py:97]: ', args)
        # url, path = args[0], args[1]

        headers = HEADERS

        if self.referer:
            headers["Referer"] = self.referer

        requests.urllib3.disable_warnings()
        session = requests.Session()
        session.headers.update(headers)

        try:
            response = session.get(url, stream=True, verify=False)

            if response.status_code > 200:
                raise Exception("Response error : {}" % (response.code))

            self.__save_file(path, response)
        except Exception as e:
            print("Exception in download_url_to_file(): ", e)
        finally:
            self.__download_state_emit()
            self.pool_count -= 1

    def __download_state_emit(self):
        self.send_count = self.send_count + 1
        self.signals.download_state.emit(
            self.id, self.type, DOWNLOAD_STATE.DOING, self.send_count, self.total_count
        )

    def __save_file(self, path: str, response: Response):
        # pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        try:
            with open(path, "wb") as f:
                for chunk in response.iter_content(chunk_size=4096):
                    f.write(chunk)
        except Exception as e:
            print("Exception in __save_file(): ", e)

    def __zip_folder(self, path: str, filename: str, remove_origin=True):
        """
        폴더 압축하기
        """
        if os.path.exists(filename):
            self.signals.download_state.emit(
                self.id,
                self.type,
                DOWNLOAD_STATE.DONE,
                self.send_count,
                self.total_count,
            )

        zipf = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
        for f in os.listdir(path):
            zipf.write(os.path.join(path, f), os.path.basename(f))
        zipf.close()

        if remove_origin:
            shutil.rmtree(path, ignore_errors=True)

        self.signals.download_state.emit(
            self.id,
            self.type,
            DOWNLOAD_STATE.DONE,
            self.send_count,
            self.total_count,
        )
