from PySide6 import QtWidgets
from PySide6 import QtCore

from lib.QToaster import QToaster


def alert(text):
    error_dialog = QtWidgets.QErrorMessage()
    error_dialog.showMessage(text)

def toast(self, text):
    QToaster.showMessage(self, text, corner=QtCore.Qt.TopRightCorner, timeout=1000, closable=False)