from PySide6 import QtWidgets


def alert(text):
    error_dialog = QtWidgets.QErrorMessage()
    error_dialog.showMessage(text)