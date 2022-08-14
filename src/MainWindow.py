from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot

from ui.Ui_MainWindow import Ui_MainWindow
from util.Clipboard import Clipboard
from util.Config import Config

from util.Site import Site
from src.util.SeleniumWorker import SeleniumWorker


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
        print('📢[MainWindow.py:42]', self.seleniumWorker.is_getting)
        if self.seleniumWorker.is_getting:
            return
        self.seleniumWorker.get_with_retry("https://wfwf220.com/cl?toon=13766&title=%BA%F9%B0%CB%C0%C7%B8%B6%BC%FA%BB%E7%B0%A1%BC%BC%B0%E8%B8%A6%B4%D9%BD%BA%B8%B0%B4%D9%BC%BC%B0%E8%C3%D6%B0%AD%C0%C7%B8%B6%BC%FA%BB%E7%C0%CE%BC%D2%B3%E2%C0%BA%B8%B6%BC%FA%C7%D0%BF%F8%BF%A1%C0%D4%C7%D0%C7%D1%B4%D9")
