import os
import re


def generate_all_ui2py(path: str):
    files = os.listdir(path)
    ui_list = []
    pattern = re.compile(r'.*\.ui$')
    for it in files:
        if pattern.match(it):
            ui_list.append(it)
    
    for it in ui_list:
        file_path = os.path.join(path, it)
        file_name_without_ext = os.path.basename(file_path)[:-3]
        cmd = f'pyside6-uic {file_path} > {path}{os.sep}Ui_{file_name_without_ext}.py'
        os.popen(cmd)


if __name__ == '__main__':
    generate_all_ui2py(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'ui'))