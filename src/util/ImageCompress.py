from pickletools import optimize
import threading
from PIL import Image as PILImage
import os
import PySide6.QtCore
from PySide6.QtCore import QObject, QThread, Signal, Slot


class ImageCompressSignal(QObject):
    # id, complete, current, total
    image_compress_state = Signal(str, bool, int, int)


class ImageCompress(QThread):
    signals = ImageCompressSignal()

    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.parent = parent

    def set_chapter_path(self, id: str, chapter_path: str):
        self.id = id
        self.chapter_path = chapter_path

    def run(self):
        self.create_compress_thread()

    def create_compress_thread(self):
        compress_thread = threading.Thread(
            target=self.__image_compress
        )
        compress_thread.start()

    def __image_compress(self):
        try:
            files = os.listdir(self.chapter_path)
            file_count = len(files)
            for idx, f in enumerate(files):
                file_path = os.path.join(self.chapter_path, f)
                source = PILImage.open(file_path)
                source.save(file_path, quality=90, optimize=True)
                self.signals.image_compress_state.emit(
                    self.id, False, idx + 1, file_count)
        except:
            self.signals.image_compress_state.emit(
                self.id, True, file_count, file_count)

        self.signals.image_compress_state.emit(self.id, True, file_count, file_count)
