import os
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
        title = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[3]/h1').text.strip()
        print('📢[Wfwf.py:27]: ', title)

        if not title:
            raise Exception('제목을 찾을 수 없습니다.')

        self.path = self.download_path_init(self.download_path, title)
        self.title_info.set_path(self.download_path, title)
        self.title_info.load()

        text = driver.find_element(By.XPATH, '/html/body/section/div[2]/div[3]/div[2]').text
        tags = text.split(":")[1].strip().split("/")

        text = driver.find_element(By.XPATH, '/html/body/section/div[2]/div[3]/div[1]').text
        sp = text.split("작가 :")
        author = sp[1].strip()
        series = sp[0].split("연재일 :")[1].strip()

        thumbnail = driver.find_element(By.XPATH, '/html/body/section/div[2]/div[2]/img').get_attribute('src')

        self.download_thumbnail(thumbnail, os.path.join(self.path, "thumbnail.jpg"))

        info = self.title_info.info
        info["title"] = title
        info["tags"] = tags
        info["id"] = self.id
        info["author"] = author
        info["series"] = series
        info["thumbnail"] = thumbnail

        self.title_info.save()

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
