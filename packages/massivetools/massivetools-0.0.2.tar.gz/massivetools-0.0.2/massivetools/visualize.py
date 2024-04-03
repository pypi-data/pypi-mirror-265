import cv2
import numpy as np 
from pycocotools.coco import COCO
import os.path as osp
import matplotlib.pyplot as plt
import io 
from PIL import Image
import datetime

def load_videos(vido_patt):
    import fiftyone as fo
    # Create a dataset from a glob pattern of videos
    dataset = fo.Dataset.from_videos_patt(vido_patt)
    dataset.persistent = True
    
def draw_text(frame ,query , x,y):
    '''
    query : dict
    x,y : int , location 
    frame : np.ndarray
    '''
    texts = [f'{k} : {v}'for k,v in query.items()]
    for text in texts:
        cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        y += 30  # Move to the next line
        
def draw_polygons(frame, polygons : dict):
    for points in polygons.values():
        overlay = frame.copy()
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.fillPoly(overlay, [pts], (0, 255, 0))
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
        
def draw_overlay_polygons(frame, polygons : dict):
    for points in polygons.values():
        overlay = frame.copy()
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.fillPoly(overlay, [pts], (0, 0, 255))
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        
def draw_lines(frame , lines : dict):
    for line in lines.values():
        cv2.line(frame, tuple(line[0]), tuple(line[1]), (255, 0, 0), thickness=2)

def draw_bboxes(frame , bboxes , categories = None):
    for i, bbox in enumerate(bboxes):
        cv2.rectangle(frame , bbox[:2] ,bbox[2:] , (255,255,255) , thickness=5 )
        
        if categories:
            cv2.putText(frame, categories[i], bbox[:2], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
def draw_holed_polygon(frame, hole , boundary ):
    '''
    hole : list of points
    boundary : list of points
    shape : shape of the image
    '''
    overlay = frame.copy()
    
    if not isinstance(boundary, np.ndarray) and not isinstance(hole, np.ndarray):
        lines = np.array(boundary, dtype = np.int32)
        hole = np.array(hole , dtype = np.int32)
    
    image1 = cv2.fillPoly(overlay, [lines,hole], (0,255,0))
    image1 = cv2.addWeighted(image1, 0.3, frame, 0.7, 0)
    
    image2 = cv2.fillPoly(overlay, [hole], (0,0,255))
    image2 = cv2.addWeighted(image2, 0.3, frame, 0.7, 0)
    combined_img = cv2.addWeighted(image1, 0.5, image2, 0.5, 0)
    return combined_img

def put_info_on_frame(frame, fps, process_time):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, current_time, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    fps_text = f"FPS: {fps:.2f}, Process Time: {process_time}ms"
    cv2.putText(frame, fps_text, (10, frame.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)


def draw_frame_num(frame, frame_num, org = (10,50)):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1  # 글자 크기
    color = (0, 255, 0)  # 글자 색상 (B, G, R)
    thickness = 2  # 글자 두께
    frame_num = int(frame_num)
    # 이미지에 텍스트 그리기
    cv2.putText(frame, f'Frame: {frame_num}', org, font, font_scale, color, thickness, cv2.LINE_AA)
    return frame

def draw_frame_time(frame, time_queue):
    # 비디오의 FPS 가져오기
    # fps = cap.get(cv2.CAP_PROP_FPS)
    
    # 현재 프레임 번호 가져오기
    # frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)
    fps = time_queue[0] 
    frame_number = time_queue[-1]

    # 비디오 시작부터의 경과 시간 계산 (초 단위)
    elapsed_time = frame_number / fps
    elapsed_hours = int(elapsed_time / 3600)
    elapsed_minutes = int((elapsed_time % 3600) / 60)
    elapsed_seconds = int(elapsed_time % 60)

    # 시간 문자열 형식화
    current_time = f"{elapsed_hours:02}:{elapsed_minutes:02}:{elapsed_seconds:02}"

    # 텍스트 속성 설정
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (10, 100)  # 좌측 상단에 그릴 위치
    font_scale = 1  # 글자 크기
    color = (0, 255, 0)  # 글자 색상 (B, G, R)
    thickness = 2  # 글자 두께

    # 이미지에 텍스트 그리기
    cv2.putText(frame, current_time, org, font, font_scale, color, thickness, cv2.LINE_AA)
    return frame


def draw_bounding_boxes(image, boxes, labels, scores, color=(0, 255, 0), thickness=2, font_scale=0.5):
    """
    이미지에 bounding box, 레이블, 점수, 그리고 bounding box의 크기를 그립니다.

    Parameters:
    - image: np.ndarray, 이미지 데이터
    - boxes: bounding box 리스트, 각 box는 [x_min, y_min, x_max, y_max] 형태
    - labels: 각 bounding box의 레이블 리스트
    - scores: 각 bounding box의 예측 점수 리스트
    - color: bounding box의 색상, 기본값은 녹색
    - thickness: bounding box의 두께
    - font_scale: 레이블 및 점수의 글꼴 크기
    """
    for box, label, score in zip(boxes, labels, scores):
        # bounding box를 그립니다.
        start_point = (int(box[0]), int(box[1]))
        end_point = (int(box[2]), int(box[3]))
        image = cv2.rectangle(image, start_point, end_point, color, thickness)

        # bounding box의 크기를 계산합니다 (너비 x 높이).
        bbox_width = end_point[0] - start_point[0]
        bbox_height = end_point[1] - start_point[1]
        bbox_size_text = f'{bbox_width}x{bbox_height}'

        # 레이블, 점수와 bounding box의 크기를 텍스트로 합칩니다.
        text = f'{label}: {score:.2f}, Size: {bbox_size_text}'

        # 텍스트의 크기를 구합니다.
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
        
        # 텍스트 위치 조정: 이미지 경계를 넘어가는지 확인합니다.
        text_start_x = start_point[0]
        text_start_y = start_point[1] - text_height - 4
        # 텍스트가 위쪽 경계를 넘어가면 아래쪽으로 조정
        if text_start_y < 0:
            text_start_y = end_point[1] + text_height + 4

        # 텍스트 배경을 그립니다.
        image = cv2.rectangle(image, (text_start_x, text_start_y - text_height - 4), (text_start_x + text_width, text_start_y + text_height), color, -1)

        # 텍스트를 이미지에 추가합니다.
        image = cv2.putText(image, text, (text_start_x, text_start_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), thickness)

    return image

    
class COCO_visual:
    def __init__(self, DATAROOT, coco_path):
        self.coco_root = DATAROOT
        self.coco_path = coco_path
        self.coco = COCO(osp.join(DATAROOT, coco_path))

    def visual(self, image_id):
        # 이미지 정보를 가져옴
        img_info = self.coco.loadImgs(image_id)[0]

        # 이미지 경로
        img_path = osp.join(self.coco_root, img_info['file_name'])

        # 이미지를 불러옴
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # COCO 애너테이션을 표시
        annIds = self.coco.getAnnIds(imgIds=img_info['id'])
        anns = self.coco.loadAnns(annIds)

        for ann in anns:
            if 'bbox' in ann:
                bbox = ann['bbox']
                x, y, w, h = bbox
                cv2.rectangle(image, (int(x), int(y)), (int(x + w), int(y + h)), (255, 0, 0), 2)

        # 이미지를 표시
        return image

def save_classes_palette_figure(classes, palette, filename="classes_palette.png"):
    """
    주어진 클래스와 팔레트를 이용하여 시각화한 후 파일로 저장하는 함수.

    Parameters:
    - classes: 튜플 또는 리스트, 클래스 이름을 포함.
    - palette: NumPy 배열, 각 클래스에 해당하는 색상 코드를 포함.
    - filename: 문자열, 저장할 이미지 파일의 이름.
    
    # 함수 사용 예시
    save_classes_palette_figure(classes, palette, "classes_palette.png")
    """
    # 각 클래스에 대한 색상 팔레트로 시각화
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(np.array([palette]))
    ax.set_xticks(np.arange(len(classes)))
    ax.set_xticklabels(classes, rotation=90)
    ax.set_yticks([])
    ax.set_title("Classes and their Corresponding Colors")

    # 파일로 저장
    plt.savefig(filename, bbox_inches='tight')
    plt.close()  # 그림 닫기


def realtime_figure(fig , ax , x_data , y1_data , y2_data):
    ax.clear()
    ax.set_xticks(range(len(x_data)))  # x_data의 길이에 따라 눈금 위치 설정
    ax.plot(x_data, y1_data, label='tank_level', linewidth=5)
    ax.plot(x_data, y2_data,label='warning area', linewidth=5)
    plt.legend()
    ax.set_xticklabels(x_data, rotation=45, ha='right')
    # x축 설정 (예: 최근 10개 데이터만 표시)
    ax.set_xlim(max(0, len(x_data) - 30), len(x_data))
    ax.set_ylim(0, 255)
    ax.grid(True)
    plt.tight_layout()
    # 이미지로 변환
    buf = io.BytesIO()
    fig.savefig(buf, format='jpg')
    buf.seek(0)
    plot_image = Image.open(buf)
    plot_image = np.array(plot_image)
    return plot_image