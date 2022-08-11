import json

class TitleInfo:

    def __init__(self):
        self.info = {
            'author': '',
            'skip': 0,
            'title': '',
            'tags': [],
            'id': 0,
            'last_updated': ''
        }


    def set_info(self, info):
        self.info = info
    

    def load(self, file_path):
        with open(file_path, "r") as json_file:
            self.info = json.load(json_file)
    

    def save(self, file_path):
        with open(file_path, 'w') as outfile:
            json.dump(self.info, outfile, indent=4)