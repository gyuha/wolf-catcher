import yaml
import re

from util.Singleton import Singleton

class Config():

    @property
    def data(self):
        return self._data


    def __init__(self):
        super(Config, self).__init__()
        self.read_data()
    

    def read_data(self):
        with open('config.yaml', 'r', encoding='utf-8') as file:
            self._data = yaml.load(file, Loader=yaml.FullLoader)


    def get_site_config(self, url: str):
        for data in self._data["site"]:
            for filter in data["filter"]:
                if re.search(filter, url):
                    return data

