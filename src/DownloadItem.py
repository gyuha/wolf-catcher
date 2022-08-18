import asyncio
from PySide6.QtWidgets import QWidget
from ui.Ui_DownloadItem import Ui_DownloadItem
from src.site.SiteBase import SiteBase

class DownloadItem(QWidget):

    def __init__(self, url: str, site: SiteBase):
        super(DownloadItem, self).__init__()
        self.ui = Ui_DownloadItem()
        self.ui.setupUi(self)
        self.url = url
        self.site = site
        self.dowload_capter_list()
    
    def dowload_capter_list(self):
        print('📢[DownloadItem.py:17]: ', self.url)
        asyncio.run(self.site.get_chapter_info(self.url))