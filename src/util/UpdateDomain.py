from PySide6.QtCore import QObject, QThread, Signal, Slot, QSize, Qt
from util.Config import Config


class UpdateDomain(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.__parent = parent
        self.browserDriver = parent.browserDriver
        self.config = Config()

    def run(self):
        pass

    def update_domain(self):
        pass
