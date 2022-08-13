import os
import pathlib
import re
import shutil
import time
import zipfile
from multiprocessing import Pool, cpu_count
import requests
import tqdm

from util.image import images_compress

CUSTOM_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36'


def strip_file_path(path):
    """
    윈도우에서 사용이 가능한 파일 명으로 변경
    """
    path = re.sub(r"NEW\t+", "", path)

    path = path.replace('\n', '')
    path = re.sub(r"\t.*$", "", path)
    path = path.replace(':', '').replace('?', '').replace(
        '/', '').replace('!', '').replace('\\', '')
    path = path.replace("「", " ").replace("」", '').replace(".", "")
    path = path.replace("<", "").replace(">", "")

    path = path.strip()
    return path


def images_download(title, save_path, images):
    pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)
    target = []
    # c = Config()

    for i, img in enumerate(images):
        # img = re.sub(r"mangashow\d.me", c.getName(), img[0])
        target.append([img, save_path, i+1])

    pool = Pool(processes=cpu_count())
    try:
        # for tar in target:
        #     __downloadFromUrl(tar)
        for _ in tqdm.tqdm(pool.imap_unordered(__download_from_url, target),
                           total=len(target), ncols=68, desc="    Download", leave=False, timeout=60):
            pass
    finally:
        pool.close()
        pool.join()

    print(" "*80, end="\r")

    images_compress(save_path)

    zip_folder(save_path + "-" + strip_file_path(title) + ".cbz", save_path)
    shutil.rmtree(save_path, ignore_errors=True)


def timed_loop(iterator, timeout):
    start_time = time.time()
    iterator = iter(iterator)

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            raise TimeoutError("long_running_function took too long!")

        try:
            yield next(iterator)
        except StopIteration:
            pass


def zip_folder(filename, path):
    zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    for f in os.listdir(path):
        zipf.write(os.path.join(path, f), os.path.basename(f))
    zipf.close()


def __download_from_url(p):
    url = p[0]
    output_path = p[1]
    num = p[2]

    name = "%03d" % (num,) + ".jpg"
    output_path = os.path.join(output_path, name)

    try:
        requests.urllib3.disable_warnings()
        s = requests.Session()
        s.headers.update({'User-Agent': CUSTOM_USER_AGENT})
        r = s.get(url[0], stream=True, verify=False)
        if (r.status_code == 404):
            r = s.get(url[0].replace('img.', 's3.'), stream=True, verify=False)
        if (r.status_code == 404):
            r = s.get(url[0].replace('cdnwowmax', 's3.cdnwowmax'),
                      stream=True, verify=False)
        if (r.status_code == 404 and len(url) == 2):
            r = s.get(url[1], stream=True, verify=False)
        if (r.status_code == 404 and len(url) == 2):
            r = s.get(url[1].replace('img.', 's3.'), stream=True, verify=False)
        with open(output_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=4096):
                f.write(chunk)
    except:
        return
