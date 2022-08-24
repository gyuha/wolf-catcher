import requests
from PySide6.QtCore import QObject, QThread, Signal, Slot, QSize, Qt
from util.Config import Config
from bs4 import BeautifulSoup
from util.message import toast
from plyer import notification


class UpdateDomain(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.parent = parent
        self.config = Config()

    def run(self):
        self.update_domain()

    def update_domain(self):
        try:
            html = requests.get(self.config.setting["link_url"])
            bs = BeautifulSoup(html.text, "html.parser", from_encoding='utf-8')
            t = bs.select("body > section > div > ul > li:nth-child(1) > a")
            href = t[0].get('href')
            self.config.data["site"][0]["url"] = href
            self.config.save()
            notification.notify(title="업데이트", message=href, app_name="Wolf", timeout=3)
        except Exception as e:
            print('📢 ', e)
