from shell import run

def is_clean() -> bool:
    output = run('git status')
    return 'nothing to commit, working tree clean' in output

def get_branch() -> str:
    output = run('git branch --show-current')
    return output.strip()

def get_remotes():
    remotes = {}
    output = run('git remote -v')
    for name, url, type in [remote.split() for remote in output.strip().split('\n')]:
        if name not in remotes:
            remotes[name] = {}
        type = type[1:-1]
        remotes[name][type] = url
    return remotes
