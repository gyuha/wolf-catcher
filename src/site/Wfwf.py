import os
from bs4 import BeautifulSoup as bs
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

    def get_chapter_info_parser(self, content: str):
        soup = bs(content, "html.parser")
        title = soup.select("#content > div:nth-child(2) > div.text-box > h1")[0].text
        # title = driver.find_element(
        #     By.XPATH, '//*[@id="content"]/div[2]/div[3]/h1'
        # ).text.strip()

        if not title:
            raise Exception("제목을 찾을 수 없습니다.")

        strip_title = self.strip_title_for_path(title)
        self.path = self.download_path_init(self.download_path, strip_title)
        self.title_info.set_path(self.download_path, strip_title)
        self.title_info.load()

        if self.name == "wfwf":
            text = soup.select(
                "#content > div:nth-child(2) > div.text-box > div:nth-child(3)"
            )[0].text
        else:
            text = soup.select("#content > div:nth-child(2) > div.text-box > div.sub")[
                0
            ].text
        tags = text.split(":")[1].strip().split("/")

        author = ""
        series = ""
        if self.name == "wfwf":
            text = soup.select(
                "#content > div:nth-child(2) > div.text-box > div:nth-child(2)"
            )[0].text
            sp = text.split("작가 :")
            author = sp[1].strip()
            series = sp[0].split("연재일 :")[1].strip()

        thumbnail = soup.select("#content > div:nth-child(2) > div.img-box > img")[0][
            "src"
        ]

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

        self.get_chapter_list(soup)

    def get_chapter_list(self, soup: bs):
        soup.find("div", class_="badge").decompose()
        soup.find("div", class_="date").decompose()

        chapters = soup.select(
            ".bbs-list > ul > li > a.view_open"
        )
        self.total_chapter = len(chapters)
        chapters = list(reversed(chapters))
        for chapter in chapters:
            href = chapter["href"]
            subject = chapter.text
            sp = subject.split("\n")
            subject = f"{sp[2].strip().zfill(3)}-{sp[3].strip()}"
            self.chapter_list.append([subject, href])

    def get_img_list(self, content: str):
        soup = bs(content, "html.parser")
        images = soup.select(
            ".image-view > img"
        )
        self.chapter_images = []
        for image in images:
            self.chapter_images.append(image["src"])
        return len(self.chapter_images) > 0

    def set_next_chapter(self):
        pass
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
