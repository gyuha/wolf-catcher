import re
import threading
import time
from enum import Enum

from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import QListWidgetItem, QMainWindow

from DownloadItem import DOWNLOAD_ITEM_STATE, DownloadItem
from lib.QToaster import QToaster
from src.site.browser.BrowserDriver import BrowserDriver
from src.site.TitleInfo import TitleInfo
from ui.Ui_MainWindow import Ui_MainWindow
from util.Clipboard import Clipboard
from util.Config import Config
from util.DatabaseManager import DatabaseManager
from util.message import toast
from util.UpdateDomain import UpdateDomain

# from util.Scraper import Scraper


class ADD_BY(Enum):
    DATABASE = 0
    CLIPBOARD = 1


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.config = Config()

        self.clipbard = Clipboard()

        # self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle("Wolf catcher")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__init_connect()
        self.__init_slot()
        self.item_dict: dict[str, QListWidgetItem] = {}
        self.item_counter = 0
        self.ui.item_list.setStyleSheet(
            "QListWidget::item { border-bottom: 1px solid #eee; }"
        )
        self.db = DatabaseManager()
        self.browser = BrowserDriver()
        self.current_key = ""
        self.__get_items_by_database()
        self.get_button()

    def __init_connect(self):
        self.ui.getButton.clicked.connect(self.get_button)
        self.ui.complete_delete_button.clicked.connect(self.__complete_delete)
        self.ui.site_open_button.clicked.connect(self.__on_site_open_button)

        self.ui.item_list.setDragEnabled(True)
        self.ui.item_list.setAcceptDrops(True)
        self.ui.item_list.dragEnterEvent = self.__dragEnterEvent
        self.ui.item_list.dragMoveEvent = self.__dragMoveEvent
        self.ui.item_list.dropEvent = self.__drop_event

        self.ui.action_exit.triggered.connect(lambda _: self.close())

        self.ui.cb_use_upscale.setChecked(self.config.setting["use_upscale"])
        self.ui.cb_use_upscale.clicked.connect(self.__on_change_upscale)

    def __init_slot(self):
        """Initial Slots"""
        self.clipbard.add_clipboard.connect(self.add_clipboard)

    def __dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def __dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
    
    def __on_change_upscale(self, event):
        self.config.setting["use_upscale"] = event
        self.config.save()


    def __drop_event(self, event: QDropEvent):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                # https://doc.qt.io/qt-5/qurl.html
                if url.isLocalFile():
                    continue
                else:
                    self.add_clipboard(url.toString())
        else:
            event.ignore()

    def __get_items_by_database(self):
        prds = self.db.get_visible_products()
        if prds is None:
            return
        for prd in prds:
            site_config = self.config.get_site_config_by_name(prd.site)
            if site_config is None:
                return
            self.add_item(prd.id, site_config, ADD_BY.DATABASE)
        self.__update_count()

    @Slot(str, object)
    def add_clipboard(self, text: str):
        self.ui.statusbar.showMessage(text)

        id, site_config = self.__url_validate(text)
        if id is None:
            return
        self.add_item(id, site_config, ADD_BY.CLIPBOARD)
        self.__update_count()

    def get_button(self):
        # self.__start_download()
        update_domain = UpdateDomain(self)
        update_domain.start()

    def __url_validate(self, url) -> str:
        site_config = self.config.get_site_config_by_url(url)
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

    def __widget_title_info(self, id):
        prd = self.db.get_product(id)
        if prd is None:
            return None
        info = {
            "title": prd.title,
            "author": prd.author,
            "tags": prd.tags.split("/"),
            "id": id,
        }
        return info

    # region item_list
    def add_item(self, id: str, site_config, by: ADD_BY):

        if self.__check_exist_item(id, site_config) == False:
            return

        if by == ADD_BY.CLIPBOARD:
            self.db.insert_product(id, site_config["name"])

        self.item_dict[site_config["name"] + id] = None  # 임시로 미리 등록 해 준다.
        widget = DownloadItem(id, site_config)

        info = self.__widget_title_info(id)
        if info is not None:
            widget.update_info(info, False)

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
        wd = self.__get_widget(key)
        if wd is not None:
            self.db.set_visible_product(wd.id, False)
        item = self.item_dict[key]
        self.ui.item_list.takeItem(self.ui.item_list.row(item))
        del self.item_dict[key]

    @Slot()
    def clear_item_list(self):
        for i in range(self.ui.item_list.count()):
            item = self.ui.item_list.item(i)
            widget = self.ui.item_list.itemWidget(item)
            if widget is not None:
                self.db.set_visible_product(widget.id, False)
        self.ui.item_list.clear()
        self.item_dict.clear()

    @Slot(str, DOWNLOAD_ITEM_STATE)
    def __on_download_state(self, key: str, state: DOWNLOAD_ITEM_STATE):
        if self.current_key != key:
            return
        if state == DOWNLOAD_ITEM_STATE.DONE or state == DOWNLOAD_ITEM_STATE.ERROR:
            # 완료 된 목록 끄기
            widget = self.__get_widget(key)
            if widget is not None:
                self.db.set_visible_product(widget.id, False)
            self.__start_download()

    def __get_widget(self, key: str):
        for i in range(self.ui.item_list.count()):
            item = self.ui.item_list.item(i)
            widget = self.ui.item_list.itemWidget(item)
            if widget is not None and widget.key == key:
                return widget
        return None

    def __update_count(self):
        self.ui.total_label.setText(str(self.ui.item_list.count()))
        count = 0
        for i in range(self.ui.item_list.count()):
            item = self.ui.item_list.item(i)
            widget = self.ui.item_list.itemWidget(item)
            if widget is not None:
                if widget.state == DOWNLOAD_ITEM_STATE.DONE:
                    count += 1
        self.ui.downloaded_label.setText(str(count))

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

        self.__update_count()
        for i in range(self.ui.item_list.count()):
            item = self.ui.item_list.item(i)
            widget = self.ui.item_list.itemWidget(item)
            if widget is not None:
                if widget.state == DOWNLOAD_ITEM_STATE.READY:
                    if self.current_key == widget.key:
                        continue
                    self.current_key = widget.key
                    widget.start()
                    return

    def __complete_delete(self):
        for i in reversed(range(self.ui.item_list.count())):
            item = self.ui.item_list.item(i)
            widget = self.ui.item_list.itemWidget(item)
            if widget is not None:
                if widget.state == DOWNLOAD_ITEM_STATE.DONE:
                    self.remove_item(widget.key)
        self.__update_count()

    # endregion

    def __on_site_open_button(self):
        url = QtCore.QUrl(self.config.setting["link_url"])
        QtGui.QDesktopServices.openUrl(url)
