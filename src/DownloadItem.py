import asyncio
from PySide6.QtWidgets import QWidget
from src.site.Site import Site
from ui.Ui_DownloadItem import Ui_DownloadItem
from src.site.SiteBase import SiteBase

class DownloadItem(QWidget):

    def __init__(self, url: str):
        print('📢[DownloadItem.py:10]: ', url)
        super(DownloadItem, self).__init__()
        self.ui = Ui_DownloadItem()
        self.ui.setupUi(self)

        self.url = url
        self.site = Site(url)
        print('📢[DownloadItem.py:16]: ', self.site)

        # 리스트 받기
        self.dowload_capter_list()
    
    def dowload_capter_list(self):
        print('📢[DownloadItem.py:17]: ', self.url)
        # self.site.get_chapter_info(self.url)