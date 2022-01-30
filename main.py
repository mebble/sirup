import nav
import git

for repo in nav.explore_repos('..'):
    print(repo)
    print(git.is_clean())
