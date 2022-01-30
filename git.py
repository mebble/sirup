from shell import run

def is_clean() -> bool:
    output, code = run('git status')
    if _failed(code):
        return None
    return 'nothing to commit, working tree clean' in output

def get_branch() -> str:
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
