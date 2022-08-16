import os
import re
import requests
from requests import Response
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
            results = pool.imap_unordered(self.__download_url_to_file, self.files)
            for result in results:
                print('url:', result)
        finally:
            pool.close()
            pool.join()
            self.downloading = False
            print('📢[Downloader.py:49]: ', self.downloading)


    # @retry(exceptions=Exception, tries=5, delay=0)
    def __download_url_to_file(self, args: list) -> None:
        url, path, referer, number = args[0], args[1], args[2], args[3]

        headers = HEADERS

        if referer:
            headers["Referer"] = referer
        
        requests.urllib3.disable_warnings()
        session = requests.Session()
        session.headers.update(headers)

        try:
            response = session.get(url, stream=True, verify=False)

            if response.status_code > 200:
                raise Exception("Response error : {}"%(response.code))

            self.__save_file(path, number, response)
            self.__download_state_emit()
        except Exception as e:
            print("Exception in download_url_to_file(): ", e)
        
        return number
    
    def __download_state_emit(self):
        self.send_count = self.send_count + 1
        self.signals.download_state.emit(self.send_count)


    
    def __save_file(self, path: str, number: int, response: Response):
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

        file_path = os.path.join(path, "%03d" % (number) + ".jpg")

        try:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=4096):
                    f.write(chunk)
        except Exception as e:
            print("Exception in __save_file(): ", e)
    
