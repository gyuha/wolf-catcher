import PySide6.QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QListWidgetItem, QMainWindow
from DownloadItem import DownloadItem

from ui.Ui_MainWindow import Ui_MainWindow
from util.Clipboard import Clipboard
from util.Config import Config
from util.Downloader import Downloader

from src.site.Site import Site
from src.util.SeleniumWorker import SeleniumWorker
from util.message import alert


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.config = Config()

        self.clipbard = Clipboard()
        self.site = Site()

        self.seleniumWorker = SeleniumWorker()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_connect()
        self.init_slot()

        widget = DownloadItem()
        my_item = QListWidgetItem(self.ui.item_list)
        my_item.setSizeHint(widget.sizeHint())
        self.ui.item_list.addItem(my_item)
        self.ui.item_list.setItemWidget(my_item, widget)


        # self.ui.item_list.setItemWidget()


    def init_connect(self):
        self.ui.getButton.clicked.connect(self.get_button)

    def init_slot(self):
        """Initial Slots"""
        self.clipbard.add_clipboard.connect(self.add_clipboard)
    

    @Slot(str, result=None)
    def add_clipboard(self, text: str, config: object):
        print('📢[MainWindow.py:31]: ', config)
        self.ui.statusbar.showMessage(text)

    def get_button(self):
        if self.seleniumWorker.is_getting:
            return

        Downloader().download_image_from_url("https://img8cloud.net/13991/ec7450ed_281_0.jpg",
                                             "./test/a.jpg", "https://wfwf220.com/")

    @Slot(int)
    def download_state(self, num):
        print('📢[MainWindow.py:67] => complete', num)


    def get_site_config(self, url: str):
        config = self.config.get_site_config(url)

        if config in self.site.sites:
            return self.site.sites[config]

        raise Exception("It's an invalid site.")
