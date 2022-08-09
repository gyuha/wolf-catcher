from src.util.Singleton import Singleton
import yaml

class Config(metaclass=Singleton):

    def __init__(self):
        super(Config, self).__init__()
        self.readData()
    
    def readData(self):
        with open('config.yaml', 'r', encoding='utf-8') as file:
            self._data = yaml.load(file, Loader=yaml.FullLoader)

    @property
    def data(self):
        return self._data

    

