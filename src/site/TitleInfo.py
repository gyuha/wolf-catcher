import os
import yaml


class TitleInfo:
    def __init__(self):
        self.id = None
        # 챕터 정보
        self.info = {
            "author": "",
            "skip": 0,
            "title": "",
            "series": "",
            "tags": [],
            "id": 0,
            "last_updated": "",
            "thumbnail": "",
        }
        # 챕터 목록 ID
        self.list = []
        self.file_name = "title.yaml"

        self.path = ""

    def set_path(self, base_path, title):
        self.path = os.path.join(base_path, title, self.file_name)

    def set_info(self, info):
        self.info = info

    def load(self):
        if not os.path.exists(self.path):
            return
        with open(self.path, "r", encoding="utf-8") as file:
            self.info = yaml.load(file, Loader=yaml.FullLoader)

    def save(self):
        with open(self.path, "w", encoding="utf-8") as outfile:
            print('📢[TitleInfo.py:38]: ', self.info)
            yaml.dump(self.info, outfile, allow_unicode=True)
