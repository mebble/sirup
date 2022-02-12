
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
    print(f'Cloning repositories to {dest_path}')
    num_repos = len(repos)

    failed_clones = []
    for i, repo in enumerate(repos, start=1):
        name = repo['name']
        remotes = repo['remotes']
        ignore = repo.get('ignore', False) or remotes == None
        if ignore:
            print(f'[{i}/{num_repos}] Ignoring repo: {name}')
            continue

        clone_url = _get_clone_url(remotes)
        print(f'[{i}/{num_repos}] Cloning repo: {name}')
        success = git.clone_repo(name, clone_url)
        if not success:
            failed_clones.append(repo)
            print(f'Failed')
        else:
            print(f'Done')

    if not failed_clones:
        return True, []

    return False, failed_clones

def _get_clone_url(remotes):
    try:
        remote = remotes['origin']
    except KeyError:
        remote = remotes[list(remotes)[0]]
    fetch_url = remote['fetch']

    return fetch_url
