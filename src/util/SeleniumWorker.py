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


    def set_url_info(self, url: str, find_by: str="xpath", condition: str="html"):
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


    def condition(self, type, text):
        pass


    def condition_by(self, type):
        if type == "id":
            return By.ID
        elif type == "class":
            return By.CLASS_NAME
        elif type == "xpath":
            return By.XPATH


    # @retry(GetTimeoutException, tries=__tries)
    def get_with_retry(self):
        if self.__is_getting:
            return

        self.__is_getting = True

        self.__browser.get(self.__url)

        wait = WebDriverWait(self.__browser, timeout=self.__timeout)

        try:
            element = wait.until(
                visibility_of_element_located((
                    self.__find_by, 
                   self.__condition 
                ))
            )
            self.__is_getting = False
            self.signals.url_get_state.emit(1)
        except TimeoutException:
            raise GetTimeoutException
        finally:
            self.__is_getting = False
    

    @property
    def page_source(self):
        return self.browser.page_source
