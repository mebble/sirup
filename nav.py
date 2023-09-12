import os
import os.path as path
from shell import run

def explore_repos(repos_dir: str):
    repos_dir = _abs_path(repos_dir)
    repos, _ = run(f'ls {repos_dir}')
    repos = repos.strip().split()
    for repo in repos:
        _chdir(path.join(repos_dir, repo))
        yield repo

def goto_dest_dir(dest_path: str):
    dest_path = _abs_path(dest_path)
    run(f'mkdir -p {dest_path}')
    _chdir(dest_path)

def _abs_path(rel_path: str):
    return path.abspath(rel_path)

def _chdir(path: str):
    os.chdir(path)
