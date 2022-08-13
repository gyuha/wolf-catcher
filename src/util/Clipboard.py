from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, SignalInstance

from util.Config import Config 


class Clipboard(QObject):
    add_clipboard: SignalInstance  = Signal(str, object)

    def __init__(self) -> None:
        super(Clipboard, self).__init__()
        self.last_text = QApplication.clipboard().text()
        self.config = Config()
        QApplication.clipboard().dataChanged.connect(self.clipboard_changed)
    

    def clipboard_changed(self):
        text = QApplication.clipboard().text()

        if not text.strip() or self.last_text.__eq__(text):
            return
        site = self.config.get_site_config(text)

        if not site:
            return;

        self.last_text = text
        self.add_clipboard.emit(text, site)
    