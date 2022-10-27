import os
import shutil
import threading
import zipfile
from enum import Enum
from multiprocessing import cpu_count

import PySide6.QtCore
from PySide6.QtCore import QObject, QThread, Signal, Slot


class COMPRESS_STATE(Enum):
    READY = 0,
    DOING = 1,
    DONE = 2,
    ERROR = 3,


class CompressorSignal(QObject):
    compress_state = Signal(str, COMPRESS_STATE)


class Compressor(QThread):
    signals = CompressorSignal()

    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.parent = parent

    def set_chapter_path(self, id: str, chapter_path: str):
        self.id = id
        self.chapter_path = chapter_path

    def run(self):
        self.create_compress_thread()

    def __get_done(self, path: str, remove_origin: bool):
        if remove_origin:
            shutil.rmtree(path, ignore_errors=True)
        self.signals.compress_state.emit(self.id, COMPRESS_STATE.DONE)

    def get_files_count(self, folder_path):
        dirListing = os.listdir(folder_path)
        return len(dirListing)

    def __zip_folder(self, path: str, filename: str, remove_origin=True):
        if self.get_files_count(path) == 0:
            self.__get_done(path, remove_origin)
            return

        """
        폴더 압축하기
        """
        if os.path.exists(filename):
            self.signals.compress_state.emit(self.id, COMPRESS_STATE.ERROR)

        try:
            zipf = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
            for f in os.listdir(path):
                zipf.write(os.path.join(path, f), os.path.basename(f))
            zipf.close()
        except:
            self.signals.compress_state.emit(self.id, COMPRESS_STATE.ERROR)

        self.__get_done(path, remove_origin)

    def create_compress_thread(self):
        compress_thread = threading.Thread(
            target=self.__zip_folder, args=(
                self.chapter_path, self.chapter_path + ".cbz")
        )
        compress_thread.start()

    @classmethod
    def zip_folder(cls, filename: str, path: str, remove_origin=False):
        """
        폴더 압축하기
        """
        zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
        for f in os.listdir(path):
            zipf.write(os.path.join(path, f), os.path.basename(f))
        zipf.close()

        if remove_origin:
            shutil.rmtree(path, ignore_errors=True)
