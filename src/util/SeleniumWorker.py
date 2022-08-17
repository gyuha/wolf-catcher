import urllib

from selenium import webdriver

from PySide6.QtCore import QObject

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import visibility_of_element_located

from lib.exceptions import GetTimeoutException
from util.Config import Config

from util.QtSingleton import QtSingleton

import urllib


class SeleniumWorker(QObject, metaclass=QtSingleton):

    __browser = None
    __browser_type = 'firefox'
    __tries = 5
    __timeout = 10
    __is_getting = False
    __is_complete = False

    @property
    def browser(self):
        return self.__browser

    @property
    def is_getting(self):
        return self.__is_getting

    @property
    def is_complete(self):
        return self.__is_complete


    def __init__(self):
        super().__init__()
        self.config = Config()
        self.__is_getting = False

        self.__browser_type = self.config.setting["browser"]
        print('📢[SeleniumWorker.py:50]: ', self.config.setting["headless"])
        self.__driver_init()


    def __driver_init(self):

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
    def get_with_retry(self, url, type = "xpath", text = "html"):
        if (self.__is_getting):
            return

        self.__is_complete = False
        self.__is_getting = True
        self.__browser.get(url)

        wait = WebDriverWait(self.__browser, timeout=self.__timeout)

        try:
            element = wait.until(
                visibility_of_element_located((
                    type, 
                    "/html"
                ))
            )
            self.__is_getting = False
            self.__is_complete = True
        except TimeoutException:
            self.__is_complete = False
            raise GetTimeoutException

        self.__is_getting = False
        return
    
    @property
    def page_source(self):
        return self.browser.page_source
