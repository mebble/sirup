from shell import run

def is_clean() -> bool:
    output, code = run('git status')
    if _failed(code):
        return None
    return 'nothing to commit, working tree clean' in output

def remote_branch_status():
    output, code = run('git status -sb')
    if _failed(code):
        return {}

    branch_pair = output.split()[1]
    pair_split_index = branch_pair.find('...')
    if pair_split_index == -1:
        return {}

    remote_branch = branch_pair[pair_split_index+3:]
    is_synced = 'ahead' not in output
    return {
        'remote_branch': remote_branch,
        'synced': is_synced
    }

def get_local_branch() -> str:
    output, code = run('git branch --show-current')
    if _failed(code):
        return None
    return output.strip()

def get_remotes():
    output, code = run('git remote -v')
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

def _failed(code):
    return code != 0
