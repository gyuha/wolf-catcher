from PySide6.QtWidgets import QWidget
from ui.Ui_DownloadItem import Ui_DownloadItem

class DownloadItem(QWidget):
    def __init__(self):
        super(DownloadItem, self).__init__()
        self.ui = Ui_DownloadItem()
        self.ui.setupUi(self)