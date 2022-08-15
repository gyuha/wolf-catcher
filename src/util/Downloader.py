import requests
import time
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from PySide6.QtCore import QObject, Signal, QThread

class DownloaderSignal(QObject):
    download_state = Signal(int)
    download_error = Signal(str)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36"
}

class Downloader(QThread):
    signals = DownloaderSignal()

    def __init__(self):
        super()
        files = []


    def run(self):
        if len(self.files):
            self.signals.download_error.emit("empty list")
            return
        self.download_run()
        

    def add_files(self, path, urls):
        pass        

    
    def download_run(self, args):
        cpus = cpu_count()
        results = ThreadPool(cpus - 1).imap_unordered(self.download_url_to_file, args)
        for result in results:
            print('url:', result[0], 'time (s):', result[1])


    def download_url_to_file(self, args):
        url, path, referer = args[0], args[1], args[2]

        headers = HEADERS

        if referer:
            headers["Referer"] = referer
        
        try:
            requests.urllib3.disable_warnings()
            response = requests.get(url, headers=headers)
            self.__save_file(path, response)
        except Exception as e:
            print("Exception in download_url_to_file(): ", e)

    
    def __save_file(self, path, response):
        try:
            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=4096):
                    f.write(chunk)
        except Exception as e:
            print("Exception in __save_file(): ", e)
    
