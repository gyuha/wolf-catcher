import PySide6.QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QListWidgetItem, QMainWindow
from DownloadItem import DownloadItem

from ui.Ui_MainWindow import Ui_MainWindow
from util.Clipboard import Clipboard
from util.Config import Config
from util.Downloader import Downloader

from src.site.Site import Site
from src.site.SiteBase import SiteBase
from src.util.SeleniumWorker import SeleniumWorker
# from util.Scraper import Scraper
from util.message import alert


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.config = Config()

        # self.Scraper = Scraper()
        self.seleniumWorker = SeleniumWorker(self)
        self.clipbard = Clipboard()
        self.site = Site(self.seleniumWorker)


        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_connect()
        self.init_slot()

        # self.ui.item_list.setItemWidget()


    def init_connect(self):
        self.ui.getButton.clicked.connect(self.get_button)

    def init_slot(self):
        """Initial Slots"""
        self.clipbard.add_clipboard.connect(self.add_clipboard)
    

    @Slot(str, object)
    def add_clipboard(self, text: str, config: object):
        print('📢[MainWindow.py:52]: ', config)
        print('📢[MainWindow.py:52]: ', text)
        self.ui.statusbar.showMessage(text)
        # self.add_item_list(text, site);

    def get_button(self):
        if self.seleniumWorker.is_getting:
            return

        url = "https://wfwf221.com/cl?toon=13955&title=%C3%BC%C0%CE%BC%D2%B8%C7%C0%FC%B1%E2%C5%E9%B8%C7"

        # self.seleniumWorker.url = url
        # self.seleniumWorker.start()
        self.add_item_list(
            url,
            self.site.get_config_by_url(url)
            )
        # Downloader().download_image_from_url("https://img8cloud.net/13991/ec7450ed_281_0.jpg",
        #                                      "./test/a.jpg", "https://wfwf220.com/")

    @Slot(int)
    def download_state(self, num):
        print('📢[MainWindow.py:67] => complete', num)


    
    # region item_list
    def add_item_list(self, url: str, site: SiteBase):
        widget = DownloadItem(url, site)
        my_item = QListWidgetItem(self.ui.item_list)
        my_item.setSizeHint(widget.sizeHint())
        self.ui.item_list.addItem(my_item)
        self.ui.item_list.setItemWidget(my_item, widget)

    # endregion
