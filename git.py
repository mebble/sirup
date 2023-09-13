from collections.abc import Callable
from dataclasses import dataclass
from typing import Optional

@dataclass
class RepoSize:
    value: str
    unit: str

@dataclass
class Branch:
    local_branch: str
    remote_branch: Optional[str] = None
    is_sync: Optional[bool] = None

@dataclass
class GitInfo:
    name: str
    is_clean: Optional[bool]
    size: Optional[RepoSize]
    current_branch: Optional[Branch]
    remotes: Optional[dict[str, str]]

Runnable = Callable[[str], tuple[str, int]]

class Git:
    def __init__(self, run: Runnable):
        self.run = run

    def is_clean(self) -> Optional[bool]:
        output, code = self.run('git status')
        if _failed(code):
            return None
        return 'nothing to commit, working tree clean' in output

    def get_repo_size(self) -> Optional[RepoSize]:
        _, code1 = self.run('git gc')
        output, code2 = self.run('git count-objects -vH')
        if _failed(code1) or _failed(code2):
            return None

        output_list = output.split()
        key_index = output_list.index('size-pack:')
        val_index = key_index + 1
        unit_index = val_index + 1

        return RepoSize(value=output_list[val_index], unit=output_list[unit_index])

    def get_current_branch(self) -> Optional[Branch]:
        output, code = self.run('git status -sb')
        if _failed(code):
            return None

        if 'No commits yet' in output:
            return None

        tokens = output.split()
        branch_pair_index = tokens.index('##') + 1
        branch_pair = tokens[branch_pair_index]
        pair_split_index = branch_pair.find('...')
        if pair_split_index == -1:
            return Branch(local_branch=branch_pair)

        local_branch = branch_pair[:pair_split_index]
        remote_branch = branch_pair[pair_split_index+3:]
        is_synced = 'ahead' not in output and 'behind' not in output
        return Branch(local_branch, remote_branch, is_synced)

    def get_remotes(self) -> Optional[dict[str, str]]:
        output, code = self.run('git remote -v')
        if _failed(code):
            return None

        remotes_str = output.strip()
        if not remotes_str:
            return None

        remotes = {}
        for name, url, type in [remote.split() for remote in remotes_str.split('\n')]:
            if name not in remotes:
                remotes[name] = {}
            type = type[1:-1]
            remotes[name][type] = url
        return remotes

    def clone_repo(self, repo_name, repo_url) -> tuple[bool, str]:
        output, code = self.run(f'git clone {repo_url} {repo_name}')
        if _failed(code):
            return False, output.strip()
        return True, ''

def _failed(code):
    return code != 0
