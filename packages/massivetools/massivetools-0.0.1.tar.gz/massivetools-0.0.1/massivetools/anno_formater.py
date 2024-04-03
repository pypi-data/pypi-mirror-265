import os
import json
import glob
import cv2
import pandas as pd
import tqdm
import os.path as osp
from CVutils import type_converter as tcvt
import re

category = {'person': 0, 'falling': 1}


class LabelmeToCocoConverter:
    def __init__(self, DATAROOT, save_path, categories: list, h_w=None):
        '''
        category : ['person' , 'falling']
        '''
        self.save_path = save_path
        self.DATAROOT = DATAROOT
        self.image_files = self._get_img_paths()
        self.df_anno = pd.DataFrame(
            columns=['id', 'category_id', 'bbox', 'image_id'])
        self.df_img = pd.DataFrame(
            columns=['id', 'file_name', 'RESOLUTION', 'height', 'width'])
        self.categories = [{'id': i, 'name': cat, 'supercategory': 'None'}
                           for i, cat in enumerate(categories, 1)]
        self.anno_idx = 1
        self.idx = 1
        self.h_w = h_w

    def _get_img_paths(self):
        jpg_path = osp.join(self.DATAROOT, '**/*.jpg')
        png_path = osp.join(self.DATAROOT, '**/*.png')
        jpg_files = glob.glob(jpg_path, recursive=True)
        png_files = glob.glob(png_path, recursive=True)
        # 두 리스트를 합칩니다.
        image_files = jpg_files + png_files
        image_files = sorted(image_files)
        return image_files

    def replace_str(self, img_path):
        label_path = re.sub(r'images/(.+)\.(jpg|png)$',
                            r'labels/\1.txt', img_path)
        return label_path

    def get_img_info(self, img_path):
        if self.h_w is None:
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            height, width = img.shape
        else:
            height, width = self.h_w
        resolution = int(height * width)
        file_name = img_path
        idx = self.idx
        self.idx += 1
        return {'id': idx, 'file_name': file_name, 'RESOLUTION': resolution, 'height': height, 'width': width}

    def convert(self):
        for img_path in tqdm.tqdm(self.image_files):
            img_info = self.get_img_info(img_path)
            new_row = pd.DataFrame([img_info])
            self.df_img = pd.concat([self.df_img, new_row], ignore_index=True)

            label_path = self.replace_str(img_path)
            if osp.isfile(label_path):
                if os.path.getsize(label_path) > 0:
                    self.process_annotation(label_path, img_info)

        self.finalize_dataframes()
        self.save_to_json()

    def process_annotation(self, label_path, img_info):
        h, w = img_info['height'], img_info['width']
        with open(label_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            category_id, *yolo_bbox = map(float, line.split())
            category_id = int(category_id)
            bbox = tcvt.yolo2coco(yolo_bbox, [h, w])
            new_row = pd.DataFrame([{
                'id': self.anno_idx,
                'category_id': category_id + 1,
                'bbox': bbox,
                'image_id': img_info['id']
            }])

            self.df_anno = pd.concat(
                [self.df_anno, new_row], ignore_index=True)
            self.anno_idx += 1

    def finalize_dataframes(self):
        self.df_img['file_name'] = self.df_img['file_name'].apply(
            lambda x: x.replace(self.DATAROOT, ''))
        self.df_anno['area'] = self.df_anno['bbox'].apply(
            lambda x: x[2] * x[3])
        self.df_anno['iscrowd'] = 0
        print('DATAROOT :', self.DATAROOT)
        print('samples_num :', self.df_img.values.shape[0])

    def save_to_json(self):
        df_coco = {
            'images': self.df_img.to_dict('records'),
            'annotations': self.df_anno.to_dict('records'),
            'categories': self.categories
        }

        with open(self.save_path, "w") as json_file:
            json.dump(df_coco, json_file, indent=4)


def merge_coco_datasets(dataset1_path, dataset2_path, merged_dataset_path):
    # 데이터셋 파일을 로드
    with open(dataset1_path, 'r') as file:
        dataset1 = json.load(file)
    with open(dataset2_path, 'r') as file:
        dataset2 = json.load(file)

    # 이미지 ID와 카테고리 ID의 최대 값을 찾음
    max_image_id = max([img['id'] for img in dataset1['images']])
    max_category_id = max([cat['id'] for cat in dataset1['categories']])

    # 데이터셋2의 이미지와 카테고리 ID를 업데이트
    for img in dataset2['images']:
        img['id'] += max_image_id
    for cat in dataset2['categories']:
        cat['id'] += max_category_id

    # 애너테이션 ID 업데이트
    max_annotation_id = max([ann['id'] for ann in dataset1['annotations']])
    for ann in dataset2['annotations']:
        ann['id'] += max_annotation_id
        ann['image_id'] += max_image_id
        ann['category_id'] += max_category_id

    # 두 데이터셋 병합
    merged_dataset = {
        'images': dataset1['images'] + dataset2['images'],
        'annotations': dataset1['annotations'] + dataset2['annotations'],
        'categories': dataset1['categories'] + dataset2['categories']
    }

    # 병합된 데이터셋을 파일로 저장
    with open(merged_dataset_path, 'w') as file:
        json.dump(merged_dataset, file)


if __name__ == "__main__":
    DATAROOT = '/home/mim/dataset/human_detection/kisa_falling_w_image/'
    save_path = '/home/mim/project/CVutils/CVutils/falling.json'
    converter = LabelmeToCocoConverter(DATAROOT, save_path, categories=[
                                       'person', 'falling'],  h_w=[720, 1280])
    converter.convert()
