from PySide6.QtCore import QObject
from src.util.Singleton import Singleton


class WebCrawring(QObject):

    def __init__(self):
        super(WebCrawring, self).__init__()