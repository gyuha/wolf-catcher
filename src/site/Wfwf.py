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

        self.chapter_list = []
        self.current_chapter = 0
        self.total_chapter = 0
        self.chapter_images = []

    def get_title_id(self, url: str) -> str:
        return ""

    def get_chapter_info_parser(self, driver: webdriver):
        title = driver.find_element(
            By.XPATH, '//*[@id="content"]/div[2]/div[3]/h1'
        ).text.strip()

        if not title:
            raise Exception("제목을 찾을 수 없습니다.")

        strip_title = self.strip_title_for_path(title)
        self.path = self.download_path_init(self.download_path, strip_title)
        self.title_info.set_path(self.download_path, strip_title)
        self.title_info.load()

        text = driver.find_element(
            By.XPATH, "/html/body/section/div[2]/div[3]/div[2]"
        ).text
        tags = text.split(":")[1].strip().split("/")

        text = driver.find_element(
            By.XPATH, "/html/body/section/div[2]/div[3]/div[1]"
        ).text
        sp = text.split("작가 :")
        author = sp[1].strip()
        series = sp[0].split("연재일 :")[1].strip()

        thumbnail = driver.find_element(
            By.XPATH, "/html/body/section/div[2]/div[2]/img"
        ).get_attribute("src")

        info = self.title_info.info
        info["title"] = title
        info["tags"] = tags
        info["id"] = self.id
        info["author"] = author
        info["series"] = series
        info["thumbnail"] = thumbnail

        self.current_chapter = int(info["skip"])

        self.title_info.save()
        self.parent.update_info(info, True)
        self.download_thumbnail(thumbnail, self.thumbnail_path)

        self.get_chapter_list(driver)

    def get_chapter_list(self, driver: webdriver):
        driver.execute_script('$(".badge").remove()')
        driver.execute_script('$(".date").remove()')
        chapters = driver.find_elements(
            By.CSS_SELECTOR,
            "#content > div.box > div.group.left-box > div.webtoon-bbs-list.bbs-list > ul:nth-child(1) > li > a",
        )
        self.total_chapter = len(chapters)
        chapters = list(reversed(chapters))
        for chapter in chapters:
            href = chapter.get_attribute("href")
            subject = chapter.find_element(By.CLASS_NAME, "list-box").text
            sp = subject.split("\n")
            subject = f'{sp[0].strip().zfill(3)}-{sp[1].strip()}'
            self.chapter_list.append([
                subject,
                href
            ])

    def get_img_list(self, driver: webdriver):
        images = driver.find_elements(By.CSS_SELECTOR,
            "body > section.webtoon-body > div.group.image-view > img"
        )
        self.chapter_images = []
        for image in images:
            self.chapter_images.append(image.get_attribute("src"))
    
    def set_next_chapter(self):
        self.current_chapter += 1
        self.title_info.info["skip"] = self.current_chapter
        self.title_info.save()

    def get_current_chapter(self):
        if self.current_chapter >= self.total_chapter:
            return [None, None]
        return self.chapter_list[self.current_chapter]

    @property
    def progress(self):
        return int((self.current_chapter + 1) / self.total_chapter * 100)