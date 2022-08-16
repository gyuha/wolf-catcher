import PySide6.QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QListWidgetItem, QMainWindow
from DownloadItem import DownloadItem

from ui.Ui_MainWindow import Ui_MainWindow
from util.Clipboard import Clipboard
from util.Config import Config
from util.Downloader import Downloader

from util.Site import Site
from src.util.SeleniumWorker import SeleniumWorker
from util.message import alert


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.config = Config()

        self.clipbard = Clipboard()
        self.sites = Site()

        self.seleniumWorker = SeleniumWorker()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_connect()
        self.init_slot()

        widget = DownloadItem()

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

        downloader = Downloader()
        downloader.signals.download_state.connect(self.download_state)
        downloader.add_files("./wfwf/카구야 님은 고백받고 싶어",
                             [
                                 "https://img8cloud.net/13991/ec7450ed_281_0.jpg",
                                 "https://img8cloud.net/13991/ec7450ed_281_1.jpg",
                                 "https://img8cloud.net/13991/ec7450ed_281_2.jpg",
                                 "https://img8cloud.net/13991/ec7450ed_281_3.jpg"
                             ],
                             "https://wfwf220.com/"
                             )
        downloader.download_run()
        # self.seleniumWorker.get_with_retry(
        #     "https://wfwf220.com/cv?toon=13766&num=1&title=%BA%F9%B0%CB%C0%C7%B8%B6%BC%FA%BB%E7%B0%A1%BC%BC%B0%E8%B8%A6%B4%D9%BD%BA%B8%B0%B4%D9%BC%BC%B0%E8%C3%D6%B0%AD%C0%C7%B8%B6%BC%FA%BB%E7%C0%CE%BC%D2%B3%E2%C0%BA%B8%B6%BC%FA%C7%D0%BF%F8%BF%A1%C0%D4%C7%D0%C7%D1%B4%D911%C8%AD",
        #     "xpath",
        #     "/html/body/section[1]/div[5]/img[1]"
        #     )
    
    @Slot(int)
    def download_state(self, num):
        print('📢[MainWindow.py:67] => complete', num)

