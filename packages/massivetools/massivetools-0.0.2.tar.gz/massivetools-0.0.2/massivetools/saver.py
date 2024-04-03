import cv2
from CVutils.utils import make_dirs
import os.path as osp
class OutputSave:
    '''
    dtype : video , image, images, None
    '''
    def __init__(self , dst_path, dtype ,frame_width = None, frame_height = None , cap = None, fps = None) -> None:
        self.dst_path = dst_path
        self.dtype = dtype
        make_dirs(self.dst_path)
        
        if self.dtype == 'video':
            self._init_video(cap, fps)
        if self.dtype == 'image':
            self.image_idx = 1
            
    def _init_video(self, cap , fps):
        if cap:
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if frame_width is None or frame_height is None:
            raise ValueError("frame_width and frame_height must be set either directly or through the 'cap' object")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'mp4v' or 'x264' etc.
        self.out = cv2.VideoWriter(self.dst_path, fourcc, fps, (frame_width, frame_height))

    def save_images(self , array):
        filename = osp.join(self.dst_path , f'frame_{str(self.image_idx).zfill(6)}.jpg')
        cv2.imwrite(filename, array)
        self.image_idx += 1
            
    def save(self, array):
        if self.dtype == 'video':
            self.out.write(array)
        if self.dtype == 'image':
            self.save_images(array)
