import pytest
import cv2
import numpy as np
import os
from CVutils.loader import InputConverter
from tempfile import TemporaryDirectory

@pytest.fixture
def create_test_files():
    with TemporaryDirectory() as temp_dir:
        # 여러 테스트용 이미지 파일 생성
        image_paths = []
        for i in range(3):  # 3개의 테스트 이미지 생성
            image_path = os.path.join(temp_dir, f'test_image_{i}.jpg')
            image = np.zeros((100, 100, 3), dtype=np.uint8)
            cv2.imwrite(image_path, image)
            image_paths.append(image_path)

        # 테스트용 비디오 파일 생성 (1 프레임만 있는 간단한 비디오)
        video_path = os.path.join(temp_dir, 'test_video.mp4')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(video_path, fourcc, 1, (100, 100))
        video.write(image)
        video.release()

        yield temp_dir, image_paths, video_path

def test_image_loading(create_test_files):
    _, image_paths, _ = create_test_files
    for image_path in image_paths:
        images = InputConverter.load(image_path)
        image = next(images, None)
        assert image is not None, "Failed to load image"

def test_video_loading(create_test_files):
    _, _, video_path = create_test_files
    frames = InputConverter.load(video_path)
    frame = next(frames, None)
    assert frame is not None, "Failed to load video frame"

def test_glob_pattern_loading(create_test_files):
    temp_dir, _, _ = create_test_files
    glob_pattern = os.path.join(temp_dir, '*.jpg')
    images = InputConverter.load(glob_pattern)
    loaded_images = list(images)
    assert len(loaded_images) == 3, "Failed to load images using glob pattern"