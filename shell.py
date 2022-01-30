import subprocess

def run(cmd: str) -> str:
    cmd_list = cmd.split(' ')
    completed = subprocess.run(cmd_list, text=True, capture_output=True)
    output = completed.stdout
    exit_code = completed.returncode
    return output, exit_code
