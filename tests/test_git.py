import unittest
from unittest.mock import Mock

from git import Git

class TestGit(unittest.TestCase):
    def setUp(self) -> None:
        self.run = Mock()
        self.git = Git(self.run)

    def test_is_clean_fail(self):
        self.run.return_value = ('cat', 1)
        self.assertIsNone(self.git.is_clean())

    def test_is_clean_no(self):
        self.run.return_value = ('cat', 0)
        self.assertFalse(self.git.is_clean())

    def test_is_clean_yes(self):
        self.run.return_value = ('foobarbaz, nothing to commit, working tree clean, foobarbaz', 0)
        self.assertTrue(self.git.is_clean())
