import PySide6.QtCore
import requests

from enum import Enum
from PySide6.QtCore import QObject, QThread, Signal, Slot

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import visibility_of_element_located, presence_of_element_located

from lib.exceptions import GetTimeoutException
from util.Config import Config

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36"
}


class REQUEST_GET_STATE(Enum):
    READY = 0
    LOADING = 1
    DONE = 2
    ERROR = 3


class REQUEST_GET_TYPE(Enum):
    TITLE_INFO = 0
    CHAPTER_INFO = 1

class RequestGetSignal(QObject):
    get_state = Signal(str, REQUEST_GET_TYPE, REQUEST_GET_STATE)

class RequestGet(QThread):
    signals = RequestGetSignal()

    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.__parent = parent
        self.config = Config()
        self.site_config = parent.site_config;
        self.referer = self.site_config["url"]
        self.__timeout = self.config.setting["timeout"]
        self.state = REQUEST_GET_STATE.READY
        self.id = ""
        self.content = ""

    @property
    def browser(self):
        return self.__browser

    def run(self):
        if self.state == REQUEST_GET_STATE.LOADING:
            raise Exception("Now loading...")
        self.__get()
        # self.quit()
    
    def stop(self):
        self.quit()

    def condition(
        self, type: REQUEST_GET_TYPE, url: str, condition: str = "html"
    ):
        self.__get_type = type
        self.__url = url
        self.__condition = condition

    def __get(self):
        self.signals.get_state.emit(self.id, self.__get_type, REQUEST_GET_STATE.LOADING)
        self.get_state = REQUEST_GET_STATE.LOADING

        headers = HEADERS

        if self.referer:
            headers["Referer"] = self.referer

        requests.urllib3.disable_warnings()
        session = requests.Session()
        session.headers.update(headers)

        try:
            response = session.get(self.__url, verify=False, timeout=(3, 10))

            if response.status_code > 200:
                raise Exception("Response error : {}" % (response.status_code))
            
            self.content = response.content
            self.signals.get_state.emit(self.id, self.__get_type, REQUEST_GET_STATE.DONE)
        except Exception as e:
            self.signals.get_state.emit(self.id, self.__get_type, REQUEST_GET_STATE.ERROR)
            raise Exception("Exception in download_url_to_file(): ", e)
        