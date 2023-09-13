import unittest
from shell import get_cmd, Command

class TestGetCmd(unittest.TestCase):
    def test_argv_unkown_cmd(self):
        self.assertEqual((None, False), get_cmd(['script.py']))
        self.assertEqual((None, False), get_cmd(['script.py', 'unknown_cmd']))

    def test_argv_invalid_args(self):
        self.assertEqual((None, False), get_cmd(['script.py', 'sum']))
        self.assertEqual((None, False), get_cmd(['script.py', 'sum', '--repos']))
        self.assertEqual((None, False), get_cmd(['script.py', 'sum', '--unknown', 'foobar']))

    def test_argv_no_flag(self):
        res, ok = get_cmd(['script.py', 'sum', '--repos', 'foobar'])
        expected = Command(name='sum', args={'--repos': 'foobar'}, flags={'--log': False})
        self.assertTrue(ok)
        self.assertEqual(expected, res)

    def test_argv_with_flag(self):
        res, ok = get_cmd(['script.py', 'sum', '--repos', 'foobar', '--log'])
        expected = Command(name='sum', args={'--repos': 'foobar'}, flags={'--log': True})
        self.assertTrue(ok)
        self.assertEqual(expected, res)

    def test_argv_unknown_flag(self):
        _, ok = get_cmd(['script.py', 'sum', '--repos', 'foobar', '--unknown_flag'])
        self.assertTrue(ok)
