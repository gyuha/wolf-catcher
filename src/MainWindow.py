import sys
from PySide6.QtWidgets import QApplication, QMainWindow

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

        