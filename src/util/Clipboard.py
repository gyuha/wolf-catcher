import PySide6.QtWidgets
from src.util.Singleton import Singleton
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QClipboard
from PySide6.QtCore import QObject, Signal 

class Clipboard(QObject):
    on_add_clipboard = Signal(str)

    def __init__(self):
        super(Clipboard, self).__init__()
        self.last_text = QApplication.clipboard().text()
        QApplication.clipboard().dataChanged.connect(self.clipboard_changed)
    

    def clipboard_changed(self):
        text = QApplication.clipboard().text()

        if not text.strip() or self.last_text.__eq__(text):
            return
        self.last_text = text
        self.on_add_clipboard.emit(text)
    