import importlib
from PySide6.QtCore import QObject, QThread, Signal, Slot
from lib.Singleton import Singleton
from src.site.SiteBase import SiteBase

from util.Config import Config


class SiteLoaderSignals(QObject):
    on_site_loaded = Signal(str)


class SiteLoader(QThread):
    signals = SiteLoaderSignals()

    def __init__(self, parent, key, config):
        QThread.__init__(self, parent)
        self.parent = parent
        self.__key = key
        self.__config = config
        self.site_class = None

    def run(self):
        self.load_site_class()

    def load_site_class(self):
        config = self.__config

        class_module = getattr(
            importlib.import_module("src.site." + config["class_name"]),
            config["class_name"],
        )

        self.site_class = class_module(config)
        self.signals.on_site_loaded.emit(self.__key)
