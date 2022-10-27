import os
import sys

import PySide6.QtCore
from PySide6.QtCore import QObject, QThread, Signal, QProcess, Slot
from PySide6.QtWidgets import (
    QApplication,  QMainWindow, QVBoxLayout, QWidget, QPushButton, QProgressBar)


class UpscalerSignal(QObject):
    progress = Signal(bool, int, int)  # run, current, total


class Upscaler(QObject):
    signals = UpscalerSignal()

    def __init__(self, parent=None):
        self._parent = parent
        self.p = None
        self.total = 0
        self.path = ""
        self.currentIndex = 0
        self.file_list = []

    def get_files_count(self, folder_path):
        dirListing = os.listdir(folder_path)
        return len(dirListing)
    
    def file_path(self) -> str:
        return os.path.join(self.path, self.file_list[self.currentIndex])

    def start(self, path: str):
        if self.get_files_count(path) == 0:
            return
        
        self.path = path

        self.file_list = os.listdir(path)
        self.total = len(self.file_list)
        self.currentIndex = 0

        print('📢[Upscaler.py:37]: ', self.file_list[self.currentIndex])
        self.on_process_next()

    def output_filepath(self, path: str) -> str:
        return path.replace(".jpg", "-S.jpg")

    def _progress(self):
        self.p = QProcess()
        self.p.finished.connect(self.on_process_next)
        current_file = self.file_path()
        output_filepath = current_file.replace(".jpg", "-S.jpg").replace(".JPG", "-S.jpg")
        self.p.start("./realesrgan-ncnn-vulkan",
                     ["-i", current_file, "-o", current_file, "-f", "jpg", "-s", "2"])

    def on_process_next(self):
        if self.currentIndex >= self.total:
            self.signals.progress.emit(True, self.currentIndex, self.total)
            return

        self.signals.progress.emit(False, self.currentIndex, self.total)
        self.p = None
        self._progress()

        self.currentIndex = self.currentIndex + 1


class ProgressWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.p = None  # Default empty value.

        self.btn = QPushButton("Execute")
        self.btn.pressed.connect(self.start_process)

        self.pbar = QProgressBar(self)

        self.upscaler = Upscaler(self)
        self.upscaler.signals.progress.connect(self.on_progress)

        l = QVBoxLayout()
        l.addWidget(self.btn)
        l.addWidget(self.pbar)

        w = QWidget()
        w.setLayout(l)

        self.setCentralWidget(w)

    @Slot(bool, int, int)
    def on_progress(self, complete: bool, current: int, total: int):
        print('📢[Upscaler.py:81] {0} : {1}, {2}'.format(
            complete, current, total))
        progress = 0;
        if current != 0:
            progress = (current / total) * 100
        self.pbar.setValue(progress)
        self.btn.setEnabled(complete)

    def start_process(self):
        self.btn.setEnabled(False)
        self.upscaler.start("./wfwf/up")

    def process_finished(self):
        self.message("Process finished.")
        self.p = None


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = ProgressWindow()
    w.show()

    app.exec_()
