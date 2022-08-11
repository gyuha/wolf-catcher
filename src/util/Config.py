import yaml
import re

from util.Singleton import Singleton

class Config(metaclass=Singleton):

    def __init__(self):
        super(Config, self).__init__()
        self.read_data()
    
    def read_data(self):
        with open('config.yaml', 'r', encoding='utf-8') as file:
            self._data = yaml.load(file, Loader=yaml.FullLoader)

    @property
    def data(self):
        return self._data


    def get_site_config(self, url: str):
        for data in self._data["site"]:
            for filter in data["filter"]:
                if re.search(filter, url):
                    return data


    

