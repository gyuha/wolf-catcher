from lib2to3.pgen2 import driver
from msilib.schema import Condition
from multiprocessing.connection import wait
# from selenium import webdriver
from seleniumwire import webdriver

from PySide6.QtCore import Signal

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium import webdriver
from lib.exceptions import GetTimeoutException
from util.Config import Config

from util.QtSingleton import QtSingleton

from retry import retry
from timeout_decorator import timeout, TimeoutError
import urllib

from .file_name import download_from_url


class SeleniumWorker(QtSingleton):
    progress_changed = Signal(int)

    __browser = None
    __browser_type = 'chrome'
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

        self.__driver_init()

    def __driver_init(self):
        print("[{}] Web Driver loading...".format(
            self.config.setting["browser"]), end="\r")

        if self.__browser_type == 'chrome':
            """ 
            Chrome
            """
            driver_file = './driver/chromedriver.exe'
            options = ChromeOptions()
            self.__browser = webdriver.Chrome(
                executable_path=driver_file,
                options=options)

        elif self.__browser_type == 'firefox':
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
                    self.condition_by(type), 
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
            
    
    def download_image(self, xpath):
        img = self.__browser.find_element(By.XPATH, xpath)
        src = img.get_attribute('src')

        print('📢[SeleniumWorker.py:141]: ', src)
        urllib.urlretrieve(src, "filename.png")
        # img.screenshot("test.png")
        with open('Logo.png', 'wb') as file:
            file.write(img.screenshot_as_png)
        print('📢[SeleniumWorker.py:141]: ', src)
        # download_from_url([src, './', 0])
        # download the image
        # urllib.urlretrieve(src, "my_image.png")

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
