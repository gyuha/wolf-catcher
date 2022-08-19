from signal import Signals
import urllib
import asyncio

from selenium import webdriver

from PySide6.QtCore import QObject, QThread, Signal

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import visibility_of_element_located

from lib.exceptions import GetTimeoutException
from util.Config import Config

import urllib


class SeleniumWorkerSignals(QObject):
    url_get_state = Signal(int)


class SeleniumWorker(QThread):
    signals = SeleniumWorkerSignals()

    def __init__(self, parent):
        super().__init__(parent)
        self.config = Config()
        self.__is_getting = False
        self.__timeout = 5
        self.__browser_type = self.config.setting["browser"]
        self.__init_driver()

    def __init_driver(self):
        print("[{}] Web Driver loading...".format(self.__browser_type), end="\r")

        if self.__browser_type == "chrome":
            """
            Chrome
            """
            driver_file = "./driver/chromedriver.exe"
            options = ChromeOptions()
            options.headless = self.config.setting["headless"]
            self.__browser = webdriver.Chrome(
                executable_path=driver_file, options=options
            )

        elif self.__browser_type == "firefox":
            """
            Firefox
            """
            driver_file = "./driver/geckodriver.exe"
            options = FirefoxOptions()
            options.headless = self.config.setting["headless"]
            self.__browser = webdriver.Firefox(
                executable_path=driver_file, options=options
            )

        if self.__browser:
            self.__browser.implicitly_wait(5)

    def set_url_info(self, url: str, find_by: str = "xpath", condition: str = "html"):
        self.__url = url
        self.__find_by = find_by
        self.__condition = condition

    def run(self):
        self.get_with_retry()

    @property
    def browser(self):
        return self.__browser

    @property
    def is_getting(self):
        return self.__is_getting

    @property
    def is_complete(self):
        return self.__is_complete

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        self.__url = value

    def driver_close(self):
        if self.__browser:
            self.__browser.close()

    def reconnect(self):
        if self.__browser:
            self.__browser.close()
            self.__browser = self.driver_init()

    @property
    def page_source(self):
        return self.browser.page_source
