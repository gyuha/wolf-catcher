from PySide6.QtCore import QObject, QThread, Signal, Slot
from util.Config import Config
from selenium import webdriver
from src.site.SiteBase import SiteBase
from selenium.webdriver.common.by import By
from urllib.parse import urlparse


@SiteBase.register
class Wfwf(SiteBase):
    def __init__(self, config: Config):
        super().__init__(config)


    def get_title_id(self, url: str) -> str:
        return ""
    # @Slot(int)
    # def url_get_state(self, state: int):
    #     print("📢[Wfwf.py:15]: ", state)
    #     title = self.browerDriver.browser.find_element(
    #         "xpath", '//*[@id="content"]/div[2]/div[3]/h1'
    #     ).text
    #     print("📢[Wfwf.py:20]: ", title)

    def get_chapter_info_parser(self, driver: webdriver):
        print('📢[Wfwf.py:26]', self.id)
        title = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[3]/h1').text
        print('📢[Wfwf.py:27]: ', title)
        tag = driver.find_element(By.XPATH, '/html/body/section/div[2]/div[3]/div[2]').text
        print('📢[Wfwf.py:28]: ', tag)
        thumbnail = driver.find_element(By.XPATH, '/html/body/section/div[2]/div[2]/img').get_attribute('src')
        print('📢[Wfwf.py:28]: ', thumbnail)

        # self.browserDriver.set_url_info(
        #     url,
        #     self.url_format["list"]["visible_condition"]["type"],
        #     self.url_format["list"]["visible_condition"]["text"],
        # )
        # self.browserDriver.start()
        # self.seleniumWorker.get_with_retry(
        #     url,
        #     self.url_format["list"]["visible_condition"]["type"],
        #     self.url_format["list"]["visible_condition"]["text"]
        # )
        # browser = self.seleniumWorker.browser
        # title = browser.find_element(
        #     'xpath',
        #     "//*[@id=\"content\"]/div[2]/div[3]/h1").text
        # print('📢[Wfwf.py:20]: ', title)
        # print('📢[Wfwf.py:18]', self.seleniumWorker.page_source)

    def get_chapter_list(self, url):
        print("📢[Wfwf.py:14]: ", url)

    def get_img_list(self, url):
        print("📢[Wfwf.py:17]: ", url)
