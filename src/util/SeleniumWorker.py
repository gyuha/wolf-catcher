from lib2to3.pgen2 import driver
from selenium import webdriver

from PySide6.QtCore import Signal

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from util.QtSingleton import QtSingleton


class SeleniumWorker(QtSingleton):
    progress_changed = Signal(int)

    current_browser = 'firefox'
    browser = None


    def driver_init(self):
        print("Web Driver loading...", end="\r")
        options = Options()
        # options.add_argument("--headless")
        # options.add_argument("--log-level=3")
        # options.add_argument('--disable-gpu')

        if self.current_browser == 'chrome':
            driver_file = './driver/chromedriver.exe'
            self.browser = webdriver.Chrome(
                driver_file, chrome_options=options)
        elif self.current_browser == 'firefox':
            driver_file = './driver/geckodriver.exe'
            self.browser = webdriver.Firefox(
                executable_path=driver_file, firefox_options=options)

        if self.browser:
            self.browser.implicitly_wait(5)


    def driver_close(self):
        if self.browser:
            self.browser.close()


    def reconnect(self):
        if self.browser:
            self.browser.close()
            self.browser = self.driver_init()


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
