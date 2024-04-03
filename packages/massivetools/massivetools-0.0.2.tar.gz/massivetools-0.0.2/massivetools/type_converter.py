from datetime import timedelta
import json 
import numpy as np 
from datetime import datetime
import cv2

def get_mask(hole , boundary , shape):
    '''
    hole : list of points
    boundary : list of points
    shape : shape of the image
    '''
    
    if len(shape) == 2:
        shape = (shape[0], shape[1], 1)
    
    if not isinstance(boundary, np.ndarray) and not isinstance(hole, np.ndarray):
        lines = np.array(boundary, dtype = np.int32)
        hole = np.array(hole , dtype = np.int32)
    
    boundary = np.zeros(shape, dtype=np.int32)
    boundary_mask = cv2.fillPoly(boundary, [lines,hole], (255))
    boundary_mask = boundary_mask.astype(np.uint8)
    
    tank_img = np.zeros(shape, dtype=np.int32)
    tank_mask = cv2.fillPoly(tank_img, [hole], (255))
    tank_mask = tank_mask.astype(np.uint8)
    
    return boundary_mask, tank_mask


class NpEncoder(json.JSONEncoder):
    '''
    numpy to json format
    '''

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

# Define the function to calculate the difference in seconds between two times
def cal_time_diff(time1, time2):
    format = '%H:%M:%S'
    time1 = datetime.strptime(time1, format)
    time2 = datetime.strptime(time2, format)
    diff = time1 - time2
    
    # 결과를 적절하게 포맷하기 위해 timedelta 객체를 사용
    # 총 초를 abs() 함수로 양수로 만들고, 음수일 경우 부호를 추가합니다.
    sign = "-" if diff.total_seconds() < 0 else ""
    abs_diff = abs(diff)
    
    # timedelta 객체를 hours, minutes, seconds로 변환
    hours, remainder = divmod(abs_diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # 포맷된 시간 문자열 반환
    return f"{sign}{hours:02}:{minutes:02}:{seconds:02}"

def calculate_area(bbox , threshold = 200):
    # Calculate the area (assuming these are coordinates of rectangles)
    areas = (bbox[:, 2] - bbox[:, 0]) * (bbox[:, 3] - bbox[:, 1])

    # Filter the elements where area is greater than 100
    return areas > threshold

def cal_poly_interior_mean(frame , mask):
    temp_frame = frame.copy()
    masked_image = cv2.bitwise_and(temp_frame, temp_frame, mask=mask)
    return cv2.mean(masked_image, mask=mask)[0]  # Returns the average values for the color channels

def sec_to_format(td):
    td = timedelta(seconds=round((td) ))
    total_seconds = td.total_seconds()
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    print(f"ETA : {str(int(hours)).zfill(2)}:{str(int(minutes)).zfill(2)}:{str(int(seconds)).zfill(2)}")
    return f"{str(int(hours)).zfill(2)}:{str(int(minutes)).zfill(2)}:{str(int(seconds)).zfill(2)}"

def createML_to_coco(bboxes, dim=2):
    '''
     createML format : [x_c , y_c , w ,h]
    coco format : [x1 , y1 , w, h]
    '''
    if dim == 1:
        x_c, y_c, w, h = bboxes
        anno = [x_c - (w // 2), y_c - (h // 2),  w, h]
    else:
        anno = [[x_c - (w // 2), y_c - (h // 2),  w, h]
                for x_c, y_c, w, h in bboxes]
    return anno


def coco2cv2(bboxes, dim=2):
    # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
    '''
    coco format : [x1,y1, w,h] float or int
    cv2 format : [x1,y1,x2,y2] int
    '''
    if dim == 1:
        x1, y1, w, h = list(map(int, bboxes))
        anno = [x1, y1, x1 + w, y1 + h]
    else:
        anno = [list(map(int, [x1, y1, x1 + w, y1 + h]))
                for x1, y1, w, h in bboxes]
    return anno

def coco2yolo(bboxes , size):
    # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
    '''
    coco format : [x1,y1, w,h] float or int
    yolo format : [x_c,y_c,w,h] int, Normalized
    '''
    if not isinstance(bboxes , np.ndarray):
        bboxes = np.array(bboxes)
    if len(bboxes.shape) ==1:
        bboxes = np.expand_dims(bboxes, axis =0)
        
    c_w, c_h = size
    
    out_bboxes = []
    for bbox in bboxes:
        
        x1,y1,w,h = bbox
        x_c = (x1 + w / 2 ) / c_w
        y_c = (y1 + h / 2) / c_h
        w_c = w / c_w
        h_c = h / c_h
        out_bboxes.append([x_c ,y_c, w_c, h_c])
    return out_bboxes


def xyxy2point(bbox):
    x1,y1,x2,y2 = bbox
    return np.array([[x1,y1] , [x2,y1], [x2,y2] , [x1,y2]])

def xyxy2centric(bbox):
    x1,y1,x2,y2 = bbox
    x_c, y_c = int((x2+x1) / 2) , int((y2+y1) / 2)
    return np.array([[x_c, y_c]])
    
def yolo2xyxy(bbox):
    x_c,y_c,w,h = bbox
    x1 = x_c - w/2
    x2 = x_c + w/2
    y1 = y_c - h/2
    y2 = y_c + h/2
    return np.array([x1,y1,x2,y2])

def yolo2coco(bbox, hw):
    H, W = hw
    nx_c, ny_c, nw, nh = bbox
    x_c = nx_c * W
    y_c = ny_c * H
    w = max(int(nw * W), 0)
    h = max(int(nh * H), 0)
    x1 = max(int(x_c - w / 2), 0)
    y1 = max(int(y_c - h / 2), 0)
    return [x1, y1, w, h]
    
def cv2_to_coco(bboxes, dim=2):
    # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
    '''
    cv2 format : [x1,y1,x2,y2] int
    coco format : [x1,y1, w,h] float or int
    '''
    if dim == 1:
        x1, y1, x2, y2 = list(map(int, bboxes))
        anno = [x1, y1, x2-x1, y2-y1]
    else:
        anno = [list(map(int, [x1, y1, x2-x1, y2-y1]))
                for x1, y1, x2, y2 in bboxes]
    return anno

def get_area(bbox , dim=2 , dtype = 'cv2'):
    x1, y1 , x2 ,y2 = bbox
    return int((x2-x1) * (y2-y1))


def milliseconds_to_hh_mm_ss(milliseconds):
    # Convert milliseconds to seconds
    seconds = int(milliseconds / 1000)
    
    # Calculate hours, minutes, and remaining seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def mmdet2dict(results , score_thr):
    # only 1 batch
    preds = results._pred_instances
    preds = preds[preds.scores > score_thr]
    preds = preds.cpu()
    return {
        'bboxes' : preds.bboxes,
        'labels' : preds.labels,
        'scores': preds.scores,
    }