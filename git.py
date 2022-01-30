import subprocess

def is_clean() -> bool:
    output = _run_cmd('git status')
    return 'nothing to commit, working tree clean' in output

def get_branch() -> str:
    output = _run_cmd('git branch --show-current')
    return output.strip()

def get_remotes():
    remotes = {}
    output = _run_cmd('git remote -v')
    for name, url, type in [remote.split() for remote in output.strip().split('\n')]:
        if name not in remotes:
            remotes[name] = {}
        type = type[1:-1]
        remotes[name][type] = url
    return remotes

def _run_cmd(cmd: str) -> str:
    cmd_list = cmd.split(' ')
    completed = subprocess.run(cmd_list, text=True, capture_output=True)
    output = completed.stdout
    return output
