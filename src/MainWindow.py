import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Slot

from src.ui.Ui_MainWindow import Ui_MainWindow
from src.util.WebCrawring import WebCrawring
from src.util.Clipboard import Clipboard
from src.util.Config import Config


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.config = Config()
        self.web_crawring = WebCrawring()
        self.clipbard = Clipboard()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_slot()
    
    def init_slot(self):
        """Initial Slots"""
        self.clipbard.on_add_clipboard.connect(self.on_add_clipboard)


    @Slot(str, result=None)
    def on_add_clipboard(self, text):
        self.ui.statusbar.showMessage(text)

