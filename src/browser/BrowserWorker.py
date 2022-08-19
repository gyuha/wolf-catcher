from enum import Enum
from src.site.SiteBase import SiteBase
from util.Config import Config

from PySide6.QtCore import QObject, QThread, Signal

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import visibility_of_element_located

from lib.exceptions import GetTimeoutException
from src.browser.BrowserWorker import WorkerState


class WorkerState(Enum):
    none = 1
    loading = 2
    done = 3
    error = 4


class BrowserWorkerSignal(QObject):
    url_get_state = Signal(WorkerState)


class BrowserWorker():

    def __init__(self, parent: SiteBase):
        self.config = Config()
        self.state = WorkerState.none
        self.__timeout = self.config.setting["browser"]["timeout"]
        self.__browser_type = self.config.setting["browser"]
        self.__init_driver()

    def __init_driver(self):
        print("[{}] Web Driver loading...".format(
            self.__browser_type), end="\r")

        if self.__browser_type == 'chrome':
            """ 
            Chrome
            """
            driver_file = './driver/chromedriver.exe'
            options = ChromeOptions()
            options.headless = self.config.setting["headless"]
            self.__browser = webdriver.Chrome(
                executable_path=driver_file,
                options=options)

        elif self.__browser_type == 'firefox':
            """
            Firefox
            """
            driver_file = './driver/geckodriver.exe'
            options = FirefoxOptions()
            options.headless = self.config.setting["headless"]
            self.__browser = webdriver.Firefox(
                executable_path=driver_file,
                options=options)

        if self.__browser:
            self.__browser.implicitly_wait(5)


    @property
    def browser(self):
        return self.__browser


    def driver_close(self):
        if self.__browser:
            self.__browser.close()


    def reconnect(self):
        if self.__browser:
            self.__browser.close()
            self.__browser = self.driver_init()


    def get(self):
        if self.state == WorkerState.loading:
            raise Exception('now loading')
        
        self.browser.get(self.__url)
