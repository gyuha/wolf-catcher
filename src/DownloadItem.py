from PySide6.QtWidgets import QWidget
from ui.Ui_DownloadItem import Ui_DownloadItem
from site.SiteBase import SiteBase

class DownloadItem(QWidget):

    def __init__(self, site: SiteBase):
        super(DownloadItem, self).__init__()
        self.ui = Ui_DownloadItem()
        self.ui.setupUi(self)
        self.site = site