from pathlib import Path
import re 
import yaml
import os.path as osp
import os
from CVutils import type_converter as tc
def compute_iou(box1, box2):
    """
    Compute the Intersection over Union (IoU) of two bounding boxes.

    Parameters:
    box1, box2 : (x1, y1, x2, y2)
    x1, y1 : 왼쪽 상단 모서리의 좌표
    x2, y2 : 오른쪽 하단 모서리의 좌표

    Returns:
    float: 두 박스 간의 IoU.
    """
    # 각 박스의 (x1, y1, x2, y2) 좌표 추출
    x1_1, y1_1, x2_1, y2_1 = box1
    x1_2, y1_2, x2_2, y2_2 = box2

    # 교집합 영역 계산
    x1_inter = max(x1_1, x1_2)
    y1_inter = max(y1_1, y1_2)
    x2_inter = min(x2_1, x2_2)
    y2_inter = min(y2_1, y2_2)

    width_inter = max(0, x2_inter - x1_inter)
    height_inter = max(0, y2_inter - y1_inter)

    # 겹치는 영역이 없는 경우, IoU는 0
    if width_inter == 0 or height_inter == 0:
        return 0.0

    area_inter = width_inter * height_inter

    # 각 박스의 면적 계산
    area_box1 = (x2_1 - x1_1) * (y2_1 - y1_1)
    area_box2 = (x2_2 - x1_2) * (y2_2 - y1_2)

    # 합집합 영역 계산
    area_union = area_box1 + area_box2 - area_inter

    # IoU 계산
    iou = area_inter / area_union
    return iou


class Cfg():
    def __init__(self, dictionary = None):
        if dictionary is not None:
            for key, value in dictionary.items():
                setattr(self, key, value)

class AttributeDict(dict):
    def __getattr__(self, attr):
        return self[attr]
    def __setattr__(self, attr, value):
        self[attr] = value
        
def yaml_load(file='data.yaml', append_filename=False):
    """
    Load YAML data from a file.

    Args:
        file (str, optional): File name. Default is 'data.yaml'.
        append_filename (bool): Add the YAML filename to the YAML dictionary. Default is False.

    Returns:
        (dict): YAML data and file name.
    """
    assert Path(file).suffix in ('.yaml', '.yml'), f'Attempting to load non-YAML file {file} with yaml_load()'
    with open(file, errors='ignore', encoding='utf-8') as f:
        s = f.read()  # string

        # Remove special characters
        if not s.isprintable():
            s = re.sub(r'[^\x09\x0A\x0D\x20-\x7E\x85\xA0-\uD7FF\uE000-\uFFFD\U00010000-\U0010ffff]+', '', s)

        # Add YAML filename to dict and return
        data = yaml.safe_load(s) or {}  # always return a dict (yaml.safe_load() may return None for empty files)
        if append_filename:
            data['yaml_file'] = str(file)
        return Cfg(data)
    

def add_file_name(filename , add_str):
    if not isinstance(add_str , str):
        add_str = str(add_str)
    file, suffix = filename.split('.')
    new_name = file + '_' + add_str + '.' + suffix
    return new_name

def modi_suffix(filename , modi_str):
    file, _ = filename.split('.')
    new_name = file + '.' + modi_str
    return new_name 

def make_folders(file_path):
    # Define the base directory
    base_dir = osp.dirname(file_path)
    # Create the directory structure
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        message = f"Directory '{base_dir}' and its subdirectories were created successfully."
    else:
        message = f"Directory '{base_dir}' already exists."
        
def get_input_list(path):
    # image , images ,video , videos
    pass
    