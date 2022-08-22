import re
import threading
import time
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QListWidgetItem, QMainWindow
from DownloadItem import DOWNLOAD_ITEM_STATE, DownloadItem
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

        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setWindowTitle("Wolf catcher")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__init_connect()
        self.__init_slot()
        self.item_dict: dict[str, QListWidgetItem] = {}
        self.item_counter = 0
        self.ui.item_list.setStyleSheet( "QListWidget::item { border-bottom: 1px solid #eee; }" );


    def __init_connect(self):
        self.ui.getButton.clicked.connect(self.get_button)

    def __init_slot(self):
        """Initial Slots"""
        self.clipbard.add_clipboard.connect(self.add_clipboard)
    
    @Slot(str, object)
    def add_clipboard(self, text: str, config: object):
        self.ui.statusbar.showMessage(text)
        self.add_item(text)
        # self.add_item_list(text, site);
    
    def get_button(self):
        self.__start_download()

    def __url_validate(self, url) -> str:
        site_config = self.config.get_site_config(url)
        if site_config is None:
            toast(self, "사이트를 찾을 수 없습니다.")
            return
        mat = re.match(site_config["url_format"]["title"]["re"], url)
        if mat:
            return mat.group(1), site_config
        return None, None
    
    def __check_exist_item(self, id, site_config) -> bool:
        key = site_config["name"] + id
        if key in self.item_dict:
            toast(self, "이미 등록된 키입니다.")
            return False
        return True

    # region item_list
    def add_item(self, url: str):
        id, site_config = self.__url_validate(url)

        if self.__check_exist_item(id, site_config) == False:
            return

        self.item_dict[site_config["name"] + id] = None # 임시로 미리 등록 해 준다.
        widget = DownloadItem(id, site_config)

        if self.item_counter == 0:
            widget.signals.remove_item.connect(self.remove_item)
            widget.signals.download_state.connect(self.__on_download_state)

        title_item = QListWidgetItem(self.ui.item_list)
        self.item_dict[widget.key] = title_item
        title_item.setSizeHint(widget.sizeHint())
        self.ui.item_list.addItem(title_item)
        self.ui.item_list.setItemWidget(title_item, widget)
        self.item_counter += 1
        self.__start_download()

    @Slot(str)
    def remove_item(self, key: str):
        item = self.item_dict[key]
        self.ui.item_list.takeItem(self.ui.item_list.row(item))
        del self.item_dict[key]

    @Slot()
    def clear_item_list(self):
        self.ui.item_list.clear()
        self.item_dict.clear()
    
    @Slot(str, DOWNLOAD_ITEM_STATE)
    def __on_download_state(self, key: str, state: DOWNLOAD_ITEM_STATE):
        if self.current_key != key:
            return
        if state == DOWNLOAD_ITEM_STATE.DONE or state == DOWNLOAD_ITEM_STATE.ERROR:
            self.__start_download()
    
    def __check_download_possible(self):
        """
        현재 다운로드 중인게 있는지 체크
        """
        for i in range(self.ui.item_list.count()):
            item = self.ui.item_list.item(i)
            widget = self.ui.item_list.itemWidget(item)
            if widget is not None:
                if widget.state == DOWNLOAD_ITEM_STATE.DOING:
                    return False
            return True
    
    def __start_download(self):
        if self.__check_download_possible() == False:
            return
        print('📢[MainWindow.py:129]: ', self.ui.item_list.count())
        for i in range(self.ui.item_list.count()):
            item = self.ui.item_list.item(i)
            widget = self.ui.item_list.itemWidget(item)
            if widget is not None:
                if widget.state == DOWNLOAD_ITEM_STATE.READY:
                    self.current_key = widget.key
                    widget.start()
                    break;

    # endregion
