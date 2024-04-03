import os.path as osp
import os 
import subprocess
import json
import cv2
import numpy as np
import datetime 
import glob
from datetime import timedelta
from .type_converter import sec_to_format
from .utils import make_dirs
from typing import Optional, Union, List

class Encoder:
    def __init__(self, fps, dst_path, frame_width=None, frame_height=None, cap=None):
        if cap:
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) )
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) )
        if frame_width is None or frame_height is None:
            raise ValueError("frame_width and frame_height must be set either directly or through the 'cap' object")
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'mp4v' or 'x264' etc.
        self.out = cv2.VideoWriter(dst_path, fourcc, fps, (frame_width, frame_height))

    def save_video(self, frame):
        self.out.write(frame)


def extract_frames(video_path: str, frame_numbers: List[int]) -> None:
    """
    Extract specific frames from a video and save them as images.

    Args:
        video_path (str): Path to the video file.
        frame_numbers (List[int]): List of frame numbers to extract.
    """
    # Build the select filter string for the specified frame numbers
    select_filter = '+'.join([f'eq(n\,{frame})' for frame in frame_numbers])

    # Command to extract frames using FFmpeg
    command = [
        'ffmpeg',
        '-i', video_path,  # Input video file
        '-vf', f"select='{select_filter}'",  # Select filter for specific frames
        '-vsync', 'vfr',  # Ensure variable frame rate is handled correctly
        'frame_%03d.jpg'  # Output filename pattern
    ]

    # Run the FFmpeg command
    subprocess.run(command, check=True)
    
def convert_images_to_video(image_folder : str, output_filename : str, frame_rate : int):
    """
    Converts a sequence of images in a folder to a video file using FFmpeg.

    :param image_folder: Path to the folder containing image files.
    :param output_filename: Name of the output video file.
    """
    try:
        # Constructing the FFmpeg command
        cmd = [
            'ffmpeg',
            '-framerate', '24',  # or any other framerate you prefer
            '-i', f'{image_folder}/%05d.jpg',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            output_filename
        ]

        # Execute the FFmpeg command
        subprocess.run(cmd, check=True)
        print(f"Video created successfully: {output_filename}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def cut_video(input_file, start_time, duration, output_file):
    """
    Use FFmpeg to cut a video from a specific start time to an end time.
    Args:
    input_file (str): Path to the input video file.
    start_time (str): Start time in 'HH:MM:SS' format.
    duration (str): End time in 'HH:MM:SS' format.
    output_file (str): Path to the output video file.
    """
    if not isinstance(start_time , str):
        start_time = sec_to_format(start_time)
        
    if not isinstance(duration , str):
        duration = sec_to_format(duration)
    command = [
        "ffmpeg",
        "-ss", start_time,
        "-i", input_file,
        "-t", duration,
        "-c", "copy",
        output_file
    ]
    os.system(' '.join( command))

def convert_videos_to_jpg(input_folder, output_folder, fps=0.5):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Find all MP4 files in the input folder
    video_files = glob.glob(os.path.join(input_folder, "*.mp4"))

    for video_file in video_files:
        # Extract the base name of the video file to create a subfolder for its frames
        base_name = os.path.splitext(os.path.basename(video_file))[0]
        video_output_folder = os.path.join(output_folder, base_name)

        if not os.path.exists(video_output_folder):
            os.makedirs(video_output_folder)

        # Output file pattern
        output_file_pattern = os.path.join(video_output_folder, "frame_%04d.jpg")

        # FFmpeg command
        command = [
            "ffmpeg",
            "-i", video_file,
            "-vf", f"fps={fps}",
            output_file_pattern
        ]

        # Execute the command
        subprocess.run(command, check=True)


def generate_ffmpeg_command(rtsp_url,output_dir, duration_hours=2, codec='libx264'):
    # Create a filename based on the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.mp4"

    # Full path for the output file
    output_path = os.path.join(output_dir, filename)

    # Duration in seconds
    duration_seconds = duration_hours * 60 * 60

    # Construct the FFmpeg command
    command = f"ffmpeg -hide_banner -y -loglevel error -rtsp_transport tcp -use_wallclock_as_timestamps 1 \
    -i {rtsp_url} -vcodec copy -an \
    -f segment -reset_timestamps 1 -segment_time {duration_seconds} \
    -segment_format mkv -segment_atclocktime 1 -strftime 1 {output_path}/%Y%m%dT%H%M%S.mp4"

    return command


def get_video_resolution(video_path):
    # ffprobe 명령어 실행
    command = ['ffprobe', 
               '-v', 'error', 
               '-select_streams', 'v:0', 
               '-show_entries', 'stream=width,height', 
               '-of', 'json', video_path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 결과 파싱
    try:
        video_info = json.loads(result.stdout)
        width = video_info['streams'][0]['width']
        height = video_info['streams'][0]['height']
        print(width,  height)
        return width, height
    except Exception as e:
        print(f"Error parsing video info: {e}")
        return None

def convert_avi_to_mp4(input_file_path, output_folder):
    # output 폴더 확인 및 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 입력 파일의 이름을 기반으로 출력 파일 이름 생성
    base_name = os.path.basename(input_file_path)
    output_file_path = os.path.join(output_folder, os.path.splitext(base_name)[0] + ".mp4")

    # ffmpeg 명령어 실행
    command = [
        "ffmpeg",
        "-i", input_file_path,
        "-c:v", "h264_nvenc",  # NVENC H264 코덱 사용
        output_file_path
    ]
    subprocess.run(command)

    return output_file_path

def merge_videos(video1_path, video2_path, output_path):
    """
    두 비디오 파일을 병합하여 새 파일을 생성합니다.

    :param video1_path: 첫 번째 비디오 파일의 경로
    :param video2_path: 두 번째 비디오 파일의 경로
    :param output_path: 병합된 비디오를 저장할 경로
    """
    command = [
        'ffmpeg',
        '-i', video1_path,
        '-i', video2_path,
        '-filter_complex', "[0:v] [1:v] concat=n=2:v=1:a=0 [v]",
        '-map', '[v]',
        output_path
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f'병합 완료: {output_path}')
    except subprocess.CalledProcessError as e:
        print(f'오류 발생: {e}')


def time_calculator(time_str1, time_str2, mode):
    # Convert the time strings to timedelta objects
    time1 = timedelta(hours=int(time_str1[:2]), minutes=int(time_str1[3:5]), seconds=int(time_str1[6:]))
    time2 = timedelta(hours=int(time_str2[:2]), minutes=int(time_str2[3:5]), seconds=int(time_str2[6:]))

    if mode == 'plus':
        # Add the two time deltas
        total_time = time1 + time2
    elif mode == 'minus':
        # Ensure the result is not negative by comparing the two time deltas
        if time1 > time2:
            # If time1 is greater, subtract time2 from time1 to avoid negative result
            total_time = time1 - time2
        else:
            # Otherwise, subtract time1 from time2
            total_time = time2 - time1
    else:
        return 'Invalid mode'

    # Format the total time back to a string
    # Ensure formatting for hours, minutes, and seconds
    hours, remainder = divmod(total_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    # Account for days in total_time, if any
    hours += total_time.days * 24
    formatted_total_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    return formatted_total_time

def convert_mp4_to_img(mp4_file_path, 
                       output_folder , 
                       start_time : Optional[str] = None,
                       duration : Optional[str] = None,
                       image_type : Optional[str] ='.jpg',
                       fps = '30', 
                       crop : Optional[str]= None ,
                       max_frames : Optional[int] = None,
                       ) -> None:
    '''
    crop=w:h:x:y
    '''
    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    command = ['ffmpeg']
    if start_time:
        command += ['-ss', start_time]
        if duration:
            command += ["-t", duration]
        
    command += ['-i', mp4_file_path]
    if fps:
        fps_rate = f'fps={fps}'
        if crop: # "crop=w:h:x:y" 
            fps_rate += ',' + crop
        command += ['-vf', fps_rate]  # 초당 5개의 프레임, 상단에서 200픽셀 자르기
    if max_frames:
        command += ["-frames:v", str(max_frames)] # Set the maximum number of video frames to extract
        
    command += [os.path.join(output_folder, f'frame_%06d{image_type}')]  # 출력 파일 형식 지정
    
    subprocess.run(command)
    
#'-vf', 'fps=15,crop=in_w:in_h-130:0:130',  # 초당 5개의 프레임, 상단에서 200픽셀 자르기
