
import nav
import git

def summarise(repos_dir, should_log=False):
    repos = []
    for repo in nav.explore_repos(repos_dir):
        if should_log:
            print(f'Checking repo: {repo}')
        git_info = {
            'name': repo,
            'is_clean': git.is_clean(),
            'current_branch': git.get_current_branch(),
            'remotes': git.get_remotes(),
            'size': git.get_repo_size()
        }
        repos.append(git_info)
    return repos

def generate(repos, dest_path):
    nav.goto_dest_dir(dest_path)

    failed_clones = []
    for repo in repos:
        name = repo['name']
        remotes = repo['remotes']
        try:
            remote = remotes['origin']
        except KeyError:
            remote = remotes[list(remotes)[0]]
        fetch_url = remote['fetch']
        success = git.clone_repo(name, fetch_url)
        if not success:
            failed_clones.append(repo)

    if not failed_clones:
        return True, []

    return False, failed_clones
