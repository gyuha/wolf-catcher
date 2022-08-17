import importlib
from PySide6.QtCore import QObject, Signal, SignalInstance

from util.Config import Config
from util.SeleniumWorker import SeleniumWorker

class Site(QObject):

    def __init__(self, seleniumWorker: SeleniumWorker) -> None:
        super(Site, self).__init__()
        self.seleniumWorker = seleniumWorker
        self.config = Config()
        self.init_sites()


    def init_sites(self):
        self.sites = dict()

        for config in self.config.data["site"]:
            print('📢[Site.py:18]: ', config)
            class_module = getattr(importlib.import_module(
                "src.site."+config["class_name"]), config["class_name"])
            module = class_module(self.seleniumWorker, config)
            self.sites[module.site_name] = module

        # for key in self.sites:
        #     print('📢[Site.py:24]: ', self.sites[key].site_name)
        #     print('📢[Site.py:24]: ', self.sites[key].get_chapter_list("http://www."))
    

    def get_config_by_url(self, url: str):
        config = self.config.get_site_config(url)

        if config is None:
            raise Exception("Could not find config")

        if config["name"] in self.sites:
            return self.sites[config["name"]]

        raise Exception("It's an invalid site.")
