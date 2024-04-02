import os
from pathlib import Path
from wata.file.utils import load_and_write_file


def load_file(path):
    file_ext = Path(path).suffix[1:]
    if file_ext in ['yaml', 'json', 'pkl', 'txt']:
        return eval('load_and_write_file.load_' + file_ext)(path)
    else:
        raise NameError("Unable to handle {} formatted files".format(file_ext))

def save_file(data, save_path):
    file_ext = Path(save_path).suffix[1:]
    if file_ext in ['yaml', 'json', 'pkl', 'txt']:
        return eval('load_and_write_file.write_' + file_ext)(data, save_path)
    else:
        raise NameError("Unable to handle {} formatted files".format(type))

def mkdir_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)