import time
import cv2
from datetime import datetime
# 시간, 분, 초로 계산
def time_fommater(total_seconds):
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # 00:00:00 포맷으로 변환
    formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
    return formatted_time

def get_ms_time():
    current_time = datetime.now()  # 현재 시간 가져오기
    formatted_time = current_time.strftime('%H:%M:%S')  # 시간을 '시:분:초' 형식으로 변환
    # current_time.microsecond는 마이크로초를 반환하므로, 1000으로 나누어 밀리초로 변환합니다.
    milliseconds = current_time.microsecond // 1000

    # 최종 포맷된 시간 문자열에 밀리초를 추가합니다.
    formatted_time_with_ms = f"{formatted_time}.{milliseconds:03d}"
    return formatted_time_with_ms

class FrameTimer:
    '''Frame단위 시간 측정하는 class'''
    def __init__(self, frame_count):
        self.frame_count = frame_count
        self.rate = 1 /  self.frame_count
        self.times = []

    def set_timer(self):
        self.start_time = time.time()

    def _step(self):
        '''시간을 list에다가 저장함'''
        elapsed_time = time.time() - self.start_time
        self.times.append(elapsed_time)
        if len(self.times) > self.frame_count:
            self.times.pop(0)

    def _get_avg(self ):
        '''시간의 평균을 계산'''
        if len(self.times) < self.frame_count:
            return {'fps' : 0 , 'msec' : 0}
        avg_time = sum(self.times) / len(self.times)
        fps_avg = round(1 / avg_time, 1)
        msec= round(avg_time * 1000 , 1)

        return {'fps' : fps_avg , 'msec' : msec}
    
    def draw_frame_rate(self , frame ):
        self._step()
        times = self._get_avg()
        cv2.putText(frame, f"Avg msec : {times['msec']:.2f}msec", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) 
        cv2.putText(frame, f"Avg FPS : {times['fps']:.2f} FPS", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    def print_frame_rate(self):
        self._step()
        times = self._get_avg()
        print( f"Avg msec : {times['msec']:.2f}msec", end = '\r')

    def frame_rate_control(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time < self.rate:  # 40 msec 미만이면 나머지 시간만큼 대기
            # print(f'{elapsed_time * 1000}msec')
            time.sleep(self.rate - elapsed_time)