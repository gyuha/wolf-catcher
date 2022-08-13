from PySide6.QtCore import QObject

class QtSingleton(QObject):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = QObject.__new__(cls, *args, **kwargs)
            return cls.__instance
