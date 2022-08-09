import PySide6.QtWidgets
from src.util.Singleton import Singleton
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QClipboard

class Clipboard(metaclass=Singleton):

    def __init__(self):
        super(Clipboard, self).__init__()
        QApplication.clipboard().dataChanged.connect(self.clipboard_changed)
    

    def clipboard_changed(self):
        text = QApplication.clipboard().text()
        print('📢[Clipboard.py:15]: ', text)
    