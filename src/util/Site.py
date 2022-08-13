import importlib
from PySide6.QtCore import QObject, Signal, SignalInstance

from util.Config import Config

class Site(QObject):

    def __init__(self) -> None:
        super(Site, self).__init__()
        self.config = Config()
        self.init_sites()


    def init_sites(self):
        self.sites = dict()

        for config in self.config.data["site"]:
            class_module = getattr(importlib.import_module(
                "src.site."+config["class_name"]), config["class_name"])
            module = class_module(config)
            self.sites[module.site_name] = module

        for key in self.sites:
            print('📢[Site.py:24]: ', self.sites[key].site_name)
            print('📢[Site.py:24]: ', self.sites[key].get_chapter_list("http://www."))
