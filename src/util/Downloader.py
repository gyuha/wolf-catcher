import os
import re
from urllib import response
import requests
from requests import Response, Session
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from PySide6.QtCore import QObject, Signal
from multiprocessing import cpu_count
import pathlib


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36"
}

class DownloaderSignal(QObject):
    download_state = Signal(int)
    download_error = Signal(str)

class Downloader:
    signals = DownloaderSignal()

    def __init__(self):
        self.files = []
        self.downloading = False
        self.send_count = 0


    def add_files(self, path: str, urls: list, referer):
        self.files = [];
        for url in urls:
            self.files.append([url, path, referer, len(self.files) + 1])
    

    def download_run(self) -> None:
        self.downloading = True
        cpus = cpu_count()
        pool = ThreadPool(cpus - 1)
        self.send_count = 0
        try:
            results = pool.imap_unordered(self.download_images_from_url, self.files)
            for result in results:
                print('url:', result)
        finally:
            pool.close()
            pool.join()
            self.downloading = False
            print('📢[Downloader.py:49]: ', self.downloading)


    def __reqeust_session(self, referer = "") -> Session:
        headers = HEADERS

        if referer:
            headers["Referer"] = referer
        
        requests.urllib3.disable_warnings()
        session = requests.Session()
        session.headers.update(headers)

        return session


    # @retry(exceptions=Exception, tries=5, delay=0)
    def download_images_from_url(self, args: list) -> None:
        url, path, referer, number = args[0], args[1], args[2], args[3]

        session = self.__reqeust_session(referer)

        try:
            response = session.get(url, stream=True, verify=False)

            file_path = os.path.join(path, "%03d" % (number) + ".jpg")
            self.__save_file(file_path, response)

            self.send_count = self.send_count + 1
            self.signals.download_state.emit(self.send_count)
        except Exception as e:
            print("Exception in download_url_to_file(): ", e)
        
        return number
    

    def download_image_from_url(self, url: str, file_path: str, referer: str) -> None:
        session = self.__reqeust_session(referer)

        try:
            response = session.get(url, stream=True, verify=False)
            self.__save_file(file_path, response)
        except Exception as e:
            print("Exception in download_image_from_url(): ", e)


    
    def __save_file(self, file_path: str, response: Response):
        pathlib.Path(os.path.dirname(file_path)).mkdir(parents=True, exist_ok=True)

        try:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=4096):
                    f.write(chunk)
        except Exception as e:
            print("Exception in __save_file(): ", e)
    