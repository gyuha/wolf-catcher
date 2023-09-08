from enum import Enum

from PySide6.QtCore import QObject, QThread, Signal
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from lib.exceptions import GetTimeoutException
from util.Config import Config


class BrowserDriver:
    def __init__(self):
        self.config = Config()
        # self.__timeout = self.config.setting["browser"]["timeout"]
        self.__browser_type = self.config.setting["browser"]
        self.__init_driver()

    def __init_driver(self):
        print("[{}] Web Driver loading...".format(self.__browser_type), end="\r")

        options = ChromeOptions()
        options.headless = self.config.setting["headless"]
        self.__browser = webdriver.Chrome(options=options)
        # self.__browser.get("https://www.google.com/")
        # driver.get("https://www.google.com/")
        # self.__browser = webdriver.Chrome(
        #     service=ChromeService(ChromeDriverManager().install()),
        #     options=options
        # )

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
