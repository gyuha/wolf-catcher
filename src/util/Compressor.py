import os
import shutil
import zipfile

class Compressor:

    @classmethod
    def zip_folder(cls, filename: str, path: str, remove_origin = False):
        """
        폴더 압축하기
        """
        zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
        for f in os.listdir(path):
            zipf.write(os.path.join(path, f), os.path.basename(f))
        zipf.close()

        if remove_origin:
            shutil.rmtree(path, ignore_errors=True)
