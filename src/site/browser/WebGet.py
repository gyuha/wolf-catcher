from enum import Enum
from PySide6.QtCore import QObject, QThread, Signal, Slot

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import visibility_of_element_located

from lib.exceptions import GetTimeoutException
from util.Config import Config


class WebGetState(Enum):
    ready = 0
    loading = 1
    done = 2
    error = 3


class WebGetSignal(QObject):
    get_state = Signal()


class WebGet(QThread):
    signal = WebGetSignal()

    def __init__(self, browser):
        self.config = Config()
        self.__browser = browser
        self.__timeout = self.config.setting["timeout"]
        self.state = WebGetState.ready

    @property
    def browser(self):
        return self.__browser

    def run(self):
        if self.state == WebGetState.loading:
            raise Exception("Now loading...")
        self.get()

    def condition(self, url: str, find_by: By = By.XPATH, condition: str = "html"):
        self.__url = url
        self.__find_by = find_by
        self.__condition = condition

    def __get(self):
        self.__browser.get(self.__url)
        wait = WebDriverWait(self.__browser, timeout=self.__timeout)

        try:
            wait.until(
                visibility_of_element_located((self.__find_by, self.__condition))
            )
            self.signals.get_state.emit(WebGetState.done)
        except TimeoutException:
            self.signals.get_state.emit(WebGetState.error)
            raise GetTimeoutException
        finally:
            self.get_state = WebGetState.ready
