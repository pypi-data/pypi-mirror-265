import pytest
from CVutils.utils import make_dirs
import os.path as osp
import shutil
import os 
import unittest

def test_make_dirs():
    options = ['tmp/' , 'test/tmp/*.jpg' , 'tmp/*.mp4' , 'tmp/*']
    base_dir = make_dirs(options[0])
    assert base_dir == 'tmp/'
    base_dir = make_dirs(options[1])
    assert base_dir == 'test/tmp'
    shutil.rmtree('test/')
    base_dir = make_dirs(options[2])
    assert base_dir == 'tmp'
    base_dir = make_dirs(options[3])
    assert base_dir == 'tmp'
    shutil.rmtree('tmp')
    
    
class TestMakeDirs(unittest.TestCase):

    def setUp(self):
        # 테스트를 위한 임시 디렉토리 설정
        self.test_dir = 'test_dir/'
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def tearDown(self):
        # 각 테스트 후에 정리
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_make_dirs_with_non_existing_dir(self):
        # 존재하지 않는 새 디렉토리 생성 테스트
        path = self.test_dir + 'new_dir/'
        base_dir = make_dirs(path)
        self.assertTrue(os.path.exists(base_dir))
        self.assertEqual(base_dir, path)

    def test_make_dirs_with_existing_dir(self):
        # 이미 존재하는 디렉토리 생성 테스트
        path = self.test_dir + 'existing_dir/'
        os.makedirs(path)
        base_dir = make_dirs(path)
        self.assertTrue(os.path.exists(base_dir))
        self.assertEqual(base_dir, path)

    def test_make_dirs_with_file_path(self):
        # 파일 경로를 위한 디렉토리 생성 테스트
        path = self.test_dir + 'new_dir/sample_file.txt'
        base_dir = make_dirs(path)
        expected_dir = os.path.dirname(path)
        self.assertTrue(os.path.exists(expected_dir))
        self.assertEqual(base_dir, expected_dir)

    # def test_make_dirs_with_invalid_path(self):
    #     # 잘못된 경로로 디렉토리 생성 테스트
    #     path = '???/invalid_path/'
    #     with self.assertRaises(OSError):
    #         make_dirs(path)


@pytest.fixture(scope='function')
def test_dir(tmp_path):
    # 임시 테스트 디렉토리 생성
    dir = tmp_path / "test_dir"
    dir.mkdir()
    return dir

def test_make_dirs_with_non_existing_dir(test_dir):
    # 존재하지 않는 새 디렉토리 생성 테스트
    path = str(test_dir / 'new_dir/')
    base_dir = make_dirs(path)
    assert os.path.exists(base_dir)
    assert base_dir == path

def test_make_dirs_with_existing_dir(test_dir):
    # 이미 존재하는 디렉토리 생성 테스트
    path = str(test_dir / 'existing_dir/')
    os.makedirs(path)
    base_dir = make_dirs(path)
    assert os.path.exists(base_dir)
    assert base_dir == path

def test_make_dirs_with_file_path(test_dir):
    # 파일 경로를 위한 디렉토리 생성 테스트
    path = str(test_dir / 'new_dir/sample_file.txt')
    base_dir = make_dirs(path)
    expected_dir = os.path.dirname(path)
    assert os.path.exists(expected_dir)
    assert base_dir == expected_dir

def test_make_dirs_with_invalid_path():
    # 잘못된 경로로 디렉토리 생성 테스트
    path = '/test'
    with pytest.raises(OSError):
        make_dirs(path)