from pathlib import Path,PurePath
import re

collect_ignore = []
TEST_BASE_DIR = ''
TEST_FILE_PATTERN = re.compile('test_.*\.py')

def build_ignores(start_path_str, skip=False):
    start_path = Path(start_path_str)
    if start_path.is_dir():
        for subitem in start_path.iterdir():
            if not subitem.name.startswith('__'):
                build_ignores(str(subitem), skip or subitem.joinpath('SKIP.ME').is_file())
    else:
        if skip and TEST_FILE_PATTERN.match(start_path.name):
            collect_ignore.append(start_path_str)

build_ignores(TEST_BASE_DIR)