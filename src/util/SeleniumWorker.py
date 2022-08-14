from lib2to3.pgen2 import driver
from selenium import webdriver

from PySide6.QtCore import Signal

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from util.Config import Config

from util.QtSingleton import QtSingleton

from retry import retry
from timeout_decorator import timeout, TimeoutError


class SeleniumWorker(QtSingleton):
    progress_changed = Signal(int)

    __browser = None
    __brower_type = 'chrome'
    __tries = 5
    __timeout = 10
    __is_getting = False


    @property
    def brower(self):
        return self.__browser


    def __init__(self):
        super().__init__()
        self.config = Config()
        self.__is_getting = False

        self.__brower_type = self.config.setting["browser"]

        self.__driver_init()


    def __driver_init(self):
        print("[{}] Web Driver loading...".format(self.config.setting["browser"]), end="\r")

        if self.__brower_type == 'chrome':
            """ 
            Chrome
            """
            driver_file = './driver/chromedriver.exe'
            options = ChromeOptions()
            self.__browser = webdriver.Chrome(
                executable_path=driver_file, 
                options=options)

        elif self.__brower_type == 'firefox':
            """
            Firefox
            """
            driver_file = './driver/geckodriver.exe'
            options = FirefoxOptions()
            options.headless = False
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
            self.__browser = self.__driver_init()


    @retry(tries=__tries)
    def get_with_retry(self, url):
        self.__is_getting = True
        self.__browser.get(url)
        self.__is_getting = False


    def do_work(self):
        progress = 0
        browser = webdriver.Firefox()
        links = ['http://www.somesite.com/',
                 'http://www.somesite.com/page2',
                 'http://www.somesite.com/page3']

        for link in links:
            browser.get(link)
            progress += 100 / len(links)
            self.progress_changed.emit(progress)

        browser.close()
