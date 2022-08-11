import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile
from MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
