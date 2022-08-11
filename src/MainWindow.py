from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot

from ui.Ui_MainWindow import Ui_MainWindow
from util.WebCrawring import WebCrawring
from util.Clipboard import Clipboard
from util.Config import Config

from src.site.Site import Site


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.config = Config()
        self.web_crawring = WebCrawring()
        self.clipbard = Clipboard()
        self.sites = Site()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_slot()

    def init_slot(self):
        """Initial Slots"""
        self.clipbard.add_clipboard.connect(self.add_clipboard)

    @Slot(str, result=None)
    def add_clipboard(self, text: str, config: object):
        print('📢[MainWindow.py:31]: ', config)
        self.ui.statusbar.showMessage(text)
