import nav
import git

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

if __name__ == '__main__':
    summary = summarise('..')
    print(summary)

