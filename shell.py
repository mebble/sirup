import subprocess

cmds: dict[str, dict[str, list[str]]] = {
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

def run(cmd: str) -> tuple[str, int]:
    cmd_list = cmd.split(' ')
    completed = subprocess.run(cmd_list, text=True, capture_output=True)
    output = completed.stdout
    err_output = completed.stderr
    exit_code = completed.returncode
    if _failed(exit_code):
        return err_output, exit_code
    return output, exit_code

def _get_arg(argv: list[str], arg_key: str):
    try:
        key_index = argv.index(arg_key)
    except ValueError:
        return None, False

    val_index = key_index + 1
    has_val = len(argv) >= val_index + 1
    if not has_val:
        return None, False

    return argv[val_index], True

def _get_flag(argv: list[str], flag: str):
    try:
        argv.index(flag)
        return True
    except ValueError:
        return False

def get_cmd(argv: list[str]):
    try:
        cmd = argv[1]
    except IndexError:
        return None, False

    if cmd not in cmds:
        return None, False

    args: dict[str, str | None] = {}
    for arg_key in cmds[cmd]['args']:
        arg_val, exists = _get_arg(argv, arg_key)
        if not exists:
            return None, False
        args[arg_key] = arg_val

    flags: dict[str, bool] = {}
    for flag in cmds[cmd]['flags']:
        exists = _get_flag(argv, flag)
        flags[flag] = exists

    return {
        'name': cmd,
        'args': args,
        'flags': flags
    }, True

def _failed(code: int) -> bool:
    return code != 0
