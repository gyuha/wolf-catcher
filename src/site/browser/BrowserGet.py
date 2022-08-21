from enum import Enum
from PySide6.QtCore import QObject, QThread, Signal, Slot

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import visibility_of_element_located

from lib.exceptions import GetTimeoutException
from util.Config import Config


class GET_STATE(Enum):
    READY = 0
    LOADING = 1
    DONE = 2
    ERROR = 3


class GET_TYPE(Enum):
    TITLE_INFO = 0
    CHAPTER_INFO = 1


class BrowserGetSignals(QObject):
    get_state = Signal(str, GET_TYPE, GET_STATE)


class BrowserGet(QThread):
    signals = BrowserGetSignals()

    def __init__(self, parent, browser: webdriver):
        QThread.__init__(self, parent)
        self.__parent = parent
        self.config = Config()
        self.__browser = browser
        self.__timeout = self.config.setting["timeout"]
        self.state = GET_STATE.READY
        self.id = ""

    @property
    def browser(self):
        return self.__browser

    def run(self):
        if self.state == GET_STATE.LOADING:
            raise Exception("Now loading...")
        self.__get()
        # self.quit()

    def condition(
        self, type: GET_TYPE, url: str, find_by: By = By.XPATH, condition: str = "html"
    ):
        self.__get_type = type
        self.__url = url
        self.__find_by = find_by
        self.__condition = condition

    def __get(self):
        self.signals.get_state.emit(self.id, self.__get_type, GET_STATE.LOADING)
        self.get_state = GET_STATE.LOADING

        self.__browser.get(self.__url)
        wait = WebDriverWait(self.__browser, timeout=self.__timeout)

        try:
            wait.until(
                visibility_of_element_located((self.__find_by, self.__condition))
            )
            self.signals.get_state.emit(self.id, self.__get_type, GET_STATE.DONE)
        except TimeoutException:
            self.signals.get_state.emit(self.id, self.__get_type, GET_STATE.ERROR)
            raise GetTimeoutException
        finally:
            self.get_state = GET_STATE.READY
