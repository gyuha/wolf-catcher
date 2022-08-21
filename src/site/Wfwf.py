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

    def get_chapter_info_parser(self, driver: webdriver):
        title = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[3]/h1').text.strip()

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


        info = self.title_info.info
        info["title"] = title
        info["tags"] = tags
        info["id"] = self.id
        info["author"] = author
        info["series"] = series
        info["thumbnail"] = thumbnail

        self.thumbnail_path = os.path.join(self.path, "thumbnail.jpg")

        self.title_info.save()
        self.parent.update_info(info)
        self.download_thumbnail(thumbnail, self.thumbnail_path)

        self.get_chapter_list(driver)


    def get_chapter_list(self, driver: webdriver):
        chapters = driver.find_elements(By.CSS_SELECTOR, "#content > div.box > div.group.left-box > div.webtoon-bbs-list.bbs-list > ul:nth-child(1) > li > a")
        chapters = list(reversed(chapters))
        for chapter in chapters:
            print('📢[Wfwf.py:60]: ', chapter.get_attribute('href'))


    def get_img_list(self, url):
        print("📢[Wfwf.py:17]: ", url)
