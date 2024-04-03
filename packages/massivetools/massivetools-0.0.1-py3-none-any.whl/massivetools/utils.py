import os 
import os.path as osp


def make_dirs(target_path):
    if (target_path[-1]  == '/') or (('.' not in  osp.basename(target_path)) and ('*' not in  osp.basename(target_path))):
        # IS DIR    
        base_dir = target_path
    else:
        base_dir = os.path.dirname(target_path)
    # Create the directory structure
    if not os.path.exists(base_dir):
        os.makedirs(base_dir) # make dirs
        message = f"Directory '{base_dir}' and its subdirectories were created successfully."
    else:
        message = f"Directory '{base_dir}' already exists."
    return base_dir


def make_output_path(input_file , dst_dir , suffix = None):
    basename = osp.basename(input_file)
    if suffix is not None:
        filename, _ = osp.splitext(basename)
        basename = '.'.join([filename, suffix])
    
    dst_path = osp.join(dst_dir , basename)
    return dst_path


if __name__=='__main__':
    pass