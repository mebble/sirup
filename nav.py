import os
import os.path as path
from shell import run

def explore_repos(repos_dir: str):
    repos_dir = _abs_path(repos_dir)
    repo_names = [dir.name for dir in os.scandir(repos_dir) if dir.is_dir()]
    for name in repo_names:
        _chdir(path.join(repos_dir, name))
        yield name

def goto_dest_dir(dest_path: str):
    dest_path = _abs_path(dest_path)
    run(f'mkdir -p {dest_path}')
    _chdir(dest_path)

def _abs_path(rel_path: str):
    return path.abspath(rel_path)

def _chdir(path: str):
    os.chdir(path)
