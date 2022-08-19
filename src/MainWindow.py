import re
from PySide6 import QtCore
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QListWidgetItem, QMainWindow
from DownloadItem import DownloadItem
from lib.QToaster import QToaster

from ui.Ui_MainWindow import Ui_MainWindow
from util.Clipboard import Clipboard
from util.Config import Config
from util.message import toast


# from util.Scraper import Scraper


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.config = Config()

        self.clipbard = Clipboard()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_connect()
        self.init_slot()
        self.item_dict: dict[str, QListWidgetItem] = {}
        self.item_counter = 0

        # self.ui.item_list.setItemWidget()

    def init_connect(self):
        self.ui.getButton.clicked.connect(self.get_button)

    def init_slot(self):
        """Initial Slots"""
        self.clipbard.add_clipboard.connect(self.add_clipboard)

    @Slot(str, object)
    def add_clipboard(self, text: str, config: object):
        print("📢[MainWindow.py:52]: ", config)
        print("📢[MainWindow.py:52]: ", text)
        self.ui.statusbar.showMessage(text)
        # self.add_item_list(text, site);
    
    def get_button(self):

        # QToaster.showMessage(self, "test", corner=QtCore.Qt.TopLeftCorner, timeout=1000, closable=False)
        url = "https://wfwf221.com/cl?toon=13955&title=%C3%BC%C0%CE%BC%D2%B8%C7%C0%FC%B1%E2%C5%E9%B8%C7"
        self.add_item(url)

    def __url_validate(self, url) -> str:
        site_config = self.config.get_site_config(url)
        if site_config is None:
            toast(self, "사이트를 찾을 수 없습니다.")
            return
        mat = re.match(site_config["url_format"]["list"]["re"], url)
        if mat:
            return mat.group(1), site_config
        return None, None

    # region item_list
    def add_item(self, url: str):
        id, site_config = self.__url_validate(url)
        print('📢[MainWindow.py:64]: ', id)
        if id is None or site_config is None:
            toast(self, "아이디를 찾을 수 없습니다.")
            return

        widget = DownloadItem(id, site_config)
        self.item_dict[widget.key] = widget
        title_item = QListWidgetItem(self.ui.item_list)
        title_item.setSizeHint(widget.sizeHint())
        self.ui.item_list.addItem(title_item)
        self.ui.item_list.setItemWidget(title_item, widget)
        self.item_counter += 1

    @Slot()
    def remove_item(self):
        widget = self.sender()
        item = self.item_dict[widget.key]
        self.ui.item_list.takeItem(self.ui.item_list.row(item))
        del self.item_dict[widget.key]

    @Slot()
    def clear_item_list(self):
        self.ui.item_list.clear()
        self.item_dict.clear()

    # endregion
