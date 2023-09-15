import unittest
from unittest.mock import Mock

from git import Git, Branch, Repo, RepoSize, parse_repos

class TestGit(unittest.TestCase):
    def setUp(self) -> None:
        self.run = Mock()
        self.git = Git(self.run)

    def test_is_git_repo_fail(self):
        self.run.return_value = ('cat', 1)
        self.assertFalse(self.git.is_git_repo())

    def test_is_git_repo_no(self):
        self.run.return_value = ('\nfalse\n', 0)
        self.assertFalse(self.git.is_git_repo())

    def test_is_git_repo_yes(self):
        self.run.return_value = ('\ntrue\n', 0)
        self.assertTrue(self.git.is_git_repo())

    def test_is_clean_fail(self):
        self.run.return_value = ('cat', 1)
        self.assertIsNone(self.git.is_clean())

    def test_is_clean_no(self):
        self.run.return_value = ('cat', 0)
        self.assertFalse(self.git.is_clean())

    def test_is_clean_yes(self):
        self.run.return_value = ('foobarbaz, nothing to commit, working tree clean, foobarbaz', 0)
        self.assertTrue(self.git.is_clean())

    def test_get_repo_size_fail(self):
        git_output = (
            'whatever\n'
        )
        self.run.return_value = (git_output, 1)
        self.assertIsNone(self.git.get_repo_size())

    def test_get_repo_size(self):
        git_output = (
            'size: 123.00 KiB\n'
            'size-pack: 321.45 KiB\n'
            'in-pack: 163\n'
        )
        self.run.return_value = (git_output, 0)
        expected = RepoSize(value='321.45', unit='KiB')
        self.assertEqual(expected, self.git.get_repo_size())

    def test_get_current_branch_fail(self):
        git_output = (
            'whatever\n'
        )
        self.run.return_value = (git_output, 1)
        self.assertIsNone(self.git.get_current_branch())

    def test_get_current_branch_no_commit(self):
        git_output = (
            '## No commits yet on main\n'
        )
        self.run.return_value = (git_output, 0)
        self.assertIsNone(self.git.get_current_branch())

    def test_get_current_branch_no_remote(self):
        git_output = (
            'foobar\n'
            '## main\n'
            'foobar\n'
        )
        self.run.return_value = (git_output, 0)
        expected = Branch(local_branch='main')
        self.assertEqual(expected, self.git.get_current_branch())

    def test_get_current_branch_not_synced(self):
        git_output1 = (
            'foobar\n'
            '## main...origin/main [ahead 3]\n'
            'foobar\n'
        )
        git_output2 = (
            'foobar\n'
            '## main...origin/main [behind 3]\n'
            'foobar\n'
        )

        for git_output in [git_output1, git_output2]:
            self.run.return_value = (git_output, 0)
            expected = Branch(local_branch='main', remote_branch='origin/main', is_sync=False)
            self.assertEqual(expected, self.git.get_current_branch())

    def test_get_current_branch_synced(self):
        git_output = (
            'foobar\n'
            '## main...origin/main\n'
            'foobar\n'
        )
        self.run.return_value = (git_output, 0)
        expected = Branch(local_branch='main', remote_branch='origin/main', is_sync=True)
        self.assertEqual(expected, self.git.get_current_branch())

    def test_get_remotes_fail(self):
        git_output = (
            'whatever\n'
        )
        self.run.return_value = (git_output, 1)
        self.assertIsNone(self.git.get_remotes())

    def test_get_remotes_no_remote(self):
        git_output = '\n'
        self.run.return_value = (git_output, 0)
        self.assertIsNone(self.git.get_remotes())

    def test_get_remotes(self):
        git_output = (
            'origin  git@github.com:mebble/sirup.git (fetch)\n'
            'origin  git@github.com:mebble/sirup.git (push)\n'
        )
        self.run.return_value = (git_output, 0)
        expected = {
            'origin': {
                'fetch': 'git@github.com:mebble/sirup.git',
                'push': 'git@github.com:mebble/sirup.git',
            }
        }
        self.assertEqual(expected, self.git.get_remotes())

class ParseRepo(unittest.TestCase):
    def test_parse_repos_not_list(self):
        success, repos = parse_repos({ 'foo': 'bar' })
        self.assertFalse(success)
        self.assertEqual([], repos)

    def test_parse_repos_fail(self):
        json = [
            { 
                'name': 'foo',
                'is_clean': True,
                'size': { 'value': '123', 'unit': 'xyz' },
                'current_branch': { 'local_branch': 'foo', 'remote_branch': 'foo', 'is_sync': True },
                'remotes': {},
            },
            {
                'foo': 'bar'
            }
        ]
        success, repos = parse_repos(json)
        self.assertFalse(success)
        self.assertEqual([], repos)

    def test_parse_repos_pass(self):
        json = [
            { 
                'name': 'foo',
                'is_clean': True,
                'size': { 'value': '123', 'unit': 'xyz' },
                'current_branch': { 'local_branch': 'foo', 'remote_branch': 'foo', 'is_sync': True },
                'remotes': {},
                'ignore': True,
            },
            { 
                'name': 'foo',
                'is_clean': True,
                'size': { 'value': '123', 'unit': 'xyz' },
                'current_branch': { 'local_branch': 'foo', 'remote_branch': 'foo', 'is_sync': True },
                'remotes': {},
            }
        ]
        expected = [
            Repo(
                name='foo',
                is_clean=True,
                size=RepoSize(
                    value='123',
                    unit='xyz'
                ),
                current_branch=Branch(
                    local_branch='foo',
                    remote_branch='foo',
                    is_sync=True,
                ),
                remotes={},
                ignore=True,
            ),
            Repo(
                name='foo',
                is_clean=True,
                size=RepoSize(
                    value='123',
                    unit='xyz'
                ),
                current_branch=Branch(
                    local_branch='foo',
                    remote_branch='foo',
                    is_sync=True,
                ),
                remotes={},
                ignore=False,
            )
        ]
        success, repos = parse_repos(json)
        self.assertTrue(success)
        self.assertEqual(expected, repos)
