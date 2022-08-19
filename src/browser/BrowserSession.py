from src.lib.Singleton import Singleton

class BrowserSession(metaclass=Singleton):

    def __init__(self):
        self.__session = None
        self.__cookie = None


    @property
    def session(self):
        return self.__session


    @session.setter
    def data(self, value):
        self.__session = value
    

    @property
    def cookie(self):
        return self.__cookie
    

    @cookie.setter
    def cookie(self, value):
        self.__cookie = value