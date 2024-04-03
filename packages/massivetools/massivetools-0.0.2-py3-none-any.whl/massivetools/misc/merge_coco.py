import json

def load_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def merge_coco_jsons(json_files, output_file):
    max_image_id = 0
    max_annotation_id = 0
    merged_images = []
    merged_annotations = []
    categories = None  # 가정: 모든 파일의 범주가 동일

    for json_file in json_files:
        data = load_json(json_file)

        if not categories:  # 첫 파일에서 범주를 설정
            categories = data['categories']

        # 이미지 및 주석 ID 재조정
        offset_image_id = max_image_id + 1
        offset_annotation_id = max_annotation_id + 1

        for img in data['images']:
            img['id'] += offset_image_id
            merged_images.append(img)
        for ann in data['annotations']:
            ann['id'] += offset_annotation_id
            ann['image_id'] += offset_image_id
            merged_annotations.append(ann)

        # 최대 ID 업데이트
        if data['images']:
            max_image_id = max([img['id'] for img in data['images']])
        if data['annotations']:
            max_annotation_id = max([ann['id'] for ann in data['annotations']])

    # 병합된 데이터 저장
    merged_data = {
        'images': merged_images,
        'annotations': merged_annotations,
        'categories': categories
    }

    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=4)

# 사용 예시
merge_coco_jsons([
    '/home/mim/dataset/fucking/annotations/instances_default.json',
    '/home/mim/dataset/cvat/train_all_add_domestic.json',
    # '/home/mim/dataset/zip_folder/kisa_all_domestic/annotations/instances_default.json',
    # '/home/mim/dataset/cvat/train.json'
    # 추가 파일 경로
], '/home/mim/dataset/cvat/train_last.json')
