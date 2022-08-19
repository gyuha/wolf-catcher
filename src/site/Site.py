import importlib
from PySide6.QtCore import QObject, Signal, SignalInstance
from lib.Singleton import Singleton

from util.Config import Config


class Site():
    def __init__(self, url: str) -> None:
        self.config = Config()
        self.load_site_class(url)

    def load_site_class(cls, url):
        config = cls.config.get_site_config(url)

        if config is None:
            raise Exception("Could not find config")

        class_module = getattr(
            importlib.import_module("src.site." + config["class_name"]),
            config["class_name"],
        )
        module = class_module(config)
        return module
