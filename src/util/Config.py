import yaml


class Config():

    def __init__(self):
        super(Config, self).__init__()
        self.read_data()
    
    def read_data(self):
        with open('config.yaml', 'r', encoding='utf-8') as file:
            self._data = yaml.load(file, Loader=yaml.FullLoader)

    @property
    def data(self):
        return self._data

    

