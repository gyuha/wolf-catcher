import importlib
from operator import attrgetter
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Slot
from src.site.Wfwf import WfWf

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

        self.init_sites()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_slot()

    def init_slot(self):
        """Initial Slots"""
        self.clipbard.add_clipboard.connect(self.add_clipboard)

    def load_module_func(self, module_name):
        mod = importlib.import_module(module_name)
        return mod

    def init_sites(self):
        self.sites = []

        for config in self.config.data["site"]:
            mod = self.load_module_func("src.site."+config["class_name"])
            print('📢[MainWindow.py:44]: ', mod)
            # mod = importlib.import_module(
            #     "src.site."+config["class_name"], config["class_name"])
            # print('📢[MainWindow.py:42]: ', mod(config))

            # self.sites.append(mod(config))

        for site in self.sites:
            print('📢[MainWindow.py:40]: ', site.site_name)

    @Slot(str, result=None)
    def add_clipboard(self, text: str, config: object):
        print('📢[MainWindow.py:31]: ', config)
        self.ui.statusbar.showMessage(text)
