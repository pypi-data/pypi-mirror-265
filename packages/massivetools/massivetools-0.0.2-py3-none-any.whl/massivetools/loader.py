import cv2
import tempfile
import matplotlib.pyplot as plt
import os

class InputConverter:
    @classmethod
    def load(cls, path):
        suffix = os.path.splitext(path)[-1].lower()
        dtype = None
        if suffix in ['.mp4', '.avi']:
            dtype = 'video'
        elif suffix in ['.png', '.jpg'] or '*' in path:  # glob 패턴을 포함할 수 있도록 수정
            dtype = 'image'

        if dtype == 'image':
            return cls._read_image_files(path)
        elif dtype == 'video':
            return cls._read_video_frames(path)

    @staticmethod
    def _read_image_files(path):
        import glob
        image_path_list = sorted(glob.glob(path , recursive= True))
        print(f'image counts : {len(image_path_list)}')
        for image_path in image_path_list:
            img = cv2.imread(image_path)
            if img is not None:
                # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                yield img

    @staticmethod
    def _read_video_frames(video_path):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Could not open video.")
            return
        print(f'Frame counts : {cap.get(cv2.CAP_PROP_FRAME_COUNT)}')
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            yield frame
        cap.release()