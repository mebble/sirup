import subprocess

def is_clean():
    completed = subprocess.run(['git', 'status'], text=True, capture_output=True)
    output = completed.stdout
    return 'nothing to commit, working tree clean' in output
