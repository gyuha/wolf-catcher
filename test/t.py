from PySide6.QtCore import QObject

class QtSingleton(QObject):
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = QObject.__new__(cls, *args, **kwargs)
        return cls.__instance


if __name__ == "__main__":
    class AA(QtSingleton):
        def __init__(self):
            super().__init__()
            self.num = 123

    class KK:
        def __init__(self):
            self.num = 55555


    print("----------- singletone 사용한 경우---------")

    aa = AA()
    bb = AA()

    print(aa)
    print(bb)

    print(aa.num)
    print(bb.num)

    aa.num = 333

    print(aa.num)
    print(bb.num)

    print("----------- singleton 아닌 경우---------")

    kk = KK()
    mm = KK()

    print(kk)

    print(mm)
