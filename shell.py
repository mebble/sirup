import subprocess
import sys

cmds = {
    'help': {
        'args': [],
        'flags': []
    },
    'sum': {
        'args': ['--repos'],
        'flags': ['--log']
    },
    'gen': {
        'args': ['--from', '--to'],
        'flags': []
    }
}

def run(cmd: str) -> str:
    cmd_list = cmd.split(' ')
    completed = subprocess.run(cmd_list, text=True, capture_output=True)
    output = completed.stdout
    err_output = completed.stderr
    exit_code = completed.returncode
    if _failed(exit_code):
        return err_output, exit_code
    return output, exit_code

def get_arg(arg_key):
    try:
        key_index = sys.argv.index(arg_key)
    except ValueError:
        return '', False

    val_index = key_index + 1
    has_val = len(sys.argv) >= val_index + 1
    if not has_val:
        return '', False

    return sys.argv[val_index], True

def get_flag(flag):
    try:
        sys.argv.index(flag)
        return True
    except ValueError:
        return False

def get_cmd():
    try:
        cmd = sys.argv[1]
    except IndexError:
        return None, False

    if cmd not in cmds:
        return None, False

    args = {}
    for arg_key in cmds[cmd]['args']:
        arg_val, exists = get_arg(arg_key)
        if not exists:
            return None, False
        args[arg_key] = arg_val

    flags = {}
    for flag in cmds[cmd]['flags']:
        exists = get_flag(flag)
        flags[flag] = exists

    return {
        'name': cmd,
        'args': args,
        'flags': flags
    }, True

def exit(code):
    sys.exit(code)

def _failed(code):
    return code != 0
