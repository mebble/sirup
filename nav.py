import os
import os.path as path
from shell import run

def explore_repos(repos_dir):
    repos_dir = _abs_path(repos_dir)
    repos = run(f'ls {repos_dir}').strip().split()
    for repo in repos:
        _chdir(path.join(repos_dir, repo))
        yield repo

def _abs_path(rel_path):
    return path.abspath(rel_path)

def _chdir(path):
    os.chdir(path)
