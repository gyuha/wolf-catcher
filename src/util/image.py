import math
import os
from PIL import Image as PILImage


def __convert(image_path):
    try:
        source = PILImage.open(image_path)
        source.save(image_path, quality=95, optimize=True)
    except:
        return


def images_compress(save_path):
    for f in os.listdir(save_path):
        fname = os.path.join(save_path, f)
        __convert(fname)


if __name__ == "__main__":
    images_compress("...")
