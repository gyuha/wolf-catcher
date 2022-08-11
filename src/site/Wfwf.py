from PySide6.QtCore import QObject, Signal, SignalInstance
from src.site.SiteBase import SiteBase

class Wfwf(QObject, SiteBase):

    def __init__(self, config):
        SiteBase.__init__(self, config)

    @property
    def site_name(self):
        return self.name
