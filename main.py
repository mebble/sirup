import json
import nav
import git
from shell import get_arg

def summarise(repos_dir):
    repos = []
    for repo in nav.explore_repos(repos_dir):
        git_info = {
            'name': repo,
            'is_clean': git.is_clean(),
            'current_branch': git.get_branch(),
            'remotes': git.get_remotes()
        }
        repos.append(git_info)
    return repos

usage_instructions = 'Usage: python3 main.py --repos ./path/to/repos'

if __name__ == '__main__':
    repos_path, exists = get_arg('--repos')
    if not exists:
        print(usage_instructions)
        exit(1)

    summary = summarise(repos_path)
    json_output = json.dumps(summary)
    print(json_output)
