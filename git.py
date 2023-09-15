from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class RepoSize:
    value: str
    unit: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        return cls(
            value=data['value'],
            unit=data['unit'],
        )

@dataclass
class Branch:
    local_branch: str
    remote_branch: Optional[str] = None
    is_sync: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        return cls(
            local_branch=data['local_branch'],
            remote_branch=data['remote_branch'],
            is_sync=data['is_sync'],
        )

@dataclass
class Repo:
    name: str
    is_clean: Optional[bool]
    size: Optional[RepoSize]
    current_branch: Optional[Branch]
    remotes: Optional[dict[str, str]]
    ignore: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        return cls(
            name=data['name'],
            is_clean=data['is_clean'],
            size=RepoSize.from_dict(data['size']),
            current_branch=Branch.from_dict(data['current_branch']),
            remotes=data['remotes'],
            ignore=data.get('ignore', False)
        )

Runnable = Callable[[str], tuple[str, int]]

class Git:
    def __init__(self, run: Runnable):
        self.run = run

    def is_git_repo(self):
        output, code = self.run('git rev-parse --is-inside-work-tree')
        if _failed(code):
            return False
        return output.strip() == 'true'

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

def parse_repos(json: Any):
    all_dicts = all(map(lambda item: isinstance(item, dict), json))
    if not all_dicts:
        return False, []

    repos: list[Repo] = []
    try:
        repos = [Repo.from_dict(item) for item in json]
    except KeyError:
        return False, []

    return True, repos
