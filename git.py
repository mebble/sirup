from shell import run

def is_clean():
    output, code = run('git status')
    if _failed(code):
        return None
    return 'nothing to commit, working tree clean' in output

def get_repo_size():
    _, code1 = run('git gc')
    output, code2 = run('git count-objects -vH')
    if _failed(code1) or _failed(code2):
        return None

    output_list = output.split()
    key_index = output_list.index('size-pack:')
    val_index = key_index + 1
    unit_index = val_index + 1

    return {
        'value': output_list[val_index],
        'unit': output_list[unit_index]
    }

def get_current_branch():
    output, code = run('git status -sb')
    if _failed(code):
        return None

    branch_pair = output.split()[1]
    pair_split_index = branch_pair.find('...')
    if pair_split_index == -1:
        return {
            'local_branch': branch_pair
        }

    local_branch = branch_pair[:pair_split_index]
    remote_branch = branch_pair[pair_split_index+3:]
    is_synced = 'ahead' not in output and 'behind' not in output
    return {
        'local_branch': local_branch,
        'remote_branch': remote_branch,
        'synced': is_synced
    }

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

def clone_repo(repo_name, repo_url):
    output, code = run(f'git clone {repo_url} {repo_name}')
    if _failed(code):
        return False, output.strip()
    return True, ''

def _failed(code):
    return code != 0
