import os
import re
import zipfile
import requests
from requests import Response
import time
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from PySide6.QtCore import QObject, Signal, QThread
from multiprocessing import Pool, cpu_count
import pathlib

from .file_name import strip_file_path

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


    def add_files(self, path: str, urls: list, referer):
        for url in urls:
            self.files.append([url, path, referer, len(self.files) + 1])
        print('📢[Downloader.py:46]: ', self.files)

    
    def download_run(self) -> None:
        self.downloading = True
        cpus = cpu_count()
        pool = ThreadPool(cpus - 1)
        try:
            results = pool.imap_unordered(self.download_url_to_file, self.files)
            # for result in results:
            #     print('url:', result[0], 'time (s):', result[1])
        finally:
            pool.close()
            pool.join()
            self.downloading = False
            self.signals.download_state.emit(len(self.files))
            self.files.clear()



    def download_url_to_file(self, args: list) -> None:
        url, path, referer, number = args[0], args[1], args[2], args[3]

        headers = HEADERS

        if referer:
            headers["Referer"] = referer
        
        requests.urllib3.disable_warnings()
        session = requests.Session()
        session.headers.update(headers)

        try:
            response = session.get(url, stream=True, verify=False)
            # response = session.get(url, headers=headers)
            self.__save_file(path, number, response)
        except Exception as e:
            print("Exception in download_url_to_file(): ", e)

    
    def __save_file(self, path: str, number: int, response: Response):
        path = self.strip_file_path(path)
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

        file_path = os.path.join(path, "%03d" % (number) + ".jpg")

        try:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=4096):
                    f.write(chunk)
        except Exception as e:
            print("Exception in __save_file(): ", e)
    

    def strip_file_path(self, path):
        """
        윈도우에서 사용이 가능한 파일 명으로 변경
        """
        path = re.sub(r"NEW\t+", "", path)

        path = path.replace('\n', '')
        path = re.sub(r"\t.*$", "", path)
        path = path.replace(':', '').replace('?', '').replace(
            '/', '').replace('!', '').replace('\\', '')
        path = path.replace("「", " ").replace("」", '').replace(".", "")
        path = path.replace("<", "").replace(">", "")

        path = path.strip()
        return path


    def zip_folder(self, filename, path):
        """
        폴더 압축하기
        """
        zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
        for f in os.listdir(path):
            zipf.write(os.path.join(path, f), os.path.basename(f))
        zipf.close()