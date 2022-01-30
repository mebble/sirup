import subprocess
import sys

def run(cmd: str) -> str:
    cmd_list = cmd.split(' ')
    completed = subprocess.run(cmd_list, text=True, capture_output=True)
    output = completed.stdout
    exit_code = completed.returncode
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
